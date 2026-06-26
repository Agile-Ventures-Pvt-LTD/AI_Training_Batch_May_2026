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


test1 = agent.run("I am going for Jaipur travel what are the advice for me?")
test2 = agent.run("What is the weather condition of the Jaipur")
test3 = agent.run("What are the packing item will suggest me to pack while travelling to Jaipur")