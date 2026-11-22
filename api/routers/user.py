from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from schema.user import UserCreate, UserResponse
from core.dependencies.dependencies import get_user_service
from service.user_service import UserService
from core.security.security import verify_jwt_token

router = APIRouter(prefix='/users')


@router.get(
    "/all",
    response_model=list[UserResponse],
    status_code=HTTPStatus.OK
)
async def get_all_users(user_service: Annotated[UserService, Depends(get_user_service)]):
    users = await user_service.get_all()
    return users


@router.get(
    "/me",
    response_model=UserResponse,
    status_code=HTTPStatus.OK
)
async def get_current_user(user_id: Annotated[UUID, Depends(verify_jwt_token)],
                           user_service: Annotated[UserService, Depends(get_user_service)]):
    return await user_service.get_by_uuid(user_id)


@router.get(
    "/email",
    response_model=UserResponse,
    status_code=HTTPStatus.OK
)
async def get_user_by_email(
        email: str,
        user_service: Annotated[UserService, Depends(get_user_service)]
):
    user = await user_service.get_by_email(email)
    return user


@router.get(
    "/{username}",
    response_model=UserResponse,
    status_code=HTTPStatus.OK
)
async def get_user_by_username(
        username: str,
        user_service: Annotated[UserService, Depends(get_user_service)]
):
    user = await user_service.get_by_username(username)
    return user


@router.post(
    "/signup",
    status_code=HTTPStatus.CREATED,
    response_model=UserResponse
)
async def create_user(user_create: UserCreate,
                      user_service: Annotated[UserService, Depends(get_user_service)]) -> UserResponse:
    user = await user_service.create(user_create)
    return user


@router.put(
    "/update",
    status_code=HTTPStatus.ACCEPTED,
    response_model=UserResponse
)
async def update_username():
    pass


@router.delete("/", status_code=HTTPStatus.ACCEPTED)
async def delete(username: str,
                 user_service: Annotated[UserService, Depends(get_user_service)]) -> None:
    await user_service.delete(username)


@router.delete("/all", status_code=HTTPStatus.ACCEPTED)
async def delete(user_service: Annotated[UserService, Depends(get_user_service)]) -> None:
    await user_service.delete_all()
