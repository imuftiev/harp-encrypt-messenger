from .exceptions import NotFoundError, ConflictError, InvalidCredentialsError


class UserNotFound(NotFoundError):
    code = "user_not_found"
    message = "User not found"


class UserAlreadyExists(ConflictError):
    code = "user_already_exists"
    message = "User with this email already exists"


class InvalidCredentials(InvalidCredentialsError):
    code = "invalid_user_credentials"
    message = "Invalid user credentials"
