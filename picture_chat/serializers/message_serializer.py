from picture_chat.entities.message import Message


def message_to_dict(message: Message) -> dict:
    return {
        "uuid": str(message.uuid),
        "text": message.text,
        "image": message.image.decode('ascii'),
        "datetime": str(message.datetime),
        "user": {
            "name": str(message.user.name),
            "uuid": str(message.user.uuid)
        }
    }
