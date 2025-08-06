import json
import logging
from typing import Set, Protocol, runtime_checkable

from fastapi import WebSocket


@runtime_checkable
class ConnectionManager(Protocol):
    def add(self, websocket: WebSocket) -> None: ...
    def remove(self, websocket: WebSocket) -> None: ...
    async def broadcast_tool_call(self, tool_name: str) -> None: ...
    async def broadcast_message_finished(self) -> None: ...


class WebSocketConnectionManager:
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()

    def add(self, websocket: WebSocket):
        self.active_connections.add(websocket)

    def remove(self, websocket: WebSocket):
        self.active_connections.discard(websocket)

    async def _send_message(self, payload: dict):
        message = json.dumps(payload)

        logging.info(
            f"There are {len(list(self.active_connections))} active connections"
        )
        for conn in list(self.active_connections):
            logging.info(f"Sending message to connection {message}")
            try:
                await conn.send_text(message)
                logging.info(f"Message sent")
            except Exception:
                self.remove(conn)
                logging.info(f"Message failed")

    async def broadcast_tool_call(self, tool_description: str):
        payload = {"event": "tool_call", "tool_description": tool_description}
        await self._send_message(payload)

    async def broadcast_message_finished(self):
        payload = {"event": "message_finished"}
        await self._send_message(payload)


websocket_connection_manager = WebSocketConnectionManager()


def get_connection_manager() -> ConnectionManager:
    """
    Returns the connection manager for sending messages to users in real time
    """

    return websocket_connection_manager
