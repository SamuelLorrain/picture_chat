from uuid import UUID, uuid4
from picture_chat.entities.room import Room
from picture_chat.repositories.room_repository import RoomRepository


def get_all_rooms() -> list[Room]:
    room_repository = RoomRepository()
    return room_repository.get_all()


def get_room_by_uuid(uuid: UUID) -> Room:
    room_repository = RoomRepository()
    return room_repository.get_room_by_uuid(uuid)


def create_room(name: str) -> Room:
    room_repository = RoomRepository()
    room = Room(
        uuid=uuid4(),
        name=name
    )
    room_repository.store_room(room)
    return room
