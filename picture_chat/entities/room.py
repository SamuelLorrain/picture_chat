from pydantic import BaseModel
from uuid import UUID


class Room(BaseModel):
    uuid: UUID
    name: str
