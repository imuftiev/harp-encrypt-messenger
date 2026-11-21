from pydantic import BaseModel, ConfigDict
from model.user import User


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str
    email: str


class UserRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str


class UserCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str
    email: str
    password: str


class UserAuthentication(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    login: str
    password: str


def to_user_response(user: User) -> UserResponse:
    return UserResponse(
        username=user.username,
        email=user.email
    )


def to_user_request(username: str) -> UserRequest:
    return UserRequest(
        username=username
    )
