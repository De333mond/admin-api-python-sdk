from collections.abc import Callable
from typing import TypeAlias

from admin_api.exceptions import PermissionDenied
from admin_api.grpc.auth_service import AuthGRPCService
from admin_api.permissions.verifier import PermissionVerifier
from admin_api.sdk.auth_context import AuthContext

Middleware: TypeAlias = Callable[[AuthContext], dict | None]


class AdminApiAuth:
    def __init__(self, grpc_target: str, timeout_ms=300):
        self._grpc_target = grpc_target
        self._timeout_ms = timeout_ms
        self._auth_service = AuthGRPCService(grpc_target=self._grpc_target)
        self._permission_verifiers: list[PermissionVerifier] = []
        self._middlewares: list[Middleware] = []

    def add_permission_verifier(self, verifier: PermissionVerifier) -> None:
        self._permission_verifiers.append(verifier)

    def set_middlewares(self, middlewares: list[Middleware]) -> None:
        self._middlewares = middlewares

    def _get_auth_context(self, service: AuthGRPCService, token: str) -> AuthContext:
        payload = service.get_payload(jwt=token)
        user = service.get_user_data(jwt=token)
        return AuthContext(user=user, permissions=list(payload.permissions))

    def _run_middlewares(self, auth_context: AuthContext) -> None:
        for middleware in self._middlewares:
            result = middleware(auth_context)
            if result:
                middleware_name = middleware.__name__
                auth_context.middleware_result.update({middleware_name: result})

    def check(self, required: tuple[str, ...], token: str) -> AuthContext:
        with self._auth_service as service:
            auth_context = self._get_auth_context(service, token)
            self._run_middlewares(auth_context)

            if required and not any(permission in auth_context.permissions for permission in required):
                raise PermissionDenied()

            for verifier in self._permission_verifiers:
                if not verifier.validate(auth_context, required):
                    raise PermissionDenied()

            return auth_context
