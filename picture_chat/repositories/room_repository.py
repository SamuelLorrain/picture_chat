from uuid import UUID
import sqlite3
import os
from picture_chat.entities.message import Message
from picture_chat.entities.room import Room
from typing import Optional


class RoomRepository:
    def get_all(self) -> list[Room]:
        rooms: list[Room] = []
        connection = sqlite3.connect(f"{os.path.dirname(__file__)}/../db.sqlite3")
        cursor = connection.execute("""
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
        connection.close()
        return rooms

    def store_room(self, room: Room) -> None:
        connection = sqlite3.connect(f"{os.path.dirname(__file__)}/../db.sqlite3")
        connection.execute("""
            INSERT INTO room(uuid, name)
            VALUES (?,?)
        """, (str(room.uuid), room.name))
        connection.commit()
        connection.close()

    def get_room_by_uuid(self, uuid: UUID) -> Optional[Message]:
        connection = sqlite3.connect(f"{os.path.dirname(__file__)}/../db.sqlite3")
        cursor = connection.execute("""
            SELECT uuid, name
            FROM room
            WHERE room.uuid = ?""", (str(uuid),))
        room_data = cursor.fetchone()
        connection.close()
        if not room_data:
            return None
        return Room(
            uuid=UUID(room_data[0]),
            name=room_data[1],
        )
