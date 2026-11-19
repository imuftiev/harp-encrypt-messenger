from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from schema.user import UserCreate, UserRequest
from model.user import User
from model.role import Role


class UserRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_create: UserCreate) -> User:
        user = User(
            username=user_create.username,
            email=user_create.email,
            password_hash=user_create.password,
            role=Role.USER
        )
        self.session.add(user)
        await self.session.commit()
        return user

    async def get_all(self) -> list[User]:
        result = await self.session.execute(select(User))
        users = result.scalars()
        return list(users)

    async def get_by_username(self, user_request: UserRequest) -> User | None:
        result = await self.session.execute(select(User).filter_by(username=user_request.username))
        user = result.scalar()
        return user

    async def delete(self, user_request: UserRequest) -> None:
        await self.session.execute(delete(User).filter_by(username=user_request.username))
        await self.session.commit()
