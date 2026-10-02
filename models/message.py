import datetime
import uuid

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class Message(Base):

    __tablename__ = "messages"

    message_id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    message: Mapped[str] = mapped_column(String(255), nullable=False)
    encrypt_type: Mapped[str]
    time_sent: Mapped[datetime.datetime] = mapped_column(nullable=False)
    sender_id: Mapped[uuid.UUID] = relationship(back_populates="messages")
    receiver_id: Mapped[uuid.UUID] = relationship(back_populates="messages")