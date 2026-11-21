import datetime
import jwt
from schema.user import UserAuthentication
from core.settings.settings import get_settings

settings = get_settings()


def create_jwt_token(user_authentication: UserAuthentication):
    """
    Функция для создания JWT токена. Мы копируем входные данные, добавляем время истечения и кодируем токен.
    """
    to_encode = user_authentication
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=settings.access_token_expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.access_token_encrypt_algorithm)
