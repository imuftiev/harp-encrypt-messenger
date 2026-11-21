from pwdlib import PasswordHash
from core.exception.errors import UserNotFound
from repository.user_repository import UserRepository
from schema.user import UserCreate, UserResponse
from schema.user import to_user_response, to_user_request


class UserService:

    def __init__(self, repository: UserRepository, password_hash: PasswordHash):
        self.repository = repository
        self.password_hash = password_hash

    async def create(self, user_create: UserCreate) -> UserResponse:
        user_create.password = self.password_hash.hash(user_create.password)
        user = await self.repository.create(user_create)
        return to_user_response(user)

    async def get_by_username(self, username: str) -> UserResponse:
        user_request = to_user_request(username)
        user = await self.repository.get_by_username(user_request.username)
        if not user:
            raise UserNotFound(f"User with username: {username} not found!")
        return to_user_response(user)

    async def get_all(self) -> list[UserResponse]:
        users = await self.repository.get_all()
        return list(map(to_user_response, users))

    async def delete(self, username: str) -> None:
        user_request = to_user_request(username)
        await self.repository.delete(user_request)
