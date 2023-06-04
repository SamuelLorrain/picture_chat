from uuid import UUID
import json
import os
import datetime
from picture_chat.entities.message import Message
from picture_chat.repositories.user_repository import UserRepository
from picture_chat.serializers.message_serializer import message_to_dict
from typing import Optional


class MessageRepository:

    def get_all(self) -> list[Message]:
        user_repository = UserRepository()
        messages = []
        with open(f"{os.path.dirname(__file__)}/../data/messages.json", "r") as file:
            messages_from_file = json.load(file)
        for i in messages_from_file["messages"]:
            messages.append(
                Message(
                    uuid=UUID(i['uuid']),
                    text=i['text'],
                    image=i['image'],
                    datetime=datetime.datetime.now(),
                    user=user_repository.get_from_uuid(UUID(i['user_uuid']))
                )
            )
        return messages

    def store_message(self, message: Message) -> None:
        messages = None
        with open(f"{os.path.dirname(__file__)}/../data/messages.json", "r") as file:
            messages = json.load(file)
        message_dict = message_to_dict(message)
        messages["messages"].append(message_dict)
        with open(f"{os.path.dirname(__file__)}/../data/messages.json", "w") as file:
            file.write(json.dumps(messages))

    def get_message_by_uuid(self, uuid: UUID) -> Optional[Message]:
        user_repository = UserRepository()
        messages = None
        with open(f"{os.path.dirname(__file__)}/../data/messages.json", "r") as file:
            messages = json.load(file)
        for message in messages:
            if message["uuid"] == str(uuid):
                return Message(
                    uuid=UUID(message['uuid']),
                    text=message['text'],
                    image=message['image'],
                    datetime=datetime.datetime.now(),
                    user=user_repository.get_from_uuid(
                        UUID(message['user_uuid'])
                    )
                )
        return None
