# Copyright (c) Microsoft. All rights reserved.
from typing import Any, Dict, List, Optional
import logging
import json

from semantic_kernel.connectors.ai import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.agents import AgentThread, ChatCompletionAgent
from semantic_kernel.connectors.ai import FunctionChoiceBehavior
from semantic_kernel.kernel_types import OptionalOneOrList
from azure.search.documents.indexes.models import SearchFieldDataType
from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.contents.chat_message_content import ChatMessageContent

from backend.plugins.azure_ai_search_plugin import azure_ai_search_plugin
from backend.plugins.menu_plugin import MenuPlugin
from backend.agents.base_agent import BaseAgent
from backend.utils.connection_manager import connection_manager

# Configure logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class RagAgent(BaseAgent):
    def __init__(self, state_store: Dict[str, Any], user_id: str, session_id: str) -> None:
        super().__init__(state_store, user_id, session_id)
        self._agent = None
        self._initialized = False


    async def _setup_agent(self) -> None:
        """Initialize the assistant and tools only once."""
        if self._initialized:
            return

        # Set up the chat completion agent with the Azure OpenAI service and Azure AI Search plugin.
        self._agent = ChatCompletionAgent(
            name="PodcastAgent",
            description="An agent that can answer questions about the Stuff You Should Know podcast episodes.",
            service = AzureChatCompletion(),
            instructions="You are a helpful assistant that can answer questions about the Stuff You Should Know podcast episodes. Use the Azure AI Search to find relevant information.",
            function_choice_behavior=FunctionChoiceBehavior.Auto(),
            plugins=[azure_ai_search_plugin, MenuPlugin()],
        )


        # Create a thread to hold the conversation.
        self._thread: ChatHistoryAgentThread | None = None
        # Re‑create the thread from persisted state (if any)

        if self.state:
            self.state = json.loads(self.state)

        if self.state and isinstance(self.state, dict) and 'thread' in self.state:
            try:
                self._thread = self.create_thread_from_state(self.state)
                logger.info("Restored thread from SESSION_STORE")
            except Exception as e:
                logger.warning(f"Error when restoring thread: {e}")
        else:
            logger.warning(f"State thread not found, starting from blank")


    async def chat_async(self, prompt: str) -> str:
        # Ensure agent/tools are ready and process the prompt.
        await self._setup_agent()

        response = await self._agent.get_response(messages=prompt, thread=self._thread)
        
        logging.debug(f"Response type: {type(response)}")
        logging.debug(f"Response: {response}")

        await connection_manager.broadcast_message_finished()
        
        response_content = str(response.content)
        self._thread = response.thread

        if self._thread:
            await self._setstate(self._thread)

        messages = [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": response_content},
        ]
        await self.append_to_chat_history(messages)

        return response_content