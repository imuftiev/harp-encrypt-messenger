from pydantic import BaseModel, ConfigDict, Field
from backend.model.user import User
from backend.model.role import UserRole
from pydantic import EmailStr


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str
    email: str


class UserRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str | None = None
    email: EmailStr | None = None


class UserSender(BaseModel):
    user_id: str


class UserReceiver(BaseModel):
    user_id: str


class UserCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str = Field(max_length=16, min_length=3)
    email: EmailStr
    password: str
    role: UserRole | None = UserRole.USER


class UserAuthentication(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    login: str
    password: str


def to_user_response(user: User) -> UserResponse:
    return UserResponse(
        username=user.username,
        email=user.email
    )


def to_user_request(username: str | None = None, email: str | None = None) -> UserRequest:
    return UserRequest(
        username=username,
        email=email
    )
