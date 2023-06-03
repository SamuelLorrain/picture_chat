from pydantic import BaseModel
from uuid import UUID


class User(BaseModel):
    uuid: UUID
    name: str
