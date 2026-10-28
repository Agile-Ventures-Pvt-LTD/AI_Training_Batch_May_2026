import re
import os
import logging
from mcp_use import MCPClient, MCPAgent
from src.llm import call_llm
from prompts import SYSTEM_PROMPT


WRITE_TOOLS = {
    "add_issue_comment",
    "update_issue_status"
}


class ToolTracker(logging.Handler):
    def __init__(self):
        super().__init__()
        self.tools = []

    def emit(self, record):
        message = record.getMessage()

        match = re.search(r"Tool call:\s*([a-zA-Z0-9_]+)", message)

        if match:
            self.tools.append(match.group(1))

    def clear(self):
        self.tools = []

class MCPHost:
    def __init__(self):
        self.client = MCPClient(os.path.join(os.path.dirname(__file__),"mcp.json"))

        self.llm = call_llm()

        self.agent = MCPAgent(
            llm=self.llm,
            client=self.client,
            max_steps=30,
            use_server_manager=False,
            system_prompt=SYSTEM_PROMPT
        )

        self.tool_tracker = ToolTracker()

        logging.getLogger(
            "mcp_use.agents.display"
        ).addHandler(
            self.tool_tracker
        )


    async def run(self, query: str):
        self.tool_tracker.clear()
    
        response = await self.agent.run(query)

        tools_used = list(set(self.tool_tracker.tools))
        write_action_performed = any(tool in WRITE_TOOLS for tool in tools_used)

        return {
            "user_query": query.strip(),
            "tools_used": tools_used,
            "final_answer": str(response),
            "write_action_performed": write_action_performed
        }


host = MCPHost()