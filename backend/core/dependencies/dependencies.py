from typing import Annotated
from pwdlib import PasswordHash
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.service.user_service import UserService
from backend.service.message_service import MessageService
from backend.service.auth_service import AuthenticationService
from backend.repository.user_repository import UserRepository
from backend.core.db.session import get_session
from backend.repository.message_repository import MessageRepository


def get_password_hash() -> PasswordHash:
    return PasswordHash.recommended()


def get_user_repository(session: Annotated[AsyncSession, Depends(get_session)]) -> UserRepository:
    return UserRepository(session)


def get_user_service(
        user_repository: Annotated[UserRepository, Depends(get_user_repository)],
        password_hash: Annotated[PasswordHash, Depends(get_password_hash)]
) -> UserService:
    return UserService(
        user_repository,
        password_hash
    )


def get_auth_service(
        user_repository: Annotated[UserRepository, Depends(get_user_repository)],
        password_hash: Annotated[PasswordHash, Depends(get_password_hash)]
) -> AuthenticationService:
    return AuthenticationService(user_repository, password_hash)


def get_message_repository(
        session: Annotated[AsyncSession, Depends(get_session)]
) -> MessageRepository:
    return MessageRepository(session)


def get_message_service(
        message_repository: Annotated[MessageRepository, Depends(get_message_repository)]
) -> MessageService:
    return MessageService(message_repository)