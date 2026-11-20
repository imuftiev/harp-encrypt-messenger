from http import HTTPStatus
from typing import Annotated
from service.message_service import MessageService
from fastapi.params import Depends

from schema.message import MessageSent, MessageCreate

from fastapi import APIRouter

router = APIRouter(prefix="/messages")


@router.post("/", status_code=HTTPStatus.CREATED, response_model=MessageSent)
async def create_message(message_create: MessageCreate,
                         message_service: Annotated[MessageService, Depends()]
                         ) -> MessageSent:
    await message_service.create(message_create)