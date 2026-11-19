from http import HTTPStatus
from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends
from schema import UserResponse, UserCreate
from core import get_user_service
from service import UserService

router = APIRouter(prefix='/users')


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


@router.get(
    "/",
    response_model=list[UserResponse],
    status_code=HTTPStatus.OK
)
async def get_all_users(user_service: Annotated[UserService, Depends(get_user_service)]):
    users = await user_service.get_all()
    if not users:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return users


@router.post(
    "/",
    status_code=HTTPStatus.CREATED,
    response_model=UserResponse
)
async def create_user(user_create: UserCreate,
                      user_service: Annotated[UserService, Depends(get_user_service)]) -> UserResponse:
    user = await user_service.create(user_create)
    return user


@router.put(
    "/",
    status_code=HTTPStatus.ACCEPTED,
    response_model=UserResponse
)
async def update_username():
    pass


@router.delete("/", status_code=HTTPStatus.ACCEPTED)
async def delete(username: str,
                 user_service: Annotated[UserService, Depends(get_user_service)]) -> None:
    await user_service.delete(username)
