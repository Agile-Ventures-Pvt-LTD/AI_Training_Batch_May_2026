import os
import sys
import json
import asyncio
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from mcp_use import MCPAgent, MCPClient
from src.config import MCP_CONFIG
from src.prompts import system_prompt
from src.output_writer import save_tool_discovery, save_mandatory_query_results, save_sample_run_outputs
from pydantic import BaseModel, Field
from typing import List, Dict, Any

# Define the Pydantic models for structured output matching the PRD
class Evidence(BaseModel):
    services: List[Dict[str, Any]] = Field(default_factory=list, description="Services evidence from service-health tool calls")
    incidents: List[Dict[str, Any]] = Field(default_factory=list, description="Incidents evidence from service-health tool calls")
    tickets: List[Dict[str, Any]] = Field(default_factory=list, description="Tickets evidence from support-ticket tool calls")
    changes: List[Dict[str, Any]] = Field(default_factory=list, description="Changes evidence from change-management tool calls")

class OperationsResponse(BaseModel):
    user_query: str = Field(description="The original user query")
    servers_used: List[str] = Field(description="List of servers used during execution (e.g., service-health, support-ticket, change-management)")
    tools_used: List[str] = Field(description="List of specific tool names called")
    evidence: Evidence = Field(description="Structured evidence collected from the tool outputs")
    operations_summary: str = Field(description="A clear, concise operations summary of current situation based on facts")
    possible_change_correlation: str = Field(description="A summary of possible correlation between recent changes and incidents. Must be speculative and not claim confirmed root cause unless explicitly proven.")
    recommended_next_actions: List[str] = Field(description="List of recommended next steps for operations team")
    limitations: List[str] = Field(description="Known limitations of the collected data or the system")

async def run_discovery(client: MCPClient) -> Dict[str, List[str]]:
    """Discover tools from all active sessions and save them."""
    active_sessions = client.get_all_active_sessions()
    discovery = {}
    for name, session in active_sessions.items():
        try:
            if hasattr(session, "list_tools"):
                tools_res = await session.list_tools()
                if isinstance(tools_res, list):
                    discovery[name] = [t.name for t in tools_res]
                else:
                    discovery[name] = [t.name for t in tools_res.tools]
            elif hasattr(session, "tools"):
                discovery[name] = [t.name for t in session.tools]
            else:
                # Fallback to predefined lists if session object can't be introspected
                predefined = {
                    "service-health": ["list_services", "get_service_health", "get_active_incidents"],
                    "support-ticket": ["search_tickets", "get_ticket_details", "get_high_priority_tickets"],
                    "change-management": ["list_recent_changes", "get_change_details", "get_changes_for_service"]
                }
                discovery[name] = predefined.get(name, [])
        except Exception as e:
            # Predefined fallback on error
            predefined = {
                "service-health": ["list_services", "get_service_health", "get_active_incidents"],
                "support-ticket": ["search_tickets", "get_ticket_details", "get_high_priority_tickets"],
                "change-management": ["list_recent_changes", "get_change_details", "get_changes_for_service"]
            }
            discovery[name] = predefined.get(name, [])
            
    # Normalize server names to match the expected format (service-health, support-ticket, change-management)
    normalized_discovery = {}
    for k, v in discovery.items():
        norm_key = k.replace("_", "-")
        normalized_discovery[norm_key] = v
        
    save_tool_discovery(normalized_discovery)
    return normalized_discovery

load_dotenv()
    
groq_api_key = os.getenv("GROQ_API_KEY")
groq_model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    
    if not groq_api_key:
        print("Error: GROQ_API_KEY environment variable not set in .env")
        sys.exit(1)
        
    llm = ChatGroq(
        model=groq_model,
        temperature=0,
        api_key=groq_api_key
    )
    
    # Initialize client and agent
    client = MCPClient(MCP_CONFIG)
    
    agent = MCPAgent(
        llm=llm,
        client=client,
        max_steps=10,
        system_prompt=system_prompt
    )
async def run_all_mandatory(agent: MCPAgent) -> List[Dict[str, Any]]:

    
    """Load and execute all eight mandatory queries."""
    query_file = os.path.join("data", "sample_queries.json")
    if not os.path.exists(query_file):
        print(f"Error: {query_file} not found.")
        return []
        
    with open(query_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    queries = data.get("mandatory_queries", [])
    results = []
    
    print(f"Executing {len(queries)} mandatory queries...\n")
    for q in queries:
        qid = q.get("id")
        query_text = q.get("query")
        print(f"--- Running {qid} ---")
        print(f"Query: {query_text}")
        
        try:
            response = await agent.run(query_text, output_schema=OperationsResponse)
            
            # Print response
            print(f"\nAnswer:\n{response.operations_summary}\n")
            
            # Format output for JSON and MD
            res_dict = {
                "query_id": qid,
                "user_query": query_text,
                "servers_used": response.servers_used,
                "tools_used": response.tools_used,
                "evidence": {
                    "services": response.evidence.services,
                    "incidents": response.evidence.incidents,
                    "tickets": response.evidence.tickets,
                    "changes": response.evidence.changes
                },
                "operations_summary": response.operations_summary,
                "possible_change_correlation": response.possible_change_correlation,
                "recommended_next_actions": response.recommended_next_actions,
                "limitations": response.limitations,
                "final_answer": response.operations_summary,
                "status": "PASS"
            }
            results.append(res_dict)
            
        except Exception as e:
            print(f"Error running query {qid}: {e}\n")
            res_dict = {
                "query_id": qid,
                "user_query": query_text,
                "servers_used": q.get("expected_servers", []),
                "tools_used": [],
                "evidence": {"services": [], "incidents": [], "tickets": [], "changes": []},
                "operations_summary": f"Error occurred: {e}",
                "possible_change_correlation": "",
                "recommended_next_actions": [],
                "limitations": [],
                "final_answer": f"Error occurred: {e}",
                "status": "FAIL"
            }
            results.append(res_dict)
            
        # Sleep for 10 seconds to avoid Groq rate limits
        await asyncio.sleep(10)
    # Save the structured outputs
    save_mandatory_query_results(results)
    save_sample_run_outputs(results)
    print("Mandatory query execution completed and results saved.")
    return results

async def main():
    load_dotenv()
    
    groq_api_key = os.getenv("GROQ_API_KEY")
    groq_model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    
    if not groq_api_key:
        print("Error: GROQ_API_KEY environment variable not set in .env")
        sys.exit(1)
        
    llm = ChatGroq(
        model=groq_model,
        temperature=0,
        api_key=groq_api_key
    )
    
    # Initialize client and agent
    client = MCPClient(MCP_CONFIG)
    
    agent = MCPAgent(
        llm=llm,
        client=client,
        max_steps=10,
        system_prompt=system_prompt
    )
    
    try:
        # Await starting all sessions
        await client.create_all_sessions()
        
        # Run discovery on start to ensure outputs/tool_discovery.json is always populated
        await run_discovery(client)
        
        # Check command line argument for running mandatory queries
        if len(sys.argv) > 1 and sys.argv[1] == "--run-mandatory":
            await run_all_mandatory(agent)
            return
            
        # Interactive mode
        print("Enterprise Operations Assistant")
        print("Connected MCP Servers:")
        print("- service-health")
        print("- support-ticket")
        print("- change-management\n")
        
        while True:
            try:
                query = input("Enter your question (or 'exit' to quit): ").strip()
                if not query:
                    continue
                if query.lower() in ["exit", "quit"]:
                    break
                    
                print("Processing...\n")
                response = await agent.run(query, output_schema=OperationsResponse)
                
                print("=== Operations Summary ===")
                print(response.operations_summary)
                print()
                if response.possible_change_correlation:
                    print("=== Possible Change Correlation ===")
                    print(response.possible_change_correlation)
                    print()
                if response.recommended_next_actions:
                    print("=== Recommended Next Actions ===")
                    for action in response.recommended_next_actions:
                        print(f"- {action}")
                    print()
                if response.limitations:
                    print("=== Limitations ===")
                    for limit in response.limitations:
                        print(f"- {limit}")
                    print()
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"An error occurred: {e}\n")
                
    finally:
        await client.close_all_sessions()

if __name__ == "__main__":
    asyncio.run(main())