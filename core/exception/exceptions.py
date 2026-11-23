class AppError(Exception):
    code = "internal_error"
    message = "Internal server error"

    def __init__(self, message: str | None = None, *, details: dict | None = None):
        self.message = message or self.message
        self.details = details or {}
        super().__init__(self.message)


class NotFoundError(AppError):
    code = "NOT_FOUND"
    message = "Resource not found"

class AuthenticationError(AppError):
    code = "AUTHENTICATION_ERROR"
    message = "Authentication error"


class InvalidCredentialsError(AppError):
    code = "INVALID"
    message = "Invalid credentials"


class ConflictError(AppError):
    code = "CONFLICT"
    message = "Resource already exists"


class ForbiddenError(AppError):
    code = "FORBIDDEN"
    message = "Access denied"
