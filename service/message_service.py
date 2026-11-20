from repository.message_repository import MessageRepository
from schema.message import MessageCreate


class MessageService:
    def __init__(self, message_repository: MessageRepository):
        self.message_repository = message_repository

    async def create(self, message_create: MessageCreate):
        await self.message_repository.create(message_create)
