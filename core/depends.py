from typing import Annotated
from pwdlib import PasswordHash
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from service.user_service import UserService
from repository.user_repository import UserRepository
from db.session import get_session


def get_password_hash() -> PasswordHash:
    return PasswordHash.recommended()


def get_user_repository(session: Annotated[AsyncSession, Depends(get_session)]) -> UserRepository:
    return UserRepository(session)


def get_user_service(
        session: Annotated[AsyncSession, Depends(get_session)]) -> UserService:
    return UserService(get_user_repository(session), get_password_hash())
