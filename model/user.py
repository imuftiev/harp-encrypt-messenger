import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SAEnum
from core.db.base import Base
from model.role import UserRole
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
    role: Mapped["UserRole"] = mapped_column(
        SAEnum(
            UserRole,
            name="role",
            native_enum=False,
            creative_constraint=True
        ),
        nullable=False,
        default=UserRole.GUEST
    )

    sent_messages: Mapped[list["Message"]] = relationship(
        back_populates="sender",
        foreign_keys="Message.sender_id"
    )
    received_messages: Mapped[list["Message"]] = relationship(
        back_populates="receiver",
        foreign_keys="Message.receiver_id"
    )
