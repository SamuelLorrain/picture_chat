from picture_chat.repositories.message_repository import MessageRepository


def get_all_messages():
    message_repository = MessageRepository()
    return message_repository.get_all()
