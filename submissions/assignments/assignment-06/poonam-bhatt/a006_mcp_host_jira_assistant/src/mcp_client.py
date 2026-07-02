import os
import sys
import logging
from typing import List, Dict, Any, Optional
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

logger = logging.getLogger("jira-assistant.mcp-client")

class JiraMCPClient:
    """Handles the subprocess stdio connection to the Jira MCP Server."""
    
    def __init__(self, server_script_path: Optional[str] = None):
        if not server_script_path:
            # Default path relative to workspace root
            self.server_script_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "server", "jira_mcp_server.py")
            )
        else:
            self.server_script_path = os.path.abspath(server_script_path)
            
        self.server_params = StdioServerParameters(
            command=sys.executable,
            args=[self.server_script_path],
            env=os.environ.copy()  # Pass current env (loaded from .env) to the server subprocess
        )
        self._stdio_mgr = None
        self._session = None

    async def connect(self):
        """Establish stdio connection and initialize the session."""
        logger.info(f"Connecting to Jira MCP server at: {self.server_script_path}")
        if not os.path.exists(self.server_script_path):
            raise FileNotFoundError(f"Jira MCP Server script not found at '{self.server_script_path}'")
            
        self._stdio_mgr = stdio_client(self.server_params)
        read, write = await self._stdio_mgr.__aenter__()
        
        self._session = ClientSession(read, write)
        await self._session.__aenter__()
        
        # Initialize connection
        await self._session.initialize()
        logger.info("Successfully connected and initialized Jira MCP Server session.")

    async def disconnect(self):
        """Clean up the session and stdio connection."""
        logger.info("Disconnecting from Jira MCP server...")
        if self._session:
            try:
                await self._session.__aexit__(None, None, None)
            except Exception as e:
                logger.error(f"Error exiting MCP ClientSession: {e}")
            self._session = None
            
        if self._stdio_mgr:
            try:
                await self._stdio_mgr.__aexit__(None, None, None)
            except Exception as e:
                logger.error(f"Error exiting stdio transport manager: {e}")
            self._stdio_mgr = None
        logger.info("MCP server connection cleaned up.")

    async def list_available_tools(self) -> List[Any]:
        """Fetch the tools exposed by the MCP Server."""
        if not self._session:
            raise RuntimeError("MCP client is not connected. Call connect() first.")
        tools_result = await self._session.list_tools()
        return tools_result.tools

    async def call_server_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        """Call a specific tool on the MCP Server."""
        if not self._session:
            raise RuntimeError("MCP client is not connected. Call connect() first.")
        logger.info(f"Executing tool '{name}' with arguments: {arguments}")
        result = await self._session.call_tool(name, arguments)
        return result
