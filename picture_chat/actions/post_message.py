from pydantic import BaseModel
from uuid import uuid4, UUID
from datetime import datetime
from picture_chat.entities.message import Message
from picture_chat.repositories.message_repository import MessageRepository
from picture_chat.repositories.user_repository import UserRepository


class MessageParams(BaseModel):
    text: str
    image: bytes
    user_uuid: UUID


def post_message(message_params: MessageParams) -> Message:
    message_repository = MessageRepository()
    user_repository = UserRepository()
    user = user_repository.get_from_uuid(message_params.user_uuid)
    uuid = uuid4()
    message = Message(
        uuid=uuid,
        text=message_params.text,
        image=message_params.image,
        datetime=datetime.now(),
        user=user
    )
    message_repository.store_message(message)
    return message
