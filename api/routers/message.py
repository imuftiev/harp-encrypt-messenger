from http import HTTPStatus
from typing import Annotated
from uuid import UUID
from service.message_service import MessageService
from fastapi.params import Depends
from schema.message import MessageCreateRequest, MessageResponse
from core.security.security import verify_jwt_token
from fastapi import APIRouter
from core.dependencies.dependencies import get_message_service

router = APIRouter(prefix="/messages")


@router.post("/", status_code=HTTPStatus.CREATED,
             response_model=MessageResponse)
async def create_message(message_create: MessageCreateRequest,
                         message_service: Annotated[MessageService, Depends(get_message_service)],
                         sender_id: Annotated[UUID, Depends(verify_jwt_token)]
                         ) -> MessageResponse:
    message_response = await message_service.create(message_create, sender_id)
    return message_response
