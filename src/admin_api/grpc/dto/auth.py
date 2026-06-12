from dataclasses import dataclass
from datetime import datetime

from admin_api.grpc._generated.auth import GetUserResponse


@dataclass
class TokenPayload:
    user_id: str
    role: str
    expires_at: str
    service_name: str
    permissions: list[str]


@dataclass
class UserData:
    id: str
    external_id: str | None
    role: str
    external_role: str | None
    name: str
    surname: str
    patronymic: str
    email: str
    faculty: str | None
    login: str
    last_login: datetime
    created_at: datetime
    sex: str | None
    study_status: str | None
    degree_level: str | None
    study_group: str | None
    specialization: str | None
    finance: str | None
    form: str | None
    enter_year: str | None
    course: str | None
    type: str | None
    department_code: str | None

    @classmethod
    def from_response(cls, data: GetUserResponse) -> "UserData":
        return cls(
            id=data.id,
            external_id=data.external_id,
            role=data.role,
            external_role=data.external_role,
            name=data.name,
            surname=data.surname,
            patronymic=data.patronymic,
            email=data.email,
            faculty=data.faculty,
            login=data.login,
            last_login=datetime.fromisoformat(data.last_login),
            created_at=datetime.fromisoformat(data.created_at),
            sex=data.sex,
            study_status=data.study_status,
            degree_level=data.degree_level,
            study_group=data.study_group,
            specialization=data.specialization,
            finance=data.finance,
            form=data.form,
            enter_year=data.enter_year,
            course=data.course,
            type=data.type,
            department_code=data.department_code,
        )
