import bcrypt
from typing import Optional
from uuid import UUID
from picture_chat.entities.user import User
from picture_chat.repositories.connection_manager import ConnectionManager

class UserRepository:
    def get_from_uuid(self, uuid: UUID) -> Optional[User]:
        with  ConnectionManager() as cursor:
            cursor.execute("""
                SELECT uuid, name
                FROM chat_user
                WHERE uuid = %s;
            """, (str(uuid),))
            user_data = cursor.fetchone()
        if not user_data:
            return None
        return User(uuid=UUID(user_data[0]), name=user_data[1])

    def verify_user_credentials(self, name: str, password: str) -> Optional[User]:
        with  ConnectionManager() as cursor:
            cursor.execute("""
                SELECT uuid, password
                FROM chat_user
                WHERE name = %s;
            """, (name,))
            data = cursor.fetchone()
        user = data if data is not None and len(data) == 2 else None
        if user is None:
            return None
        plain_password = password.encode('utf-8')
        hashed_password = user[1].encode('utf-8')
        if not bcrypt.checkpw(plain_password, hashed_password):
            return None
        return User(
            uuid=UUID(user[0]),
            name=name
        )

    def create_new_user(self, user: User, encrypted_password: bytes):
        with  ConnectionManager() as cursor:
            cursor.execute("""
                INSERT INTO chat_user(uuid, name, password)
                VALUES (%s,%s,%s)
            """, (
                str(user.uuid),
                user.name,
                encrypted_password
            ))
