from sqlalchemy import select, Result

from models.user import User
from infrastracture.session import get_session


class UserRepository:
    async def get_user_by_username(self, username: str) -> User | None:
        async with get_session() as session:
            stmt = select(User).filter_by(username=username)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def create_user(self, username) -> User | None:
        async with get_session() as session:
            stmt = select(User).filter_by(username=username)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()


def get_user_repository() -> UserRepository:
    return UserRepository()
