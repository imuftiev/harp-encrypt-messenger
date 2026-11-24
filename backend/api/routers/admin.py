from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter
from fastapi.param_functions import Depends

from schema.user import UserResponse
from service.user_service import UserService
from core.dependencies.dependencies import get_user_service

router = APIRouter(prefix="/admin")


@router.get(
    "/users/all",
    response_model=list[UserResponse],
    status_code=HTTPStatus.OK
)
async def get_all_users(user_service: Annotated[UserService, Depends(get_user_service)]):
    users = await user_service.get_all()
    return users


@router.delete("/users/", status_code=HTTPStatus.NO_CONTENT)
async def delete(username: str,
                 user_service: Annotated[UserService, Depends(get_user_service)]) -> None:
    await user_service.delete(username)


@router.delete("/users/all", status_code=HTTPStatus.NO_CONTENT)
async def delete(user_service: Annotated[UserService, Depends(get_user_service)]) -> None:
    await user_service.delete_all()
