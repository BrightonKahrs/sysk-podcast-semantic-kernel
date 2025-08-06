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

    async def _send_message(self, payload: dict):
        message = json.dumps(payload)

        for conn in list(self.active_connections):
            try:
                await conn.send_text(message)
            except Exception:
                self.remove(conn)

    async def broadcast_tool_call(self, tool_name: str):
        payload = {"event": "tool_call", "tool_name": tool_name}
        await self._send_message(payload)

    async def broadcast_message_finished(self):
        payload = {"event": "message_finished"}
        await self._send_message(payload)


# Singleton instance
connection_manager = ConnectionManager()


def get_connection_manager() -> ConnectionManager:
    """
    Returns the connection manager for sending messages to users in real time
    """

    return ConnectionManager()
