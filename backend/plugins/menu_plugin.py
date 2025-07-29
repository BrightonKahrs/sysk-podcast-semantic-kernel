import asyncio
from typing import Annotated
import time

from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.functions import kernel_function

from backend.utils.connection_manager import connection_manager

"""
The following sample demonstrates how to create a chat completion agent that
answers questions about a sample menu using a Semantic Kernel Plugin. The Chat
Completion Service is passed directly via the ChatCompletionAgent constructor.
Additionally, the plugin is supplied via the constructor.
"""

# Define a sample plugin for the sample
class MenuPlugin:
    """A sample Menu Plugin used for the concept sample."""

    @kernel_function(description="Provides a list of specials from the menu.")
    async def get_specials(self) -> Annotated[str, "Returns the specials from the menu."]:

        await connection_manager.broadcast_tool_call('Menu Tool')

        time.sleep(10)

        return """
        Special Soup: Clam Chowder
        Special Salad: Cobb Salad
        Special Drink: Chai Tea
        """

    @kernel_function(description="Provides the price of the requested menu item.")
    def get_item_price(
        self, menu_item: Annotated[str, "The name of the menu item."]
    ) -> Annotated[str, "Returns the price of the menu item."]:
        return "$9.99"