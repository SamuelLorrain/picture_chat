from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from picture_chat.actions.get_all_messages import get_all_messages as get_all_messages_action
from picture_chat.actions.post_message import post_message as post_message_action, MessageParams
from picture_chat.serializers.message_serializer import message_to_dict
import json

app = FastAPI()

origins = [
    'http://localhost:3000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/messages')
def get_all_messages():
    messages = get_all_messages_action()
    return messages


@app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        json_data = json.loads(data)
        new_message = post_message_action(MessageParams(**json_data))
        await websocket.send_text(json.dumps(message_to_dict(new_message)))
