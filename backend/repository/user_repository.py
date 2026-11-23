from sqlalchemy import select, delete, or_
from sqlalchemy.ext.asyncio import AsyncSession
from backend.schema.user import UserCreate, UserRequest
from backend.model.user import User
from backend.core.exception.errors import UserEmailAlreadyExists, UserUsernameAlreadyExists


class UserRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_create: UserCreate) -> User:
        user = User(
            username=user_create.username,
            email=user_create.email,
            password_hash=user_create.password,
            role=user_create.role
        )
        try:
            self.session.add(user)
            await self.session.commit()
        except Exception as exc:
            await self.session.rollback()
            original_error = getattr(exc, "driver_exception", None)
            if original_error.constraint_name == "users_email_key":
                raise UserEmailAlreadyExists
            elif original_error.constraint_name == "users_username_key":
                raise UserUsernameAlreadyExists
            raise
        return user

    async def get_by_uuid(self, user_id: str) -> User | None:
        stmt = select(User).filter_by(user_id=user_id)
        user = await self.session.execute(stmt)
        return user.scalar_one_or_none()

    async def get_all(self) -> list[User]:
        result = await self.session.execute(select(User))
        users = result.scalars()
        return list(users)

    async def get_by_login(self, login: str) -> User | None:
        stmt = select(User).where(
            or_(
                User.username == login,
                User.email == login
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> User | None:
        stmt = select(User).filter_by(username=username)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(User).filter_by(email=email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def delete(self, user_request: UserRequest) -> None:
        await self.session.execute(delete(User).filter_by(username=user_request.username))
        await self.session.commit()

    async def delete_all(self) -> None:
        await self.session.execute(delete(User))
        await self.session.commit()
