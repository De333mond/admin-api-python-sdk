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
