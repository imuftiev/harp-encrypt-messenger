import uuid
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.base import Base
from models.message import Message


class User(Base):

    __table__name="users"

    user_id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str]

    messages: Mapped[List["Message"]] = relationship(back_populates="user")


