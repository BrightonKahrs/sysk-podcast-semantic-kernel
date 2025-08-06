from semantic_kernel.functions import KernelParameterMetadata, KernelPlugin

from backend.data_collections.podcast_collection import podcast_collection
                                     
                                     
azure_ai_search_plugin = KernelPlugin(
    name="azure_ai_search",
    description="Searches against Azure AI Search to learn about podcast episode information",
    functions=[
        podcast_collection.create_search_function(
            function_name="search_podcast_transcripts",
            description="Get general information about podcast episodes and their trancscripts based on a query",
            search_type="vector",
            parameters=[
                KernelParameterMetadata(
                    name="query",
                    description="What to search for.",
                    type="str",
                    is_required=True,
                    type_object=str,
                ),
                KernelParameterMetadata(
                    name="top",
                    description="Number of results to return.",
                    type="int",
                    default_value=5,
                    type_object=int,
                ),
            ],
            string_mapper=lambda x: f'Podcast episode title: {x.record.title}, Description: {x.record.description}, Publish Date: {x.record.publish_date}, Transcript: {x.record.transcript}'
        )
    ]
)