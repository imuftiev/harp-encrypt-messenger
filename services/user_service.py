from sqlalchemy import Result

from schemas.user_schema import UserResponse
from repositories.user_repository import get_user_repository

user_repository = get_user_repository()

class UserService:

    async def get_user_by_username(self, username) -> UserResponse:
        user = await user_repository.get_user_by_username(username)
        user_response = user.columns()
