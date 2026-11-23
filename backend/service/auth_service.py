from pwdlib import PasswordHash
from backend.repository.user_repository import UserRepository
from backend.schema.user import UserAuthentication
from backend.model.user import User
from backend.core.exception.errors import InvalidCredentialsError
from backend.core.security.security import create_jwt_token


class AuthenticationService:
    def __init__(self, repository: UserRepository,
                 password_hash: PasswordHash):
        self.repository = repository
        self.password_hash = password_hash

    async def login(self, user_authentication: UserAuthentication):
        user = await self.authenticate_user(user_authentication)
        token = create_jwt_token(user)
        return {
            "access_token": token,
            "token_type": "Bearer"
        }

    async def authenticate_user(self, user_authentication: UserAuthentication) -> User:
        user = await self.repository.get_by_login(user_authentication.login)
        if not user:
            raise InvalidCredentialsError("No user found with matching email/username")
        password = user.password_hash
        if not self.password_hash.verify(
                user_authentication.password,
                password
        ):
            raise InvalidCredentialsError("Invalid password")
        return user
