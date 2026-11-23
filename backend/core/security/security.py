from datetime import datetime, timezone, timedelta
from uuid import UUID

from fastapi import Depends, HTTPException

from backend.model.user import User
from backend.core.settings.settings import get_settings
import jwt
from fastapi.security import OAuth2PasswordBearer

settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/")


def create_jwt_token(user: User) -> str:
    """
    Функция для создания JWT токена. Добавляем user_id, время создания, время истечения и кодируем токен.
    """
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user.user_id),
        "iat": now,
        "exp": now + timedelta(minutes=30)
    }
    token = jwt.encode(
        payload=payload,
        key=settings.secret_key,
        algorithm=settings.access_token_encrypt_algorithm
    )
    return token


def verify_jwt_token(token: str = Depends(oauth2_scheme)) -> UUID:
    try:
        payload = jwt.decode(token, key=settings.secret_key, algorithms=(settings.access_token_encrypt_algorithm,))
        sub = payload.get("sub")
        return UUID(sub)
    except (jwt.InvalidTokenError, ValueError, KeyError, TypeError):
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"}
        )
