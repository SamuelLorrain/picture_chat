from uuid import UUID
import sqlite3
import os
from picture_chat.entities.message import Message
from picture_chat.entities.user import User
from typing import Optional
from datetime import datetime


class MessageRepository:
    def get_all(self) -> list[Message]:
        messages: list[Message] = []
        connection = sqlite3.connect(f"{os.path.dirname(__file__)}/../db.sqlite3")
        cursor = connection.execute("""
            SELECT user.uuid as user_uuid,
                   user.name as user_name,
                   message.uuid as uuid,
                   text,
                   image,
                   datetime
            FROM message JOIN user ON message.user_uuid = user_uuid;""")
        messages_data = cursor.fetchall()
        for message in messages_data:
            messages.append(
                Message(
                    uuid=UUID(message[2]),
                    text=message[3],
                    image=message[4],
                    datetime=datetime.fromisoformat(message[5]),
                    user=User(uuid=UUID(message[0]), name=message[1])
                )
            )
        return messages

    def store_message(self, message: Message) -> None:
        connection = sqlite3.connect(f"{os.path.dirname(__file__)}/../db.sqlite3")
        connection.execute("""
            INSERT INTO message(uuid, text, image, datetime, user_uuid)
            VALUES (?,?,?,?,?)
        """, (
            str(message.uuid),
            message.text,
            message.image,
            message.datetime,
            str(message.user.uuid)))
        connection.commit()

    def get_message_by_uuid(self, uuid: UUID) -> Optional[Message]:
        connection = sqlite3.connect(f"{os.path.dirname(__file__)}/../db.sqlite3")
        cursor = connection.execute("""
            SELECT user.uuid as user_uuid,
                   user.name as user_name,
                   message.uuid as uuid,
                   text,
                   image,
                   datetime
            FROM message JOIN user ON message.user_uuid = user_uuid
            WHERE message.uuid = ?""", (str(uuid),))
        message_data = cursor.fetchone()
        if not message_data:
            return None
        return Message(
            uuid=UUID(message_data[2]),
            text=message_data[3],
            image=message_data[4],
            datetime=datetime.fromisoformat(message_data[5]),
            user=User(uuid=UUID(message_data[0]), name=message_data[1])
        )
