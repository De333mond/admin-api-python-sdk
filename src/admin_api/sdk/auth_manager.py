from admin_api.grpc.auth_service import AuthGRPCService
from admin_api.sdk.auth_context import AuthContext


class AdminApiAuth:
    def __init__(self, grpc_target: str, timeout_ms=300):
        self._grpc_target = grpc_target
        self._timeout_ms = timeout_ms
        self._auth_service = AuthGRPCService(grpc_target=self._grpc_target)

    def check(self, required: tuple[str, ...], token: str) -> AuthContext:
        with self._auth_service as service:
            payload = service.get_payload(jwt=token)
            user = service.get_user_data(jwt=token)

            if required and not any(permission in payload.permissions for permission in required):
                raise Exception("Permission denied error")

            return AuthContext(user=user, permissions=list(payload.permissions))
