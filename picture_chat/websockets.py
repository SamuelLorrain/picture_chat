from collections import defaultdict
from fastapi import WebSocket


class WebsocketConnectionManager:
    def __init__(self):
        self.active_connections = defaultdict(list)

    async def connect(self, connection_id: str, socket: WebSocket):
        await socket.accept()
        self.active_connections[connection_id].append(socket)

    def disconnect(self, connection_id: str, socket: WebSocket):
        sockets = self.active_connections[connection_id]
        sockets.remove(socket)

    async def broadcast(self, connection_id: str, message: str):
        for socket in self.active_connections[connection_id]:
            await socket.send_text(message)
