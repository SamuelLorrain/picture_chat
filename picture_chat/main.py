from picture_chat.websockets import WebsocketConnectionManager
from pydantic import BaseModel
from fastapi import FastAPI, WebSocket, Response, WebSocketDisconnect, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from picture_chat.actions.get_all_messages import get_all_messages_by_room_uuid as get_all_messages_by_room_uuid_action
from picture_chat.actions.post_message import post_message as post_message_action, MessageParams
from picture_chat.serializers.message_serializer import message_to_dict
from picture_chat.actions.room_crud import get_all_rooms as get_all_rooms_action
from picture_chat.actions.room_crud import create_room as create_room_action
from picture_chat.authentication.authentication import register, get_new_token, authenticate
import json
from uuid import UUID
from picture_chat.config import Config

app = FastAPI()
origins = [
    Config().front_url,
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# https://stackoverflow.com/questions/64146591/custom-authentication-for-fastapi
def verify_token(req: Request):
    try:
        token = req.headers['Authorization']
    except KeyError:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if authenticate(token[7:]):  # Bearer TOKEN
        return True
    raise HTTPException(status_code=401, detail="Unauthorized")


@app.get('/messages/{uuid}')
def get_all_messages_by_room_uuid(uuid: UUID, authorized: bool = Depends(verify_token)):
    if authorized:
        messages = get_all_messages_by_room_uuid_action(uuid)
        return messages
    return None


websocket_connection_manager = WebsocketConnectionManager()


@app.websocket('/ws/{room_uuid}')
async def websocket_endpoint(websocket: WebSocket, room_uuid: UUID):
    await websocket_connection_manager.connect(str(room_uuid), websocket)
    try:
        while True:
            data = await websocket.receive_text()
            json_data = json.loads(data)

            if not authenticate(json_data['jwt']):
                raise WebSocketDisconnect

            del json_data['jwt']  # CODE SMELL HERE

            new_message = post_message_action(MessageParams(**json_data))
            await websocket_connection_manager.broadcast(
                str(room_uuid),
                json.dumps(message_to_dict(new_message))
            )
    except WebSocketDisconnect:
        websocket_connection_manager.disconnect(str(room_uuid), websocket)


@app.get('/room')
def get_all_rooms(authorized: bool = Depends(verify_token)):
    if authorized:
        rooms = get_all_rooms_action()
        return rooms
    return None


class RoomParams(BaseModel):
    name: str


@app.post('/room')
def create_new_room(room_param: RoomParams, authorized: bool = Depends(verify_token)):
    if authorized:
        room = create_room_action(room_param.name)
        return room
    return None


class UserParams(BaseModel):
    name: str
    password: str


@app.post('/register')
def create_new_user(user_params: UserParams):
    user = register(user_params.name, user_params.password)
    return user


@app.post('/login')
def login_user(user_params: UserParams):
    token = get_new_token(user_params.name, user_params.password)
    if token is None:
        return Response("Unable to authenticate", status_code=403)
    return {"jwt": token}
