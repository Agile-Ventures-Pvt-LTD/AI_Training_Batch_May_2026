import os
from src.config import llm
from mcp_use import MCPAgent, MCPClient

config = MCPClient(os.path.join(os.path.dirname(__file__), "src/mcp.json"))

agent = MCPAgent(
    llm=llm,
    client=config,
    max_steps=30,
    use_server_manager=False
)


test1 = agent.run("What is the travel Checklist")
test2 = agent.run("What are the weather advisory rule")
test3 = agent.run("Show me the normalised schema of the forecast")