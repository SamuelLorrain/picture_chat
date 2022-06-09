from django.contrib.auth.models import User
from django.db.models import Q
from .models import Room, Message
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import MessageSerializer

@api_view(['GET', 'POST'])
def getMessages(request):
    if request.method == 'GET':
        room = Room.objects.get(pk=2)
        user = User.objects.get(pk=1)
        messages = Message.objects.filter(
            Q(room=room) & Q(user=user)
        )
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        room = Room.objects.get(pk=2)
        user = User.objects.get(pk=1)

        data = request.data
        # TODO valid data with the serializer
        message = Message.objects.create(
            room=room,
            user=user,
            text=data['text'],
            image=data['canvas']
        )

        return Response(MessageSerializer(message))
