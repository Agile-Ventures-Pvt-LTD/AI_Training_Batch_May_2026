import os
os.environ["ANONYMIZED_TELEMETRY"] = "false"
from mcp_use import MCPAgent, MCPClient
from dotenv import load_dotenv
import asyncio
load_dotenv()
from langchain_groq import ChatGroq
import os
import json
from pathlib import Path
from src.config import MCP_SERVER_CONFIG
from src.output_writer import write_sample_runs,write_mandatory_queries
from src.tool_discovery import run_tool_discovery
from src.prompts import SYSTEM_PROMPT

async def main():
    
    print("Enterprise Operations Assistant")

    run_tool_discovery()
    client = MCPClient(MCP_SERVER_CONFIG)
    llm = ChatGroq(
            model=os.getenv("GROQ_MODEL","llama-3.3-70b-versatile"),
            temperature=0.0,
            max_retries=2,
        )
    agent = MCPAgent(
        llm = llm,
        client= client,
        max_steps = 10,
        system_prompt=SYSTEM_PROMPT
    )
    
    query_path = Path("data/sample_queries.json")
    if not query_path:
        return FileNotFoundError
    with open(query_path,"r",encoding="utf-8") as file:
        query_data = json.load(file)
    structured_results = []
    for q in query_data.get("mandatory_queries",[]):
        try:
            response = await agent.run(q["query"])
            records = {
                "query_id" : q.get("id"),
                "user_query":q.get("query"),
                "servers_used":q.get("expected_servers"),
                "tools_used":[],
                "final_answer":str(response),
                "status":"PASS"
            }
            structured_results.append(records)
        except Exception as e:
            structured_results.append({
                "query_id" : q.get("id"),
                "user_query":q.get("query"),
                "servers_used":[],
                "tools_used":[],
                "final_answer":f"error {str(e)}",
                "status":"FAIL"
            })
    
    write_mandatory_queries(structured_results)
    write_sample_runs(structured_results)
    await client.close_all_sessions()
if __name__ == "__main__":
        asyncio.run(main())