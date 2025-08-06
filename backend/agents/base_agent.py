import os
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv
import json

from semantic_kernel.contents.chat_message_content import (
    ChatMessageContent,
    FunctionCallContent,
    FunctionResultContent,
)
from semantic_kernel.agents import ChatHistoryAgentThread
from semantic_kernel.contents.chat_history import ChatHistory

from backend.utils.json_encoder import CustomEncoder

load_dotenv()


class BaseAgent:
    """
    Base class for all agents.
    Not intended to be used directly.
    Handles environment variables, state store, and chat history.
    """

    def __init__(
        self,
        state_store: Dict[str, Any],
        connection_manager: Any,
        user_id: str,
        session_id: str,
    ) -> None:
        self.azure_deployment = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT")
        self.azure_openai_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.api_version = os.getenv("AZURE_OPENAI_API_VERSION")

        self.session_id = session_id
        self.user_id = user_id
        self.state_store = state_store
        self.connection_manager = connection_manager

        self.chat_history: List[Dict[str, str]] = self.state_store.get(
            user_id, f"{session_id}_chat_history", []
        )
        self.state: Optional[Any] = self.state_store.get(user_id, session_id, None)

    async def _setstate(self, state: Any) -> None:
        state = json.dumps(
            {"thread": state}, cls=CustomEncoder
        )  # Make JSON friendly version of thread state
        await self.state_store.set(self.user_id, self.session_id, state)

    async def append_to_chat_history(self, messages: List[Dict[str, str]]) -> None:
        self.chat_history.extend(messages)
        await self.state_store.set(
            user_id=self.user_id,
            session_id=f"{self.session_id}_chat_history",
            value=self.chat_history,
        )

    def _parse_message(self, msg: dict) -> ChatMessageContent:
        if "tool_calls" in msg:
            # Convert tool calls to FunctionCallContent
            items = [
                FunctionCallContent(
                    id=call["id"],
                    name=call["function"]["name"],
                    arguments=call["function"]["arguments"],
                )
                for call in msg["tool_calls"]
            ]
            return ChatMessageContent(
                role=msg["role"],
                items=items,
                name=msg.get("name"),
            )
        elif "tool_call_id" in msg:
            # This is likely a tool response
            items = [
                FunctionResultContent(id=msg["tool_call_id"], content=msg["content"])
            ]
            return ChatMessageContent(
                role=msg["role"],
                items=items,
                name=msg.get("name"),
            )
        else:
            # Plain message
            return ChatMessageContent(
                role=msg["role"],
                content=msg.get("content"),
                name=msg.get("name"),
            )

    def create_thread_from_state(self, state: dict) -> ChatHistoryAgentThread:
        thread_data = state["thread"]
        chat_history_data = thread_data["_chat_history"]
        messages_data = chat_history_data["messages"]

        messages = [self._parse_message(msg) for msg in messages_data]

        chat_history = ChatHistory(
            messages=messages, system_message=chat_history_data.get("system_message")
        )

        return ChatHistoryAgentThread(
            chat_history=chat_history, thread_id=thread_data["_id"]
        )

    async def chat_async(self, prompt: str) -> str:
        """
        Override in child class!
        """
        raise NotImplementedError("chat_async should be implemented in subclass.")
