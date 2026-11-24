from sqlalchemy.ext.asyncio import AsyncSession
from schema.message import MessageCreateData
from model.message import Message


class MessageRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, message_create: MessageCreateData) -> Message:
        message = Message(
            message=message_create.message,
            encrypt_type=message_create.encrypt_type,
            receiver_id=message_create.receiver,
            sender_id=message_create.sender_id

        )
        self.session.add(message)
        await self.session.commit()
        return message
