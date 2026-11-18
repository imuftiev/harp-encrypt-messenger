from repository.user_repository import UserRepository
from schema import UserCreate, UserResponse, UserRequest
from schema import to_user_response, to_user_request


class UserService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def create(self, user_create: UserCreate) -> UserResponse:
        user = await self.repository.create(user_create)
        return to_user_response(user)

    async def get_by_username(self, username: str) -> UserResponse:
        user_request = to_user_request(username)
        user = await self.repository.get_by_username(user_request)
        return to_user_response(user)

    async def get_all(self) -> list[UserResponse]:
        users = await self.repository.get_all()
        return list(map(to_user_response, users))
