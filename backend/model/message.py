import datetime
import uuid
from backend.model.encryption import Encryption
from sqlalchemy import Enum as SAEnum
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.core.db.base import Base


class Message(Base):
    __tablename__ = "messages"

    message_id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )
    message: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    encrypt_type: Mapped["Encryption"] = mapped_column(
        SAEnum(
            Encryption,
            name="encrypt_type",
            native_enum=False,
            create_constraint=True
        ),
        nullable=False,
        default=Encryption.PLAIN
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        nullable=False,
        default=datetime.datetime.now()
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
