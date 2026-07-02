import os
import json
import logging
from typing import List, Dict, Any, Optional
from groq import Groq
from src.prompts import SYSTEM_PROMPT

logger = logging.getLogger("jira-assistant.llm")

class GroqLLMClient:
    """Wrapper class for interacting with the Groq API for tool calling."""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        # Allow passing key directly or fallback to env
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.model = model or os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        
        # We only check for api_key during execution, not class creation, to allow mock initialization in tests
        self._client = None

    @property
    def client(self) -> Groq:
        if self._client is None:
            if not self.api_key or self.api_key == "your_groq_api_key_here":
                raise ValueError("GROQ_API_KEY is not set or contains the default placeholder. Please configure it in your .env file.")
            self._client = Groq(api_key=self.api_key)
        return self._client

    def convert_mcp_tools_to_groq(self, mcp_tools: List[Any]) -> List[Dict[str, Any]]:
        """Converts MCP tool schemas into Groq-compatible tool definitions."""
        groq_tools = []
        for tool in mcp_tools:
            # Handle tool being either an object with attributes or a dict
            name = getattr(tool, "name", None) or tool.get("name")
            desc = getattr(tool, "description", None) or tool.get("description", "")
            schema = getattr(tool, "inputSchema", None) or tool.get("inputSchema", {})
            
            # Ensure schema conforms to Groq's expectation
            if not schema:
                schema = {
                    "type": "object",
                    "properties": {}
                }
                
            groq_tools.append({
                "type": "function",
                "function": {
                    "name": name,
                    "description": desc,
                    "parameters": schema
                }
            })
        return groq_tools

    def get_chat_response(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None
    ) -> Any:
        """Call Groq chat completions API with the conversation history and optional tools."""
        logger.info(f"Sending request to Groq using model: {self.model}")
        
        # Prepare system message if not already present or ensure alignment
        has_system = any(m.get("role") == "system" for m in messages)
        full_messages = messages.copy()
        if not has_system:
            full_messages.insert(0, {"role": "system", "content": SYSTEM_PROMPT})
            
        kwargs: Dict[str, Any] = {
            "model": self.model,
            "messages": full_messages,
            "temperature": 0.1,  # Low temperature for precise tool usage
        }
        
        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = "auto"
            
        try:
            response = self.client.chat.completions.create(**kwargs)
            return response
        except Exception as e:
            logger.error(f"Groq API call failed: {e}")
            raise RuntimeError(f"Failed to fetch response from Groq LLM: {str(e)}")
