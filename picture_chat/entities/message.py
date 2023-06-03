from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from picture_chat.entities.user import User


class Message(BaseModel):
    uuid: UUID
    text: str
    image: bytes
    datetime: datetime
    user: User
