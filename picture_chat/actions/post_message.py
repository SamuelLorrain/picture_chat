from pydantic import BaseModel
from uuid import uuid4, UUID
from datetime import datetime
from picture_chat.entities.message import Message
from picture_chat.repositories.message_repository import MessageRepository
from picture_chat.repositories.user_repository import UserRepository
from picture_chat.repositories.room_repository import RoomRepository


class MessageParams(BaseModel):
    text: str
    image: bytes
    user_uuid: UUID
    room_uuid: UUID


def post_message(message_params: MessageParams) -> Message:
    message_repository = MessageRepository()
    room_repository = RoomRepository()
    user_repository = UserRepository()
    user = user_repository.get_from_uuid(message_params.user_uuid)
    room = room_repository.get_room_by_uuid(message_params.room_uuid)
    message = Message(
        uuid=uuid4(),
        text=message_params.text,
        image=message_params.image.decode('utf8'),
        datetime=datetime.now(),
        user=user,
        room=room
    )
    message_repository.store_message(message)
    return message
