from typing import Annotated
import os
from dotenv import load_dotenv

from semantic_kernel.functions import kernel_function
from semantic_kernel.connectors.ai.open_ai import AzureTextEmbedding
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery

from backend.utils.connection_manager import ConnectionManager

load_dotenv()

SEARCH_CLIENT = SearchClient(
    endpoint=os.getenv("AZURE_AI_SEARCH_ENDPOINT"),
    index_name=os.getenv("AZURE_AI_SEARCH_INDEX_NAME"),
    credential=AzureKeyCredential(os.getenv("AZURE_AI_SEARCH_API_KEY")),
)

EMBEDDING_GENERATOR = AzureTextEmbedding()


class AzureAISearchPlugin:
    """Searches against Azure AI Search to learn about podcast episode information"""

    def __init__(self, connection_manager: ConnectionManager):
        self.connection_manager = connection_manager

    @kernel_function(
        description="Get general information about podcast episodes and their trancscripts based on a query"
    )
    async def vector_search_podcast_transcripts(
        self,
        query: Annotated[str, "What to search for"],
        top: Annotated[int, "Number of results to return"],
    ) -> str:

        await self.connection_manager.broadcast_tool_call(
            "Looking up transcripts from Azure AI Search"
        )

        try:
            vector = await EMBEDDING_GENERATOR.generate_embeddings([query])

            vector = vector.tolist()
            vector = vector[0]

            vector_query = VectorizedQuery(
                vector=vector,
                k_nearest_neighbors=5,
                fields="embedding",
                kind="vector",
                exhaustive=True,
            )

            results = SEARCH_CLIENT.search(
                vector_queries=[vector_query],
                select=["title", "publish_date", "description", "transcript"],
                top=top,
                include_total_count=True,
            )

            results_formatted = [
                f"Podcast episode title: {result['title']}, Description: {result['description']}, Publish Date: {result['publish_date']}, Transcript: {result['transcript']}"
                for result in results
            ]

            return results_formatted

        except Exception as ex:
            print(f"Vector search failed: {ex}")
