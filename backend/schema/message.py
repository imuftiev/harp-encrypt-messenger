import datetime
from uuid import UUID

from pydantic import BaseModel
from backend.model.encryption import Encryption


class MessageCreateRequest(BaseModel):
    message: str
    encrypt_type: Encryption = Encryption.PLAIN
    receiver: str


class MessageResponse(BaseModel):
    message_id: UUID
    sender_id: UUID
    receiver: str
    encrypt_type: Encryption
    created_at: datetime.datetime


class MessageCreateData(MessageCreateRequest):
    sender_id: UUID
