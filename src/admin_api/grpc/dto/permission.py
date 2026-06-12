from dataclasses import dataclass


@dataclass
class CreatePermission:
    title: str
    verbose_name: str | None


@dataclass
class Permission:
    id: str
    title: str
    verbose_name: str | None
