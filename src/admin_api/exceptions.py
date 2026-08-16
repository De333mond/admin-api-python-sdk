class AuthException(Exception):
    message: str = "Authentication error"

    def __init__(self, message: str | None = None) -> None:
        if not message:
            message = self.message
        super().__init__(message)


class PermissionDenied(AuthException):
    message = "Permissions denied error."


class TokenNotProvided(AuthException):
    message = "Token not provided."


class InvalidTokenException(AuthException):
    message = "JWT Token is invalid"


class ApiError(AuthException):
    message = "Admin API request failed"

    def __init__(
        self,
        message: str | None = None,
        *,
        status_code: int,
        error_code: str = "",
        detail: dict | list | str = "",
        errors: dict | list | str = "",
    ) -> None:
        self.status_code = status_code
        self.error_code = error_code
        self.detail = detail
        self.errors = errors
        super().__init__(message)
