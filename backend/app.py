from typing import Dict, List, Set
from dotenv import load_dotenv
import os
  
import uvicorn  
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from opentelemetry.instrumentation.openai_v2 import OpenAIInstrumentor
from azure.ai.projects import AIProjectClient
from azure.identity import ClientSecretCredential
from azure.monitor.opentelemetry import configure_azure_monitor

from backend.utils.connection_manager import connection_manager
from backend.utils.state_store import get_state_store
from backend.agents.rag_agent import RagAgent  # Import the RagAgent class
  
#Setup from environment
load_dotenv()  # read .env if present  


# Set up telemetry - requires an AZ login via Service Principal
OpenAIInstrumentor().instrument()

client_id = os.getenv('AZURE_CLIENT_ID')
client_secret = os.getenv('AZURE_CLIENT_SECRET')
tenant_id = os.getenv('AZURE_TENANT_ID')
endpoint = os.getenv('AZURE_AI_FOUNDRY_ENDPOINT')

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
STATE_STORE = get_state_store()  # either dict or CosmosDBStateStore  
  
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


@app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connection_manager.add(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        connection_manager.remove(websocket)
  
  
@app.post("/chat", response_model=ChatResponse)  
async def chat(req: ChatRequest):  
    agent = RagAgent(STATE_STORE, req.session_id)  
    answer = await agent.chat_async(req.prompt)  
    return ChatResponse(response=answer)  
  
  
@app.post("/reset_session")  
async def reset_session(req: SessionResetRequest):  
    if req.session_id in STATE_STORE:  
        del STATE_STORE[req.session_id]  
    hist_key = f"{req.session_id}_chat_history"  
    if hist_key in STATE_STORE:  
        del STATE_STORE[hist_key]  
  
  
@app.get("/history/{session_id}", response_model=ConversationHistoryResponse)  
async def get_conversation_history(session_id: str):  
    history = STATE_STORE.get(f"{session_id}_chat_history", [])  
    return ConversationHistoryResponse(session_id=session_id, history=history)  
  
  
if __name__ == "__main__":  
    uvicorn.run(app, host="0.0.0.0", port=7000)  