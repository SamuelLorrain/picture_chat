from uuid import UUID
import sqlite3
import os
from picture_chat.entities.message import Message
from picture_chat.entities.user import User
from picture_chat.entities.room import Room
from typing import Optional
from datetime import datetime


class MessageRepository:
    def get_all_by_room_uuid(self, uuid: UUID) -> list[Message]:
        messages: list[Message] = []
        connection = sqlite3.connect(f"{os.path.dirname(__file__)}/../db.sqlite3")
        cursor = connection.execute("""
            SELECT user.uuid as user_uuid,
                   user.name as user_name,
                   message.uuid as uuid,
                   text,
                   image,
                   datetime,
                   room.uuid as room_uuid,
                   room.name as room_name
            FROM message
            JOIN room ON message.room_uuid = room.uuid
            JOIN user ON message.user_uuid = user.uuid
            WHERE room.uuid = ?
            ORDER BY datetime""", (str(uuid),))
        messages_data = cursor.fetchall()
        print(len(messages_data))
        for message in messages_data:
            messages.append(
                Message(
                    uuid=UUID(message[2]),
                    text=message[3],
                    image=message[4],
                    datetime=datetime.fromisoformat(message[5]),
                    user=User(uuid=UUID(message[0]), name=message[1]),
                    room=Room(uuid=UUID(message[6]), name=message[7])
                )
            )
        connection.close()
        return messages

    def store_message(self, message: Message) -> None:
        connection = sqlite3.connect(f"{os.path.dirname(__file__)}/../db.sqlite3")
        connection.execute("""
            INSERT INTO message(uuid, text, image, datetime, user_uuid, room_uuid)
            VALUES (?,?,?,?,?,?)
        """, (
            str(message.uuid),
            message.text,
            message.image,
            message.datetime,
            str(message.user.uuid),
            str(message.room.uuid)))
        connection.commit()
        connection.close()

    def get_message_by_uuid(self, uuid: UUID) -> Optional[Message]:
        connection = sqlite3.connect(f"{os.path.dirname(__file__)}/../db.sqlite3")
        cursor = connection.execute("""
            SELECT user.uuid as user_uuid,
                   user.name as user_name,
                   message.uuid as uuid,
                   text,
                   image,
                   datetime,
                   room.uuid as room_uuid,
                   room.name as room_name
            FROM message
            JOIN user ON message.user_uuid = user_uuid
            JOIN room ON message.room_uuid = room.uuid
            WHERE message.uuid = ?""", (str(uuid),))
        message_data = cursor.fetchone()
        connection.close()
        if not message_data:
            return None
        return Message(
            uuid=UUID(message_data[2]),
            text=message_data[3],
            image=message_data[4],
            datetime=datetime.fromisoformat(message_data[5]),
            user=User(uuid=UUID(message_data[0]), name=message_data[1]),
            room=Room(uuid=UUID(message_data[6]), name=message_data[7]),
        )
