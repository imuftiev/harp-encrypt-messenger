class AppError(Exception):
    code = "internal_error"
    message = "Internal server error"

    def __init__(self, message: str | None = None, *, details: dict | None = None):
        self.message = message or self.message
        self.details = details or {}
        super().__init__(self.message)


class NotFoundError(AppError):
    code = "not_found"
    message = "Resource not found"


class ConflictError(AppError):
    code = "conflict"
    message = "Resource already exists"


class ForbiddenError(AppError):
    code = "forbidden"
    message = "Access denied"
