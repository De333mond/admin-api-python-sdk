from admin_api.exceptions import PermissionDenied
from admin_api.grpc.auth_service import AuthGRPCService
from admin_api.permissions.verifier import PermissionVerifier
from admin_api.sdk.auth_context import AuthContext


class AdminApiAuth:
    def __init__(self, grpc_target: str, timeout_ms=300):
        self._grpc_target = grpc_target
        self._timeout_ms = timeout_ms
        self._auth_service = AuthGRPCService(grpc_target=self._grpc_target)
        self._permission_verifiers: list[PermissionVerifier] = []

    def add_permission_verifier(self, verifier: PermissionVerifier) -> None:
        self._permission_verifiers.append(verifier)

    def check(self, required: tuple[str, ...], token: str) -> AuthContext:
        with self._auth_service as service:
            payload = service.get_payload(jwt=token)
            user = service.get_user_data(jwt=token)
            auth_context = AuthContext(user=user, permissions=list(payload.permissions))

            if required and not any(permission in payload.permissions for permission in required):
                raise PermissionDenied()

            for verifier in self._permission_verifiers:
                if not verifier.validate(auth_context, required):
                    raise PermissionDenied()

            return auth_context
