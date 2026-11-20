from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from schema.message import MessageCreate
from model.message import Message
from model.user import User


class MessageRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, message_create: MessageCreate):
        user = await self.session.execute(select(User).filter_by(user_id=message_create.sender_id))
        receiver = await self.session.execute(select(User).filter_by(user_id=message_create.receiver_id))
        message = Message(
            message_id=message_create.message_id,
            message=message_create.message,
            encrypt_type=message_create.encrypt_type,
            time_sent=message_create.time_sent,
            sender_id=user.scalar_one_or_none(),
            receiver_id=receiver.scalar()
        )
        self.session.add(message)
        await self.session.commit()
