from http import HTTPStatus
from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends
from schema import UserResponse, UserCreate
from common.depends import get_user_service
from service.user_service import UserService

router = APIRouter(prefix='/user')


@router.get(
    "/",
    response_model=UserResponse,
    status_code=HTTPStatus.OK
)
async def get_user_by_username(
        username: str,
        user_service: Annotated[UserService, Depends(get_user_service)]
):
    user = await user_service.get_by_username(username)
    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return user


@router.get(
    "/all",
    response_model=list[UserResponse],
    status_code=HTTPStatus.OK
)
async def get_all(user_service: Annotated[UserService, Depends(get_user_service)]):
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
