from dataclasses import dataclass, field
from typing import Any


@dataclass
class AuthContext:
    user: Any
    permissions: list[str]
    middleware_result: dict[str, Any] = field(default_factory=dict)
