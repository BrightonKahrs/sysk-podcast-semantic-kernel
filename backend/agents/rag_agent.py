# Copyright (c) Microsoft. All rights reserved.
from typing import Any, Dict, List, Optional
import logging

from semantic_kernel.connectors.ai import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.agents import AgentThread, ChatCompletionAgent
from semantic_kernel.connectors.ai import FunctionChoiceBehavior
from semantic_kernel.kernel_types import OptionalOneOrList
from azure.search.documents.indexes.models import SearchFieldDataType
from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread

from backend.plugins import azure_ai_search_plugin, MenuPlugin
from .base_agent import BaseAgent


# Configure logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class RagAgent(BaseAgent):
    def __init__(self, state_store: Dict[str, Any], session_id: str) -> None:
        super().__init__(state_store, session_id)
        self._agent = None
        self._initialized = False


    async def _setup_agent(self) -> None:
        """Initialize the assistant and tools only once."""
        if self._initialized:
            return
        
        #wrapped_ai_search_plugin = [self.instrument_tool_call(f) for f in azure_ai_search_plugin.functions]

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
        if self.state and isinstance(self.state, dict) and "thread" in self.state:
            try:
                self._thread = self.state["thread"]
                logger.info("Restored thread from SESSION_STORE")
            except Exception as e:
                logger.warning(f"Could not restore thread: {e}")

        self._initialized = True


    async def chat_async(self, prompt: str) -> str:
        # Ensure agent/tools are ready and process the prompt.
        await self._setup_agent()

        response = await self._agent.get_response(messages=prompt, thread=self._thread)
        
        logging.debug(f"Response type: {type(response)}")
        logging.debug(f"Response: {response}")
        
        response_content = str(response.content)

        self._thread = response.thread
        if self._thread:
            self._setstate({"thread": self._thread})

        messages = [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": response_content},
        ]
        self.append_to_chat_history(messages)

        return response_content