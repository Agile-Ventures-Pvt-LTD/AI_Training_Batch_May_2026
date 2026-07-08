from langchain_groq import ChatGroq
from mcp_use import MCPAgent, MCPClient
from src.prompts import SYSTEM_PROMPT
from src.config import GROQ_API_KEY,GROQ_MODEL,MCP_SERVER_CONFIG
from src.tool_discovery import discover_tools
from src.output_writer import write_mandatory_results, write_sample_runs
import re
import json 
import asyncio
import sys
from typing import Dict, Any
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"

class OperationsHost:
    def __init__(self):
        if not GROQ_API_KEY:
            raise ValueError("GROQ API KEY must be set in environment variable")
        
        self.llm = ChatGroq(model=GROQ_MODEL,groq_api_key=GROQ_API_KEY,temperature=0)

        self.client = MCPClient(MCP_SERVER_CONFIG)
        self.agent = MCPAgent(llm=self.llm,client=self.client,max_steps=10,system_prompt=SYSTEM_PROMPT)

    async def process_query(self, query: str) -> Dict[str, Any]:
        try:
            response_text = await self.agent.run(query)
            return self.parse_response(response_text, query)
        except Exception as e:
            return {
                "user_query": query,
                "error": str(e),
                "status": "FAIL"
            }

    def parse_response(self, response_text: str, original_query: str) -> Dict[str, Any]: 
        try:
            response_data = json.loads(response_text)
        except json.JSONDecodeError:
            response_data = {
                "user_query": original_query,
                "operations_summary": response_text,
                "servers_used": [],
                "tools_used": [],
                "status": "PASS"
            }
        summary_content = response_data.get("operations_summary", "")
        if isinstance(summary_content, str) and "```json" in summary_content:
            try:
                match = re.search(r"```json\s*(.*?)\s*```", summary_content, re.DOTALL)
                if match:
                    inner_json_str = match.group(1)
                    inner_data = json.loads(inner_json_str)
                    
                    if isinstance(inner_data, dict):
                        response_data.update(inner_data)
            except Exception:
                pass

        if "user_query" not in response_data or not response_data["user_query"]:
            response_data["user_query"] = original_query
        response_data["status"] = "PASS"
        if "tool_used" in response_data and "tools_used" not in response_data:
            response_data["tools_used"] = response_data.pop("tool_used")
        return response_data

    async def close(self):
        await self.client.close_all_sessions()

async def run_cli():
    host = OperationsHost()
    print("Enterprise Operations Assistant")
    print("Connected MCP Servers:")
    for name in MCP_SERVER_CONFIG["mcpServers"].keys():
        print(f"- {name}")
    
    print("\nEnter your question (or 'exit' to quit):")
    while True:
        query = input("> ")
        if query.lower() == 'exit':
            break
        print("Processing...")
        result = await host.process_query(query)
        print("\nResult:")
        print(json.dumps(result, indent=2))

        write_mandatory_results([result])
        # write_sample_runs([result])
        print("\n")
        
    await host.close()

async def run_mandatory_queries():
    host = OperationsHost()
    await discover_tools()
    
    with open(DATA_DIR / "sample_queries.json", "r") as f:
        data = json.load(f)
    if isinstance(data, dict) and "mandatory_queries" in data:
        queries = data["mandatory_queries"]
    elif isinstance(data, list):
        queries = data
    else:
        queries = []
    results = []
    for q in queries:
        if not isinstance(q, dict):
            continue
        query_text = q.get("query", "")
        query_id = q.get("id", "Query")
        if not query_text.strip():
            continue  
        print(f"Processing {query_id}: {query_text}")
        result = await host.process_query(query_text)
        result["query_id"] = query_id
        results.append(result)
        
    # write_mandatory_results(results)
    write_sample_runs(results) 
    await host.close()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--run-mandatory":
        asyncio.run(run_mandatory_queries())
    else:
        asyncio.run(run_cli())
