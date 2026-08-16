from __future__ import annotations

from pydantic import TypeAdapter

from admin_api.api.request import Operation
from admin_api.api.users.schemas import FullUser, UserPermissions


class Users:
    def get_me(self) -> Operation[FullUser]:
        return Operation("GET", "/api/v1/users/me", adapter=TypeAdapter(FullUser))

    def get_permissions(self, service_name: str) -> Operation[UserPermissions]:
        return Operation(
            "GET",
            "/api/v1/users/permissions",
            adapter=TypeAdapter(UserPermissions),
            params={"service_name": service_name},
        )
