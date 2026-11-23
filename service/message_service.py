from uuid import UUID
from repository.message_repository import MessageRepository
from schema.message import MessageCreateRequest, MessageCreateData, MessageResponse


class MessageService:
    def __init__(self, repository: MessageRepository):
        self.repository = repository

    async def create(self, message_create: MessageCreateRequest, sender_id: UUID) -> MessageResponse:
        message_create = MessageCreateData(
            **message_create.model_dump(),
            sender_id=sender_id
        )
        message = await self.repository.create(message_create)
        message_response = MessageResponse(
            message_id=message.message_id,
            sender_id=message.sender_id,
            receiver=message.receiver,
            encrypt_type=message.encrypt_type,
            created_at=message.created_at
        )
        return message_response
