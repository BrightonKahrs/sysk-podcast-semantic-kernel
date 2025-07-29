# connection_manager.py
import json
from typing import Set

from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()

    def add(self, websocket: WebSocket):
        self.active_connections.add(websocket)

    def remove(self, websocket: WebSocket):
        self.active_connections.discard(websocket)

    async def broadcast(self, message: str):
        event = json.dumps({
            'event': 'tool_call',
            'tool_name': message
        })
        for conn in list(self.active_connections):
            try:
                await conn.send_text(event)
            except Exception:
                self.remove(conn)

# singleton instance
connection_manager = ConnectionManager()

