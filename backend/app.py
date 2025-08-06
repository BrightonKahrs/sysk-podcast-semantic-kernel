from typing import Dict, List, Set, Annotated, Any, Union
from dotenv import load_dotenv
import os
import logging

import uvicorn
from fastapi import (
    FastAPI,
    WebSocket,
    WebSocketDisconnect,
    Request,
    HTTPException,
    Depends,
)
from pydantic import BaseModel
from opentelemetry.instrumentation.openai_v2 import OpenAIInstrumentor
from azure.ai.projects import AIProjectClient
from azure.identity import ClientSecretCredential
from azure.monitor.opentelemetry import configure_azure_monitor

from backend.utils.connection_manager import (
    get_connection_manager,
    ConnectionManager,
)
from backend.utils.state_store import get_state_store, StateStore
from backend.agents.rag_agent import RagAgent

state_store_dependency = Annotated[StateStore, Depends(get_state_store)]

connection_manager_dependency = Annotated[
    ConnectionManager, Depends(get_connection_manager)
]

# Set up logging
logging.basicConfig(
    level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Suppress uvicorn logs
logging.getLogger("uvicorn.access").setLevel(logging.CRITICAL)
logging.getLogger("uvicorn").setLevel(logging.ERROR)

# Suppress Azure SDK logs
logging.getLogger("azure.core.pipeline").setLevel(logging.CRITICAL)

# Suppress Application Insights telemetry logs
logging.getLogger("opencensus").setLevel(logging.CRITICAL)
logging.getLogger("opencensus.trace").setLevel(logging.CRITICAL)
logging.getLogger("opencensus.ext.azure.common.transport").setLevel(logging.CRITICAL)
logging.getLogger("opencensus.ext.azure.common").setLevel(logging.CRITICAL)

# Setup from environment
load_dotenv()  # read .env if present


# Set up telemetry - requires an AZ login via Service Principal
OpenAIInstrumentor().instrument()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
tenant_id = os.getenv("TENANT_ID")
endpoint = os.getenv("AZURE_AI_FOUNDRY_ENDPOINT")

credential = ClientSecretCredential(
    tenant_id=tenant_id,
    client_id=client_id,
    client_secret=client_secret,
)

project_client = AIProjectClient(
    credential=credential,
    endpoint=endpoint,
)

connection_string = project_client.telemetry.get_connection_string()
configure_azure_monitor(connection_string=connection_string)

# Store active WebSocket connections
active_connections: Set[WebSocket] = set()

# Set conversation state history
# STATE_STORE = get_state_store()  # either dict or CosmosDBStateStore

# Setup FastAPI App
app = FastAPI()


class ChatRequest(BaseModel):
    session_id: str
    prompt: str


class ChatResponse(BaseModel):
    response: str


class ConversationHistoryResponse(BaseModel):
    session_id: str
    history: List[Dict[str, str]]


class SessionResetRequest(BaseModel):
    session_id: str


class ConversationHistoryId(BaseModel):
    session_id: str
    title: str


class ConversationHistoryIds(BaseModel):
    session_ids: List[ConversationHistoryId]


@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket, connection_manager: connection_manager_dependency
):
    await websocket.accept()
    connection_manager.add(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        connection_manager.remove(websocket)


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest, request: Request, state_store: state_store_dependency):
    user_id = request.headers.get("X-User-ID")
    agent = RagAgent(state_store, user_id, req.session_id)
    answer = await agent.chat_async(req.prompt)
    return ChatResponse(response=answer)


@app.post("/reset_session")
async def reset_session(req: SessionResetRequest, request: Request):
    user_id = request.headers.get("X-User-ID")
    if not user_id:
        raise HTTPException(status_code=400, detail="Missing user ID")


@app.post("/delete/{session_id}")
async def delete_session(
    session_id: str, request: Request, state_store: state_store_dependency
):
    user_id = request.headers.get("X-User-ID")
    if not user_id:
        raise HTTPException(status_code=400, detail="Missing user ID")

    hist_key = f"{session_id}_chat_history"

    state_store.delete_session(user_id, session_id)
    state_store.delete_session(user_id, hist_key)


@app.get("/history/{session_id}", response_model=ConversationHistoryResponse)
async def get_conversation_history(
    session_id: str, request: Request, state_store: state_store_dependency
):
    user_id = request.headers.get("X-User-ID")
    history = state_store.get(user_id, f"{session_id}_chat_history", [])
    return ConversationHistoryResponse(session_id=session_id, history=history)


@app.get("/history", response_model=ConversationHistoryIds)
async def get_conversation_history(
    request: Request, state_store: state_store_dependency
):
    user_id = request.headers.get("X-User-ID")
    session_ids = list(state_store.list_session_ids(user_id))

    session_ids = [
        ConversationHistoryId(
            session_id=id[0].replace("_chat_history", ""), title=id[1]
        )
        for id in session_ids
    ]

    return ConversationHistoryIds(session_ids=session_ids)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7000)
