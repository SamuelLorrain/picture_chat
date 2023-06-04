from uuid import UUID
from picture_chat.repositories.message_repository import MessageRepository


def get_all_messages_by_room_uuid(uuid: UUID):
    message_repository = MessageRepository()
    return message_repository.get_all_by_room_uuid(uuid)
