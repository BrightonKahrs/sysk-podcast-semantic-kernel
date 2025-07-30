import asyncio
import logging
from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.ai import FunctionChoiceBehavior
from semantic_kernel.contents.chat_history import ChatHistory
from backend.plugins.azure_ai_search_plugin import azure_ai_search_plugin
from backend.plugins.menu_plugin import MenuPlugin

import json

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'to_dict'):
            return obj.to_dict()
        elif hasattr(obj, '__dict__'):
            return obj.__dict__
        return super().default(obj)
    
def to_dict(obj):
    if hasattr(obj, 'to_dict'):
        return obj.to_dict()
    elif hasattr(obj, '__dict__'):
        result = {}
        for key, value in obj.__dict__.items():
            result[key] = to_dict(value) if hasattr(value, '__dict__') else value
        return result
    elif isinstance(obj, list):
        return [to_dict(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: to_dict(value) for key, value in obj.items()}
    else:
        return obj


# Configure logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def main():
    # Initialize the agent
    agent = ChatCompletionAgent(
        name="PodcastAgent",
        description="An agent that can answer questions about the Stuff You Should Know podcast episodes.",
        service=AzureChatCompletion(),
        instructions="You are a helpful assistant that can answer questions about the Stuff You Should Know podcast episodes. Use the Azure AI Search to find relevant information.",
        function_choice_behavior=FunctionChoiceBehavior.Auto(),
        plugins=[azure_ai_search_plugin, MenuPlugin()],
    )

    # Create a thread with minimal mock chat history
    chat_history = ChatHistory()
    thread = ChatHistoryAgentThread(chat_history=chat_history, thread_id="debug-thread-001")

    prompt = "What is the podcast episode about the history of coffee?"

    response = await agent.get_response(messages=prompt, thread=thread)

    logger.info(f"Type of response: {type(response)}")
    logger.info(f"Response content: {response.content}")

    thread = response.thread

    # json_str = {
    #     "thread": json.dumps(thread, cls=CustomEncoder)
    # }

    response_dict = {"thread": to_dict(thread)}

    print(type(response_dict))
    print(response_dict)


if __name__ == '__main__':
    asyncio.run(main())