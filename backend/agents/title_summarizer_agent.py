from semantic_kernel.connectors.ai import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai import FunctionChoiceBehavior


class TitleSummarizerAgent:
    def __init__(self) -> None:
        self._agent = None
        self._initialized = False

    async def _setup_agent(self) -> None:
        """Initialize the assistant and tools only once."""
        if self._initialized:
            return

        # Set up the chat completion agent for summarizations
        self._agent = ChatCompletionAgent(
            name="SummarizerAgent",
            description="An agent that is purpose built to summarize content into a title",
            service=AzureChatCompletion(),
            instructions="""
                You are a helpful assistant that summarizes content into a meaningful title
                Limit the number of filler words
                Keep the title catchy and to the point
                
                You MUST make the title no more than 5 words
                """,
            function_choice_behavior=FunctionChoiceBehavior.Auto(),
            plugins=[],
        )

    async def summarize_content(self, messages: dict) -> str:
        await self._setup_agent()
        messages = str(messages)
        response = await self._agent.get_response(messages=messages)
        response_content = str(response.content)

        return response_content
