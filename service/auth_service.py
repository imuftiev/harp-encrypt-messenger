from pwdlib import PasswordHash
from repository.user_repository import UserRepository
from schema.user import UserAuthentication
from model.user import User
from core.exception.errors import InvalidCredentials


class AuthenticationService:
    def __init__(self, repository: UserRepository,
                 password_hash: PasswordHash):
        self.repository = repository
        self.password_hash = password_hash

    async def login(self, user_authentication: UserAuthentication):
        user = await self.authenticate_user(user_authentication)
        return user

    async def authenticate_user(self, user_authentication: UserAuthentication) -> User:
        user = await self.repository.get_by_login(user_authentication.login)
        if not user:
            raise InvalidCredentials("неправильный логин")
        password = user.password_hash
        if not self.password_hash.verify(
                user_authentication.password,
                password
        ):
            raise InvalidCredentials("неверный пароль")
        return user
