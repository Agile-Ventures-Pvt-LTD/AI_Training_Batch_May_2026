import os
import sys
import asyncio
from typing import List, Dict, Any
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import tool

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.config import Mcp
from src.output_writer import save_json, save_markdown_summary
from src.prompts import SYSTEM_PROMPT
from servers.service_health_server import list_services, get_service_health, get_active_incidents
from servers.support_ticket_server import search_tickets, get_ticket_details, get_high_priority_tickets
from servers.change_management_server import list_recent_changes, get_change_details, get_changes_for_service

@tool
def call_list_services() -> str:
    """This will list all available system service nodes and their current health status."""
    return list_services()

@tool
def call_get_service_health(service_name: str) -> str:
    """It will retrieve health metrics for service."""
    return get_service_health(service_name)

@tool
def call_get_active_incidents(service_name: str = None) -> str:
    """This will return active operational incidents"""
    return get_active_incidents(service_name)

@tool
def call_search_tickets(service_name: str = None, priority: str = None, status: str = None, limit: int = 20) -> str:
    """This will search support tickets"""
    return search_tickets(service_name, priority, status, limit)

@tool
def call_get_ticket_details(ticket_id: str) -> str:
    """This will get full details of ticket"""
    return get_ticket_details(ticket_id)

@tool
def call_get_high_priority_tickets(service_name: str = None) -> str:
    """THis will return high priority tickets"""
    return get_high_priority_tickets(service_name)

@tool
def call_list_recent_changes(limit: int = 10) -> str:
    """It will return recent changes"""
    return list_recent_changes(limit)

@tool
def call_get_change_details(change_id: str) -> str:
    """This will return details of changes occured"""
    return get_change_details(change_id)

@tool
def call_get_changes_for_service(service_name: str) -> str:
    """This will return recent changes mapped to a service name"""
    return get_changes_for_service(service_name)

TOOLS_KIT = {"call_list_services": call_list_services,"call_get_service_health": call_get_service_health,"call_get_active_incidents": call_get_active_incidents,"call_search_tickets": call_search_tickets,"call_get_ticket_details": call_get_ticket_details,"call_get_high_priority_tickets": call_get_high_priority_tickets,"call_list_recent_changes": call_list_recent_changes,"call_get_change_details": call_get_change_details,"call_get_changes_for_service": call_get_changes_for_service}

class MCPOperations:
    def __init__(self):
        Mcp.validate()
        self.llm = ChatGroq(api_key=Mcp.GROQ_API_KEY, model_name="llama-3.1-8b-instant", temperature=0.0)
        self.tools_list = list(TOOLS_KIT.values())
        self.model_with_tools = self.llm.bind_tools(self.tools_list)
        
    def execute_workflow(self, user_query: str) -> Dict[str, Any]:
        messages = [SystemMessage(content=SYSTEM_PROMPT),HumanMessage(content=user_query)]
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
                target_tool = TOOLS_KIT[tool_name]
                tool_result = target_tool.invoke(tool_args)
                
                messages.append(ToolMessage(content=str(tool_result), tool_call_id=tool_call["id"]))
        
        final_answer = messages[-1].content
        return {"query": user_query,"tool_used": ", ".join(tools_called) if tools_called else "None","result": final_answer}

def execution():
    print("Enterprise Operations Assistant")
    print("Connected MCP Servers:")
    print("- service-health")
    print("- support-ticket")
    print("- change-management")
    print("Enter your question (type 'exit' to quit):")
    
    try:
        workflow = MCPOperations()
    except Exception as e:
        print(f"Error occured: {e}")
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
            record = workflow.execute_workflow(user_input)
            execution_history.append(record)
            print(f"\n{record['result']}\n")
            
            save_json(Mcp.OUTPUTS_DIR, "mandatory_query_results.json", execution_history)
            save_markdown_summary(Mcp.OUTPUTS_DIR, "sample_run_outputs.md", execution_history)
        except Exception as e:
            print(f"Execution Error: {e}\n")

if __name__ == "__main__":
    execution()
