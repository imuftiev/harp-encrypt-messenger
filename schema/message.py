import datetime
import uuid

from pydantic import BaseModel


class MessageCreate(BaseModel):
    message_id: uuid.UUID
    message: str
    encrypt_type: str
    time_sent: datetime.datetime
    sender_id: uuid.UUID
    receiver_id: uuid.UUID


class MessageSent(BaseModel):
    message: str
    time_sent: datetime.datetime
    sender: str


class MessageReceive(BaseModel):
    message: str
    time_sent: datetime.datetime
    receiver: str


def to_message_sent(message_create: MessageCreate) -> MessageSent:
    return MessageSent(
        message=message_create.message,
        time_sent=message_create.time_sent,
        sender=str(message_create.sender_id)
    )


def to_message_receive(message_create: MessageCreate) -> MessageReceive:
    return MessageReceive(
        message=message_create.message,
        time_sent=message_create.time_sent,
        receiver=str(message_create.sender_id)
    )
