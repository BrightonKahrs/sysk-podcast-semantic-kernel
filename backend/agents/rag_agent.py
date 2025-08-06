# Copyright (c) Microsoft. All rights reserved.
from typing import Any, Dict
import json

from semantic_kernel.connectors.ai import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread

from backend.plugins.azure_ai_search_plugin import AzureAISearchPlugin
from backend.plugins.analytics_plugin import AnalyticsPlugin
from backend.agents.base_agent import BaseAgent
from backend.utils.connection_manager import ConnectionManager


class RagAgent(BaseAgent):
    def __init__(
        self,
        state_store: Dict[str, Any],
        connection_manager: ConnectionManager,
        user_id: str,
        session_id: str,
    ) -> None:
        super().__init__(state_store, connection_manager, user_id, session_id)
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
            service=AzureChatCompletion(),
            instructions="""
            You are a helpful assistant that can answer questions about the Stuff You Should Know podcast episodes. 
            Use the AnalyticsPlugin to run sql statements to answer analytics style questions of the podcast episodes - for example this would be a good tool to use if a user asks "how many podcast episodes aired in 2023?"
            Use the azure_ai_search_plugin to get detailed information about episodes, including the description and specific transcripts.

            When using the AnalyticsPlugin-query_sql tool. You MUST pass it only a tsql readable query string and nothing else

            Where it makes sense, use a combination of the plugins to come to the right answer
            """,
            function_choice_behavior=FunctionChoiceBehavior.Auto(),
            plugins=[
                AzureAISearchPlugin(self.connection_manager),
                AnalyticsPlugin(self.connection_manager),
            ],
        )

        # Create a thread to hold the conversation.
        self._thread: ChatHistoryAgentThread | None = None
        # Re‑create the thread from persisted state (if any)

        if self.state:
            self.state = json.loads(self.state)

        if self.state and isinstance(self.state, dict) and "thread" in self.state:
            try:
                self._thread = self.create_thread_from_state(self.state)
            except Exception as e:
                pass

    async def chat_async(self, prompt: str) -> str:
        # Ensure agent/tools are ready and process the prompt.
        await self.connection_manager.broadcast_tool_call("Determining what to do")

        await self._setup_agent()
        response = await self._agent.get_response(messages=prompt, thread=self._thread)

        response_content = str(response.content)
        self._thread = response.thread

        if self._thread:
            await self._setstate(self._thread)

        messages = [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": response_content},
        ]
        await self.append_to_chat_history(messages)

        await self.connection_manager.broadcast_message_finished()

        return response_content
