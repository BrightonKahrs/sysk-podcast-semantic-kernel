from typing import Annotated

from semantic_kernel.connectors.ai.open_ai import AzureTextEmbedding
from semantic_kernel.data.vector import VectorStoreField, vectorstoremodel
from semantic_kernel.connectors.ai.open_ai import AzureTextEmbedding
from semantic_kernel.kernel_types import OptionalOneOrList
from pydantic import BaseModel
from azure.search.documents.indexes.models import SearchFieldDataType

@vectorstoremodel
class PodcastEpisode(BaseModel):
    id: Annotated[str, VectorStoreField("key")]
    title: Annotated[str, VectorStoreField("data", type=SearchFieldDataType.String)]
    publish_date: Annotated[str, VectorStoreField("data", type=SearchFieldDataType.String)] = None
    description: Annotated[str, VectorStoreField("data", type=SearchFieldDataType.String)] = None
    transcript: Annotated[str, VectorStoreField("data", type=SearchFieldDataType.String, is_full_text_indexed=True)] = None
    embedding: Annotated[list[float], VectorStoreField("vector", dimensions=1536, embedding_generator=AzureTextEmbedding())] = None