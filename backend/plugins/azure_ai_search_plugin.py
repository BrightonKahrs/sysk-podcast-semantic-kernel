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
        description="Get general information about podcast episodes and their trancscripts based on a query. Use ONLY if you need to find transcrript level information"
    )
    async def search_podcast_transcripts(
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
                search_text=query,
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

    @kernel_function(
        description="Find information about the podcast episode by its title"
    )
    async def podcast_episode_search_by_title(
        self, podcast_title: Annotated[str, "the episode to search for"]
    ) -> str:

        await self.connection_manager.broadcast_tool_call(
            f"Getting information from the {podcast_title} episode"
        )

        results = SEARCH_CLIENT.search(
            include_total_count=True,
            search_text=podcast_title,
            search_fields=["title"],
            select=["title", "publish_date", "description", "transcript"],
            top=3,
        )

        results_formatted = [
            f"Podcast episode title: {result['title']}, Description: {result['description']}, Publish Date: {result['publish_date']}, Transcript: {result['transcript']}"
            for result in results
        ]

        return results_formatted

    @kernel_function(description="Get podcast titles and descriptions based on a query")
    async def hybrid_search_episodes(
        self,
        query: Annotated[str, "what to search for"],
        episodes_wanted: Annotated[int, "the number of episodes to return"],
    ) -> str:

        await self.connection_manager.broadcast_tool_call(
            f"Searching for {episodes_wanted} podcast episodes about {query}"
        )

        vector = await EMBEDDING_GENERATOR.generate_embeddings([query])

        vector = vector.tolist()
        vector = vector[0]

        vector_query = VectorizedQuery(
            vector=vector,
            k_nearest_neighbors=5,
            fields="embedding",
            exhaustive=True,
        )

        i = 0
        unique_results = []
        seen = set()
        while True:
            if i > 10:  # Arbitrary limit to prevent infinite loop
                break

            results = SEARCH_CLIENT.search(
                include_total_count=True,
                search_text=query,
                select=["title", "publish_date", "description"],
                top=episodes_wanted,
                skip=episodes_wanted * i,
                vector_queries=[vector_query],
            )

            for result in results:
                if result["title"] not in seen:
                    unique_results.append(result)
                    seen.add(result["title"])

            if len(unique_results) >= episodes_wanted:
                results_total = unique_results[:episodes_wanted]
                break

            i += 1

            print(f"Iteration {i}")

        results_formatted = [
            f"Podcast episode title: {result['title']}, Description: {result['description']}, Publish Date: {result['publish_date']}"
            for result in results_total
        ]

        return results_formatted
