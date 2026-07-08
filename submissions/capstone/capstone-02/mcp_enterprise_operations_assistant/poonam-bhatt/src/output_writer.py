import os
import json
from typing import List, Dict, Any

def save_tool_discovery(discovered_tools: Dict[str, List[str]]):
    """Save the tool discovery JSON to outputs/tool_discovery.json."""
    os.makedirs("outputs", exist_ok=True)
    path = os.path.join("outputs", "tool_discovery.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(discovered_tools, f, indent=2)

def save_mandatory_query_results(results: List[Dict[str, Any]]):
    """Save mandatory query results to outputs/mandatory_query_results.json."""
    os.makedirs("outputs", exist_ok=True)
    path = os.path.join("outputs", "mandatory_query_results.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

def save_sample_run_outputs(results: List[Dict[str, Any]]):
    """Save all query runs to outputs/sample_run_outputs.md in the required markdown format."""
    os.makedirs("outputs", exist_ok=True)
    path = os.path.join("outputs", "sample_run_outputs.md")
    
    with open(path, "w", encoding="utf-8") as f:
        f.write("# Sample Run Outputs\n\n")
        for i, res in enumerate(results, 1):
            query_id = res.get("query_id", f"Q{i}")
            # Map query_id to Title
            titles = {
                "Q1": "Payment API Health and Recent Change",
                "Q2": "High-Priority Tickets for Unhealthy Services",
                "Q3": "Payment API Incident and Support Ticket Impact",
                "Q4": "Checkout Service Degradation and Recent Change",
                "Q5": "Operations Summary of Unhealthy Services, Incidents, and Tickets",
                "Q6": "Recent Changes to Services with Active Incidents",
                "Q7": "Ticket TKT-1001 Details and Related Service Health",
                "Q8": "Payment API Recent Changes and Rollback Availability"
            }
            title = titles.get(query_id, f"Query {i}")
            f.write(f"## {query_id} - {title}\n\n")
            f.write("User Query:\n")
            f.write(f"{res.get('user_query', '')}\n\n")
            
            f.write("Servers Used:\n")
            for server in res.get("servers_used", []):
                f.write(f"- {server}\n")
            f.write("\n")
            
            f.write("Tools Used:\n")
            for tool in res.get("tools_used", []):
                f.write(f"- {tool}\n")
            f.write("\n")
            
            f.write("Final Answer:\n")
            f.write(f"{res.get('final_answer', '')}\n\n")
            if i < len(results):
                f.write("---\n\n")
