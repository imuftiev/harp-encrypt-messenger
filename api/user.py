from http import HTTPStatus
from fastapi import APIRouter, HTTPException
from repositories.user_repository import get_user_repository
from schemas.user_schema import UserResponse

user_repository = get_user_repository()

router = APIRouter(prefix='/user')


@router.get("/{username}", response_model=UserResponse, status_code=HTTPStatus.FOUND)
async def get_user(username: str):
    user = await user_repository.get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return user

