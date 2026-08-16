from __future__ import annotations

from typing import Annotated

from pydantic import Field

from admin_api.api.dto import (
    FullNaturalUser,
    FullOrganizationalUser,
    UnitScopeResponse,
    UnitTypeScopeResponse,
)

FullUser = Annotated[
    FullNaturalUser | FullOrganizationalUser,
    Field(discriminator="kind"),
]
Scope = Annotated[
    UnitScopeResponse | UnitTypeScopeResponse,
    Field(discriminator="type"),
]
UserPermissions = dict[str, list[Scope]]
