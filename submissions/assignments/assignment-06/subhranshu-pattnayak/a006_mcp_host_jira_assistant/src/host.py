"""Jira Issue Assistant MCP Host"""

import asyncio
from typing import Any
from mcp_use import MCPAgent
try:
    from .llm import default_llm
    from .mcp_client import get_client
    from .prompts import SYSTEM_PROMPT
    from .utils import write_output
except ImportError:
    from llm import default_llm
    from mcp_client import get_client
    from prompts import SYSTEM_PROMPT
    from utils import write_output


async def main(
    user_query: str,
    *,
    test: bool = False,
) -> tuple[dict[str, Any], str]:
    """
    Executes user query through the MCP Host.
    """
    
    agent = MCPAgent(
        llm=default_llm,
        client=get_client(),
        system_prompt=SYSTEM_PROMPT,
        max_steps=30,
    )
    
    result = await agent.run(user_query)
    response = str(result)
    output = {
        "user_query": user_query,
        "tools_used": list(set(agent.tools_used_names)),
        "final_answer": response,
        "write_action_performed": any(
            tool in agent.tools_used_names
            for tool in (
                "add_issue_comment",
                "update_issue_status",
            )
        ),
    }
    
    write_output(
        data=output,
        test=test,
    )
    return output, response


if __name__ == "__main__":
    query = input("INPUT  > ").strip()

    output, response = asyncio.run(
        main(query)
    )

    print("\nAssistant Response")
    print("-" * 70)
    print(response)