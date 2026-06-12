from dataclasses import dataclass, field
from typing import Any

from admin_api.grpc.dto.auth import UserData


@dataclass
class AuthContext:
    user: UserData
    permissions: list[str]
    middleware_result: dict[str, Any] = field(default_factory=dict)
