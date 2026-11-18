import datetime
import uuid
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base


class Message(Base):
    __tablename__ = "messages"

    message_id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True
    )
    message: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    encrypt_type: Mapped[str]
    time_sent: Mapped[datetime.datetime] = mapped_column(
        nullable=False
    )

    sender_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.user_id"),
        nullable=False
    )

    receiver_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.user_id"),
        nullable=False
    )

    sender: Mapped["User"] = relationship(
        back_populates="sent_messages",
        foreign_keys=[sender_id]
    )
    receiver: Mapped["User"] = relationship(
        back_populates="received_messages",
        foreign_keys=[receiver_id]
    )
