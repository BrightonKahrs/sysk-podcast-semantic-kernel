import os  
import logging  
from typing import Any, Dict, List, Optional  
from dotenv import load_dotenv

from functools import wraps

# Configure logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
  
load_dotenv()  # Load environment variables from .env file if needed 

import json
class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'to_dict'):
            return obj.to_dict()
        elif hasattr(obj, '__dict__'):
            return obj.__dict__
        return super().default(obj)

  
class BaseAgent:  
    """  
    Base class for all agents.  
    Not intended to be used directly.  
    Handles environment variables, state store, and chat history.  
    """  
  
    def __init__(self, state_store: Dict[str, Any], session_id: str) -> None:  
        self.azure_deployment = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT")  
        self.azure_openai_key = os.getenv("AZURE_OPENAI_API_KEY")  
        self.azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")  
        self.api_version = os.getenv("AZURE_OPENAI_API_VERSION")
  
        self.session_id = session_id  
        self.state_store = state_store  
  
        self.chat_history: List[Dict[str, str]] = self.state_store.get(f"{session_id}_chat_history", [])  
        self.state: Optional[Any] = self.state_store.get(session_id, None) 
        logging.debug(f"Chat history for session {session_id}: {self.chat_history}")  
  

    def _setstate(self, state: Any) -> None:
        state = json.dumps({'thread': state}, cls=CustomEncoder)
        # state = json.loads(state)
        self.state_store[self.session_id] = state  
  

    def append_to_chat_history(self, messages: List[Dict[str, str]]) -> None:  
        self.chat_history.extend(messages)  
        self.state_store[f"{self.session_id}_chat_history"] = self.chat_history  
  

    async def chat_async(self, prompt: str) -> str:  
        """  
        Override in child class!  
        """  
        raise NotImplementedError("chat_async should be implemented in subclass.")  
    

    def instrument_tool_call(self, func):
        """
        Wrapper method to send tool usage events to the frontend
        """
        @wraps(func)
        async def wrapper(*args, **kwargs):
            tool_name = func.__name__
            logging.debug(f'🔧 Tool called: {tool_name} with args: {kwargs}')
            return await func(*args, **kwargs)
        
        return wrapper