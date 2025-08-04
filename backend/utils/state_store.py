from __future__ import annotations  
  
import os  
import logging 
from typing import Any, Dict, Iterator, List, Optional  
  
# ---------------------------------------------------------------------------  
# 3rd-party SDKs  
# ---------------------------------------------------------------------------  
  
from azure.cosmos import CosmosClient, PartitionKey, exceptions as cosmos_exceptions
from azure.identity import ClientSecretCredential, DefaultAzureCredential
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

from backend.agents.title_summarizer_agent import TitleSummarizerAgent
  
# ---------------------------------------------------------------------------  
# Cosmos-backed implementation  
# ---------------------------------------------------------------------------  
class CosmosDBStateStore():  
    """  
    Dict-like wrapper around a Cosmos DB container whose hierarchical  
    partition key is (tenant_id, id).  
  
    Keys   -> session_id  
    Values -> arbitrary JSON-serialisable python objects  
    """  
  
    def __init__(self) -> None:  
        if CosmosClient is None:  
            raise RuntimeError("azure-cosmos is not installed")  
  
        endpoint = os.getenv("COSMOSDB_ENDPOINT")
        if not endpoint:  
            raise RuntimeError("COSMOSDB_ENDPOINT must be defined")  
  
        # Data-level tenant (NOT the AAD tenant used for auth)  
        self.tenant_id: str = os.getenv("DATA_AZURE_TENANT_ID", "default")
        # self.user_id = "1111-1111-1111-1111"
  
        self.client = CosmosClient(endpoint, credential=self._create_credential())  
  
        db_name = (  
            os.getenv("COSMOSDB_DB_NAME")  
            or os.getenv("COSMOS_DB_NAME")  
            or "ai_state_db"  
        )  
        container_name = (  
            os.getenv("COSMOSDB_CONTAINER_NAME")  
            or os.getenv("COSMOS_CONTAINER_NAME")  
            or "state_store"  
        )  
  
        # Partition key: /tenant_id  +  /id  
        pk = PartitionKey(path=["/tenant_id", "/user_id", "/id"], kind="MultiHash")  
  
        self.database = self.client.create_database_if_not_exists(id=db_name)  
        self.container = self.database.create_container_if_not_exists(  
            id=container_name,  
            partition_key=pk,  
        )  
  
    # ------------------------- authentication helpers -------------------------  
    def _create_credential(self):  
        key = os.getenv("COSMOSDB_KEY")
        if key:  
            logging.info("CosmosDBStateStore: authenticating with KEY")  
            return key.strip('"')
  
        c_id, c_secret, t_id = (  
            os.getenv("CLIENT_ID"),  
            os.getenv("CLIENT_SECRET"),  
            os.getenv("TENANT_ID"),  
        )  
        if c_id and c_secret and t_id:  
            if ClientSecretCredential is None:  
                raise RuntimeError("azure-identity is not installed")  
            logging.info("CosmosDBStateStore: authenticating with AAD client-secret")  
            return ClientSecretCredential(  
                tenant_id=t_id, client_id=c_id, client_secret=c_secret  
            )  
  
        if DefaultAzureCredential is None:  
            raise RuntimeError(  
                "No Cosmos key or AAD creds found, and azure-identity is missing."  
            )  
        logging.info("CosmosDBStateStore: authenticating with DefaultAzureCredential")  
        return DefaultAzureCredential(exclude_interactive_browser_credential=True)
    
    # def _update_user_id(self, user_id: str):  
    #     self.user_id = user_id
  
    # ------------------------- internal helpers -------------------------  
    def _read(self, user_id: str, session_id: str) -> Optional[Dict[str, Any]]:  
        try:  
            return self.container.read_item(  
                item=session_id,  
                partition_key=[self.tenant_id, user_id, session_id],  
            )  
        except cosmos_exceptions.CosmosResourceNotFoundError:  
            return None  
  
    # ------------------------- MutableMapping API -------------------------  
    def get(self, user_id: str, session_id: str, default: Any = None) -> Any:  
        doc = self._read(user_id, session_id)  
        return default if doc is None else doc["value"]  

    async def set(self, user_id: str, session_id: str, value: Any) -> None:  
        existing = self._read(user_id, session_id)

        item = {
            'id': session_id,
            'tenant_id': self.tenant_id,
            'user_id': user_id,
            'value': value
        }

        # Preserve title if it exists and save from a slow AOAI summary
        if existing and 'title' in existing:
            logging.info('TITLE FOUND: NOT SUMMARIZING CONTENT')
            item['title'] = existing['title']
        elif '_chat_history' in session_id:
            logging.info('SUMMARIZING CHAT HISTORY CONTENT')
            item['title'] = await self._summarize_session(value)
        else:
            logging.info('ONLY WILL SUMMARIZE CHAT HISTORY CONTENT')

        self.container.upsert_item(item) 

    async def _summarize_session(self, session: str) -> str:
        summarizer_agent = TitleSummarizerAgent()
        response = await summarizer_agent.summarize_content(session)
        return response

  
    def delete_session(self, user_id: str, session_id: str) -> None:  
        try:  
            self.container.delete_item(  
                item=session_id,  
                partition_key=[self.tenant_id, user_id, session_id],  
            )  
        except cosmos_exceptions.CosmosResourceNotFoundError:  
            raise KeyError(session_id)  
  
    def list_session_ids(self, user_id: str) -> Iterator[str]:  
        query = """
            SELECT 
                c.id as session_id, 
                c.title as session_title 
            FROM c 
            WHERE 
                c.tenant_id = @tid 
                AND c.user_id = @uid
                AND CONTAINS (c.id, '_chat_history')
            """  
        for doc in self.container.query_items(  
            query=query,  
            parameters=[
                {"name": "@tid", "value": self.tenant_id},
                {"name": "@uid", "value": user_id},
                ],  
            enable_cross_partition_query=True,  
        ):  
        
            yield doc['session_id'], doc['session_title']
  
    def count_session_ids(self, user_id: str) -> int:  
        query = "SELECT VALUE COUNT(1) FROM c WHERE c.tenant_id = @tid AND c.user_id = @uid"  
        res: List[int] = list(  
            self.container.query_items(  
                query=query,  
                 parameters=[
                    {"name": "@tid", "value": self.tenant_id},
                    {"name": "@uid", "value": user_id},
                ],   
                enable_cross_partition_query=True,  
            )  
        )  
        return res[0] if res else 0  
  
  
# ---------------------------------------------------------------------------  
# public factory  
# ---------------------------------------------------------------------------  
def get_state_store() -> Dict[str, Any] | CosmosDBStateStore:  
    """  
    Return a CosmosDBStateStore if Cosmos configuration exists, else a dict.  
    """  
    have_endpoint = os.getenv("COSMOSDB_ENDPOINT")
    have_aad = (  
        os.getenv("AZURE_CLIENT_ID")  
        and os.getenv("AZURE_CLIENT_SECRET")  
        and os.getenv("AZURE_TENANT_ID")  
    )  
  
    if have_endpoint and have_aad:  
        logging.info("Using Cosmos DB state store (tenant_id + id partition)")  
        return CosmosDBStateStore()  
  
    logging.info("Cosmos DB config absent → using in-memory dict")  
    return {}  # fallback