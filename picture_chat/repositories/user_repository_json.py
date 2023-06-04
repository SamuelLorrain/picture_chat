import os
import json
from typing import Optional
from uuid import UUID
from picture_chat.entities.user import User


class UserRepository:
    def get_from_uuid(self, uuid: UUID) -> Optional[User]:
        file_content = None
        with open(f"{os.path.dirname(__file__)}/../data/users.json") as file:
            file_content = json.load(file)

        for i in file_content["users"]:
            if i["uuid"] == str(uuid):
                return User(uuid=UUID(i["uuid"]), name=i["name"])
        return None
