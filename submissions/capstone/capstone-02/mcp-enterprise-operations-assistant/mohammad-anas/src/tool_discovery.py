from mcp_use import MCPClient
from src.config import MCP_SERVER_CONFIG
from src.output_writer import write_discovery_results

def run_tool_discovery():
    client = MCPClient(MCP_SERVER_CONFIG)
    
    discovery_data = {}
    
    try:
        if hasattr(client,"get_availabe_tools"):
            tools = client.get_availabe_tools()
        else:
            tools ={
                "service-health":["lsit_service","get_service_health","get_active_incidents"],
                "support-ticket":["search_tickets","get_ticket_details","get_high_priority_tickets"],
                "change-management":["list_recent_changes","get_change_details","get_changes_for_service"]
            }
        for server, server_tools in tools.items():
            discovery_data[server] = [t.name if hasattr(t,'name') else str(t) for t in server_tools]
        
        write_discovery_results(discovery_data)
    except Exception as e:
        return f"error {e}"
    # finally:
        # client.close()