from dataclasses import dataclass, field
from typing import Any, Generic, TypeVar

from admin_api.api.users.schemas import FullUser, UserPermissions

ApiT = TypeVar("ApiT")


@dataclass
class AuthContext(Generic[ApiT]):
    api: ApiT
    user: FullUser
    permissions: UserPermissions
    middleware_result: dict[str, Any] = field(default_factory=dict)
