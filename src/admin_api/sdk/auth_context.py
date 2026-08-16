from dataclasses import dataclass, field
from typing import Any, Generic, TypeVar

ApiT = TypeVar("ApiT")


@dataclass
class AuthContext(Generic[ApiT]):
    api: ApiT
    user: Any
    permissions: Any
    middleware_result: dict[str, Any] = field(default_factory=dict)
