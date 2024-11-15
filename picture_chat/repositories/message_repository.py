from uuid import UUID
from picture_chat.entities.message import Message
from picture_chat.entities.user import User
from picture_chat.entities.room import Room
from typing import Optional
from datetime import datetime
from picture_chat.repositories.connection_manager import ConnectionManager


class MessageRepository:
    def get_all_by_room_uuid(self, uuid: UUID) -> list[Message]:
        messages: list[Message] = []
        with ConnectionManager() as cursor:
            cursor.execute("""
                SELECT chat_user.uuid as user_uuid,
                       chat_user.name as user_name,
                       message.uuid as uuid,
                       text,
                       image,
                       datetime,
                       room.uuid as room_uuid,
                       room.name as room_name
                FROM message
                JOIN room ON message.room_uuid = room.uuid
                JOIN chat_user ON message.user_uuid = chat_user.uuid
                WHERE room.uuid = %s
                ORDER BY datetime""", (str(uuid),))
            messages_data = cursor.fetchall()
        for message in messages_data:
            messages.append(
                Message(
                    uuid=UUID(message[2]),
                    text=message[3],
                    image=message[4].encode('utf8'),
                    datetime=datetime.fromisoformat(message[5]),
                    user=User(uuid=UUID(message[0]), name=message[1]),
                    room=Room(uuid=UUID(message[6]), name=message[7])
                )
            )
        return messages

    def store_message(self, message: Message) -> None:
        with ConnectionManager() as cursor:
            cursor.execute("""
                INSERT INTO message(uuid, text, image, datetime, user_uuid, room_uuid)
                VALUES (%s,%s,%s,%s,%s,%s)
            """, (
                str(message.uuid),
                message.text,
                message.image.decode('utf8'),
                message.datetime,
                str(message.user.uuid),
                str(message.room.uuid)))

    def get_message_by_uuid(self, uuid: UUID) -> Optional[Message]:
        with ConnectionManager() as cursor:
            cursor.execute("""
                SELECT chat_user.uuid as user_uuid,
                       chat_user.name as user_name,
                       message.uuid as uuid,
                       text,
                       image,
                       datetime,
                       room.uuid as room_uuid,
                       room.name as room_name
                FROM message
                JOIN chat_user ON message.user_uuid = user_uuid
                JOIN room ON message.room_uuid = room.uuid
                WHERE message.uuid = %s""", (str(uuid),))
            message_data = cursor.fetchone()

        if not message_data:
            return None
        return Message(
            uuid=UUID(message_data[2]),
            text=message_data[3],
            image=message_data[4].encode('utf8'),
            datetime=datetime.fromisoformat(message_data[5]),
            user=User(uuid=UUID(message_data[0]), name=message_data[1]),
            room=Room(uuid=UUID(message_data[6]), name=message_data[7]),
        )
