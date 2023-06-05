import os
import sqlite3
import bcrypt
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
        connection.close()
        if not user_data:
            return None
        return User(uuid=UUID(user_data[0]), name=user_data[1])

    # TODO SHOULD THE REPOSITORY HAVE
    # THIS ROLE ?
    def verify_user_credentials(self, name: str, password: str) -> Optional[User]:
        connection = sqlite3.connect(f"{os.path.dirname(__file__)}/../db.sqlite3")
        cursor = connection.execute("""
            SELECT uuid, password
            FROM user
            WHERE name = ?;
        """, (name,))
        data = cursor.fetchone()
        connection.close()

        user = data if data is not None and len(data) == 2 else None
        if user is None:
            return None
        if not bcrypt.checkpw(password.encode('utf-8'), user[1]):
            return None
        return User(
            uuid=UUID(user[0]),
            name=name
        )

    def create_new_user(self, user: User, encrypted_password: bytes):
        connection = sqlite3.connect(f"{os.path.dirname(__file__)}/../db.sqlite3")
        connection.execute("""
            INSERT INTO user(uuid, name, password)
            VALUES (?,?,?)
        """, (
            str(user.uuid),
            user.name,
            encrypted_password
        ))
        connection.commit()
        connection.close()
