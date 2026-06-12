from admin_api.permissions.base import PermissionBase
from admin_api.sdk.auth_context import AuthContext


class PermissionVerifier:
    def __init__(self):
        self._permissions: dict[str, type[PermissionBase]] = {}

    def add_permission(self, permission: type[PermissionBase]) -> None:
        self._permissions.update({permission.title: permission})

    def validate(self, auth_context: AuthContext, required_permissions: tuple[str, ...]):
        validation_result = True
        for permission in required_permissions:
            if perm := self._permissions.get(permission):
                validation_result = perm.check(auth_context)
            if not validation_result:
                return validation_result

        return validation_result
