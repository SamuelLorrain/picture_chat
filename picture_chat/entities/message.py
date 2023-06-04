from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from picture_chat.entities.user import User
from picture_chat.entities.room import Room


class Message(BaseModel):
    uuid: UUID
    text: str
    image: bytes
    datetime: datetime
    user: User
    room: Room
