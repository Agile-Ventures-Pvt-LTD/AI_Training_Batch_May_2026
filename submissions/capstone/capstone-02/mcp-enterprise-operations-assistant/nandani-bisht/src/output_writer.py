import json
from pathlib import Path
from typing import List, Dict, Any
from pydantic import BaseModel, Field

class Evidence(BaseModel):
    services: List[Dict[str, Any]] = Field(default_factory=list, description="List of service records retrieved.")
    incidents: List[Dict[str, Any]] = Field(default_factory=list, description="List of incident records retrieved.")
    tickets: List[Dict[str, Any]] = Field(default_factory=list, description="List of ticket records retrieved.")
    changes: List[Dict[str, Any]] = Field(default_factory=list, description="List of change records retrieved.")

class OperationsResult(BaseModel):
    user_query: str = Field(description="The exact natural language query.")
    servers_used: List[str] = Field(default_factory=list, description="List of MCP servers queried.")
    tools_used: List[str] = Field(default_factory=list, description="List of MCP tools executed.")
    evidence: Evidence = Field(default_factory=Evidence, description="Raw data collected from MCP tools.")
    operations_summary: str = Field(description="Clear natural language operations summary.")
    possible_change_correlation: str = Field(description="Analysis of potential correlation between recent changes and incidents.")
    recommended_next_actions: List[str] = Field(default_factory=list, description="List of recommended next steps.")
    limitations: List[str] = Field(default_factory=list, description="Limitations of the analysis (e.g. missing logs).")

def get_servers_for_tools(tools: List[str]) -> List[str]:
    """Map tool names to their respective MCP server names."""
    servers = set()
    for t in tools:
        if t in ("list_services", "get_service_health", "get_active_incidents"):
            servers.add("service-health")
        elif t in ("search_tickets", "get_ticket_details", "get_high_priority_tickets"):
            servers.add("support-ticket")
        elif t in ("list_recent_changes", "get_change_details", "get_changes_for_service"):
            servers.add("change-management")
    return sorted(list(servers))

def write_query_results_json(results: List[Dict[str, Any]], filepath: Path) -> None:
    """Save query results as a JSON array."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"Structured results written to {filepath}")

def generate_sample_run_markdown(results: List[Dict[str, Any]], filepath: Path) -> None:
    """Format and write the 8 query runs to outputs/sample_run_outputs.md."""
    md_content = "# Sample Run Outputs\n\n"
    
    titles = {
        "Q1": "Q1 – Payment API Health and Recent Change",
        "Q2": "Q2 – High-Priority Tickets for Unhealthy Services",
        "Q3": "Q3 – Payment API Incident and Ticket Impact",
        "Q4": "Q4 – Checkout Service Degradation and Recent Changes",
        "Q5": "Q5 – Operations Summary of Unhealthy Services, Incidents, and Tickets",
        "Q6": "Q6 – Recent Changes on Services with Active Incidents",
        "Q7": "Q7 – Ticket TKT-1001 details and Related Service Health",
        "Q8": "Q8 – Recent Changes for Payment API and Rollback Availability"
    }
    
    for i, res in enumerate(results):
        query_id = res.get("query_id", f"Q{i+1}")
        title = titles.get(query_id, f"Q{i+1} – Operations Inquiry")
        
        md_content += f"## {title}\n\n"
        md_content += "User Query:\n"
        md_content += f"{res.get('user_query')}\n\n"
        
        md_content += "Servers Used:\n"
        for s in res.get("servers_used", []):
            md_content += f"- {s}\n"
        md_content += "\n"
        
        md_content += "Tools Used:\n"
        for t in res.get("tools_used", []):
            md_content += f"- {t}\n"
        md_content += "\n"
        
        md_content += "Final Answer:\n"

        ans = res.get("final_answer", "")
        md_content += f"{ans}\n\n"
        
        if i < len(results) - 1:
            md_content += "---\n\n"
            
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Markdown outputs written to {filepath}")
