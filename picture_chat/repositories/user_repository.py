import os
import sqlite3
from typing import Optional
from uuid import UUID
from picture_chat.entities.user import User


class UserRepository:
    def get_from_uuid(self, uuid: UUID) -> Optional[User]:
        connection = sqlite3.connect(f"{os.path.dirname(__file__)}/../db.sqlite3")
        cursor = connection.execute("""
            SELECT uuid, name
            FROM user
            WHERE uuid = ?;
        """, (str(uuid),))
        user_data = cursor.fetchone()
        if not user_data:
            return None
        return User(uuid=UUID(user_data[0]), name=user_data[1])
