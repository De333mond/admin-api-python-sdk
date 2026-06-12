import abc

from admin_api.sdk.auth_context import AuthContext


class PermissionValidatorBase(abc.ABC):
    @abc.abstractmethod
    def validate(self, auth_context: AuthContext) -> bool:
        raise NotImplementedError


class PermissionBase(abc.ABC):
    title: str
    validator: type[PermissionValidatorBase]

    @classmethod
    def check(cls, auth_context: AuthContext) -> bool:
        return cls.validator().validate(auth_context)
