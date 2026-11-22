from .exceptions import NotFoundError, ConflictError, InvalidCredentialsError


class UserNotFound(NotFoundError):
    code = "user_not_found"
    message = "User not found"


class UserEmailAlreadyExists(ConflictError):
    code = "user_email_already_exists"
    message = "User with this email already exists"


class UserUsernameAlreadyExists(ConflictError):
    code = "user_username_already_exists"
    message = "User with this username already exists"


class InvalidCredentials(InvalidCredentialsError):
    code = "invalid_credentials"
    message = "Invalid user credentials"
