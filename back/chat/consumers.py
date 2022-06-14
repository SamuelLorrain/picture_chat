from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Room, Message
from django.core.serializers import serialize
import json
from asgiref.sync import async_to_sync

class ChatConsumer(WebsocketConsumer):
    def getAllData(self):
        # TODO authentication
        room = Room.objects.get(pk=2)
        user = User.objects.get(pk=1)
        messages = Message.objects.filter(
            Q(room=room) & Q(user=user)
        )
        return messages

    def connect(self):
        room = Room.objects.get(pk=2)
        self.route_group_name = room.name

        async_to_sync(self.channel_layer.group_add)(
            self.route_group_name,
            self.channel_name
        )

        self.accept()
        # TODO authentication
        user = User.objects.get(pk=1)
        messages = Message.objects.filter(
            Q(room=room) & Q(user=user)
        )
        messagesString = serialize('json', self.getAllData())
        self.send(text_data=messagesString)

    def receive(self, text_data):
        # TODO authentication
        room = Room.objects.get(pk=2)
        user = User.objects.get(pk=1)

        data = json.loads(text_data)
        # TODO valid data with the serializer
        Message.objects.create(
            room=room,
            user=user,
            text=data['text'],
            image=data['canvas']
        )
        messagesString = serialize('json', self.getAllData())

        async_to_sync(self.channel_layer.group_send)(
            self.route_group_name,
            {
                'type':'chat_message',
                'message':messagesString
            }
        )

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=message)


    # def disconnect(self, close_code):
    #     pass

