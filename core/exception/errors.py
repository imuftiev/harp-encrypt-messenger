from .exceptions import NotFoundError, ConflictError


class UserNotFound(NotFoundError):
    code = "user_not_found"
    message = "User not found"


class UserAlreadyExists(ConflictError):
    code = "user_already_exists"
    message = "User with this email already exists"