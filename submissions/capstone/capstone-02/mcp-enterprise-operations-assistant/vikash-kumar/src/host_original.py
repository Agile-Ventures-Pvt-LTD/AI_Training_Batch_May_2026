import os
import sys
import asyncio
from typing import List, Dict, Any
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import tool

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.config import OrchestratorConfig
from src.output_writer import save_json_artifact, save_markdown_summary

from servers.service_health_server import check_service_metrics, get_degraded_services
from servers.support_ticket_server import fetch_high_impact_incidents, find_tickets_by_service
from servers.change_management_server import get_recent_deployments

@tool
def call_service_health_metrics(service_name: str) -> str:
    """Retrieve telemetry health status, error rates, and metrics for a specific internal service module."""
    return check_service_metrics(service_name)

@tool
def call_get_degraded_services() -> str:
    """Scan infrastructure to identify all microservice nodes reporting degraded telemetry behaviors."""
    return get_degraded_services()

@tool
def call_fetch_high_impact_incidents() -> str:
    """Query active support ticket ledgers for incidents flagged with severe customer business impacts."""
    return fetch_high_impact_incidents()

@tool
def call_find_tickets_by_service(service_name: str) -> str:
    """Retrieve support ticket incident backlogs mapped explicitly to an internal application service."""
    return find_tickets_by_service(service_name)

@tool
def call_get_recent_deployments(service_name: str) -> str:
    """Query change management manifests for configuration rollouts and release changes affecting a specific service."""
    return get_recent_deployments(service_name)

TOOLS_MAPPING = {
    "call_service_health_metrics": call_service_health_metrics,
    "call_get_degraded_services": call_get_degraded_services,
    "call_fetch_high_impact_incidents": call_fetch_high_impact_incidents,
    "call_find_tickets_by_service": call_find_tickets_by_service,
    "call_get_recent_deployments": call_get_recent_deployments
}

class MCPOperationsOrchestrator:
    def __init__(self):
        OrchestratorConfig.validate()
        self.llm = ChatGroq(
            api_key=OrchestratorConfig.GROQ_API_KEY, 
            model_name="llama-3.3-70b-versatile",
            temperature=0.0
        )
        self.tools_list = list(TOOLS_MAPPING.values())
        self.model_with_tools = self.llm.bind_tools(self.tools_list)
        
    def execute_workflow(self, user_query: str) -> Dict[str, Any]:
        system_prompt = (
            "You are an expert enterprise Site Reliability Operations Host. Your task is to diagnose platform failures.\n"
            "Review available tools from your MCP Client and call them to collect system logs or health state evidence.\n"
            "If a question requires multiple servers (e.g., checking health and looking up changes), call tools sequentially.\n"
            "Combine all structural evidence transparently to generate a final troubleshooting answer. Do not guess parameters."
        )
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_query)
        ]
        
        tools_called = []
        max_loops = 5  
        
        for _ in range(max_loops):
            response = self.model_with_tools.invoke(messages)
            messages.append(response)
            
            if not response.tool_calls:
                break
                
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                tools_called.append(tool_name)
                
                target_tool = TOOLS_MAPPING[tool_name]
                tool_result = target_tool.invoke(tool_args)
                
                messages.append(ToolMessage(content=str(tool_result), tool_call_id=tool_call["id"]))
        
        final_answer = messages[-1].content
        return {
            "query": user_query,
            "tool_used": ", ".join(tools_called) if tools_called else "None",
            "result": final_answer
        }

def start_interactive_cli():
    print("Enterprise Operations Assistant")
    print("Connected MCP Servers:")
    print("- service-health")
    print("- support-ticket")
    print("- change-management")
    print("Enter your question (type 'exit' to quit):")
    print("35")
    
    try:
        orchestrator = MCPOperationsOrchestrator()
    except Exception as e:
        print(f"Initialization Error: {e}")
        return

    execution_history = []
    
    while True:
        try:
            user_input = input("> ").strip()
        except (KeyboardInterrupt, EOFError):
            break
            
        if not user_input:
            continue
        if user_input.lower() == "exit":
            break
            
        print("Processing...")
        try:
            record = orchestrator.execute_workflow(user_input)
            execution_history.append(record)
            print(f"\n{record['result']}\n")
            
            save_json_artifact(OrchestratorConfig.OUTPUTS_DIR, "mandatory_query_results.json", execution_history)
            save_markdown_summary(OrchestratorConfig.OUTPUTS_DIR, "sample_run_outputs.md", execution_history)
        except Exception as e:
            print(f"Execution Error: {e}\n")

if __name__ == "__main__":
    start_interactive_cli()
