import asyncio
import sys
from pathlib import Path
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from mcp_use import MCPAgent, MCPClient

sys.path.append(str(Path(__file__).resolve().parent.parent))
from src.config import SERVER_CONFIGS, GROQ_MODEL, GROQ_API_KEY
from src.prompts import SYSTEM_PROMPT
from src.output_writer import save_query_result
from src.tool_discovery import generate_discovery


class EvidenceModel(BaseModel):
    services: List[Dict[str, Any]] = Field(default_factory=list)
    incidents: List[Dict[str, Any]] = Field(default_factory=list)
    tickets: List[Dict[str, Any]] = Field(default_factory=list)
    changes: List[Dict[str, Any]] = Field(default_factory=list)


class StructuredOpsResponse(BaseModel):
    user_query: str
    servers_used: List[str]
    tools_used: List[str]
    evidence: EvidenceModel
    operations_summary: str
    possible_change_correlation: str
    recommended_next_actions: List[str]
    limitations: List[str]


async def handle_operations_query(query: str, query_id: str = "CLI") -> StructuredOpsResponse:
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY environment variable is missing.")

    llm = ChatGroq(model=GROQ_MODEL, temperature=0, api_key=GROQ_API_KEY)
    structured_llm = llm.with_structured_output(StructuredOpsResponse)
    
    client = MCPClient.from_dict(SERVER_CONFIGS)

    agent = MCPAgent(
        llm=llm,
        client=client,
        max_steps=10,
        system_prompt=SYSTEM_PROMPT,
        use_server_manager=False
    )

    raw_response = await agent.run(query)

    formatting_prompt = (
        f"You are formatting an investigation summary. Convert the findings into the exact schema.\n\n"
        f"User Query: {query}\n\n"
        f"Investigation Findings & Tool Evidence:\n{raw_response}"
    )
    
    structured_output: StructuredOpsResponse = await structured_llm.ainvoke(formatting_prompt)
    
    save_query_result(structured_output.model_dump())

    return structured_output


async def main():
    print("--- Executing MCP Server Discovery Process ---")
    await generate_discovery()

    print("\nEnterprise Operations Assistant (Type 'exit' to quit)")
    while True:
        try:
            query = input("\nEnter operations inquiry: ").strip()
            if not query or query.lower() == "exit":
                break
            print("Orchestrating multi-server investigation data flow...")
            response_obj = await handle_operations_query(query)
            print(f"\n[Investigation Summary]\n{response_obj.operations_summary}")
        except Exception as err:
            print(f"Error handling query: {err}")


if __name__ == "__main__":
    asyncio.run(main())
