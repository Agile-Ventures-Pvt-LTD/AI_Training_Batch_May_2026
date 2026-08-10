from mcp_use import MCPAgent, MCPClient
from llm import get_llm
from prompts import system_prompt
from pathlib import Path


try:
    PARENT_DIR = Path(__file__).resolve().parent
except NameError:
    PARENT_DIR = Path.cwd()

server_file = PARENT_DIR.parent / "server" / "jira_mcp_server.py"


config = MCPClient({
    "mcpServers": {
        "weather": {
            "command": "python",
            "args": [
                str(server_file)
            ]
        }
    }
})


mcp_agent = MCPAgent(
    llm = get_llm(),
    client = config,
    max_steps = 30,
    system_prompt = system_prompt

)









