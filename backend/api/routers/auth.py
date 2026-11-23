from typing import Annotated, Any
from backend.service.auth_service import AuthenticationService
from fastapi.params import Depends
from backend.core.dependencies.dependencies import get_auth_service
from backend.schema.user import UserAuthentication

from fastapi import APIRouter

router = APIRouter(prefix="/auth/login")


@router.post("/")
async def auth(
        user_authentication: UserAuthentication,
        auth_service: Annotated[AuthenticationService, Depends(get_auth_service)]) -> Any:
    token = await auth_service.login(user_authentication)
    return token
