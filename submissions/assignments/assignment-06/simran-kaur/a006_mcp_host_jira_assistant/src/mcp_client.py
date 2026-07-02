from mcp_use import MCPAgent, MCPClient
from src.llm import model_llm
from src.prompts import system_prompt
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


host_agent = MCPAgent(
    llm = model_llm,
    client = config,
    max_steps = 30,
    system_prompt = system_prompt

)










