from collections.abc import Callable
from typing import TypeAlias

from admin_api.api.client import SyncApi
from admin_api.exceptions import PermissionDenied
from admin_api.permissions.verifier import PermissionVerifier
from admin_api.sdk.auth_context import AuthContext

Middleware: TypeAlias = Callable[[AuthContext], dict | None]


class AdminApiAuth:
    def __init__(
        self,
        api: SyncApi | None = None,
        *,
        base_url: str | None = None,
        timeout_ms: int = 300,
        service_name: str | None = None,
    ) -> None:
        if api is None and base_url is not None:
            api = SyncApi(base_url, timeout=timeout_ms / 1000)
        self._root_api = api
        self._timeout_ms = timeout_ms
        self._service_name = service_name
        self._permission_verifiers: list[PermissionVerifier] = []
        self._middlewares: list[Middleware] = []

    def add_permission_verifier(self, verifier: PermissionVerifier) -> None:
        self._permission_verifiers.append(verifier)

    def set_middlewares(self, middlewares: list[Middleware]) -> None:
        self._middlewares = middlewares

    def context_from_token(self, token: str) -> AuthContext[SyncApi]:
        if self._root_api is None:
            raise ValueError("Provide api or base_url")
        if not self._service_name:
            raise ValueError("service_name is required")
        user_api = self._root_api.bind(token)
        user = user_api.send(user_api.users.get_me())
        permissions = user_api.send(user_api.users.get_permissions(self._service_name))
        return AuthContext(api=user_api, user=user, permissions=permissions)

    def _run_middlewares(self, auth_context: AuthContext) -> None:
        for middleware in self._middlewares:
            result = middleware(auth_context)
            if result:
                middleware_name = middleware.__name__
                auth_context.middleware_result.update({middleware_name: result})

    def check(self, required: tuple[str, ...], token: str) -> AuthContext:
        auth_context = self.context_from_token(token)
        self._run_middlewares(auth_context)

        if required and not any(permission in auth_context.permissions for permission in required):
            raise PermissionDenied()

        for verifier in self._permission_verifiers:
            if not verifier.validate(auth_context, required):
                raise PermissionDenied()

        return auth_context
