import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.base import Base
from model.role import Role
from model.message import Message


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(
        unique=True,
        nullable=False
    )
    username: Mapped[str] = mapped_column(
        unique=True,
        nullable=False
    )
    password_hash: Mapped[str] = mapped_column(
        nullable=False
    )
    role: Mapped["Role"]

    sent_messages: Mapped[list["Message"]] = relationship(
        back_populates="sender",
        foreign_keys="Message.sender_id"
    )
    received_messages: Mapped[list["Message"]] = relationship(
        back_populates="receiver",
        foreign_keys="Message.receiver_id"
    )
