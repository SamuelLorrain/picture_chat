from pydantic import BaseModel
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from picture_chat.actions.get_all_messages import get_all_messages_by_room_uuid as get_all_messages_by_room_uuid_action
from picture_chat.actions.post_message import post_message as post_message_action, MessageParams
from picture_chat.serializers.message_serializer import message_to_dict
from picture_chat.actions.room_crud import get_all_rooms as get_all_rooms_action
from picture_chat.actions.room_crud import create_room as create_room_action
import json
from uuid import UUID

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


@app.get('/messages/{uuid}')
def get_all_messages_by_room_uuid(uuid: UUID):
    messages = get_all_messages_by_room_uuid_action(uuid)
    return messages


@app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        json_data = json.loads(data)
        new_message = post_message_action(MessageParams(**json_data))
        await websocket.send_text(json.dumps(message_to_dict(new_message)))


@app.get('/room')
def get_all_rooms():
    rooms = get_all_rooms_action()
    return rooms


class RoomParam(BaseModel):
    name: str


@app.post('/room')
def create_new_room(room_param: RoomParam):
    room = create_room_action(room_param.name)
    return room
