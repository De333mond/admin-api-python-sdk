from dataclasses import dataclass

from admin_api.grpc.dto.auth import UserData


@dataclass
class AuthContext:
    user: UserData
    permissions: list[str]
