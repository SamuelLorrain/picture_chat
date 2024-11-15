from uuid import UUID
from picture_chat.entities.message import Message
from picture_chat.entities.room import Room
from typing import Optional

from picture_chat.repositories.connection_manager import ConnectionManager


class RoomRepository:
    def get_all(self) -> list[Room]:
        rooms: list[Room] = []
        with  ConnectionManager() as cursor:
            cursor.execute("""
                SELECT uuid, name
                FROM room;""")
            rooms_data = cursor.fetchall()
            for room in rooms_data:
                rooms.append(
                    Room(
                        uuid=UUID(room[0]),
                        name=room[1],
                    )
                )
        return rooms

    def store_room(self, room: Room) -> None:
        with  ConnectionManager() as cursor:
            cursor.execute("""
                INSERT INTO room(uuid, name)
                VALUES (%s,%s)
            """, (str(room.uuid), room.name))

    def get_room_by_uuid(self, uuid: UUID) -> Optional[Message]:
        with  ConnectionManager() as cursor:
            cursor.execute("""
                SELECT uuid, name
                FROM room
                WHERE room.uuid = %s""", (str(uuid),))
            room_data = cursor.fetchone()

        if not room_data:
            return None
        return Room(
            uuid=UUID(room_data[0]),
            name=room_data[1],
        )
