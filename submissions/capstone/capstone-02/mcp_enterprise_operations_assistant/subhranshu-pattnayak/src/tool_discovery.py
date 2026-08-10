from mcp_use import MCPClient
from config import SERVER_PATH
import os, asyncio

client = MCPClient({
    "mcpServers": {
        "service-health": {
            "command": "uv",
            "args": [
                "run",
                "python",
                os.path.join(SERVER_PATH, "service_health_server.py")
            ]
        },
        "support-ticket": {
            "command": "uv",
            "args": [
                "run",
                "python",
                os.path.join(SERVER_PATH, "support_ticket_server.py")
            ]
        },
        "change-management": {
            "command": "uv",
            "args": [
                "run",
                "python",
                os.path.join(SERVER_PATH, "change_management_server.py")
            ]
        }
    }
})

client.create_all_sessions()
print(client.active_sessions)

async def disover_health_tools():
    service_health_session = client.get_session("service-health")
    
    health_tools = await service_health_session.list_tools()
    
    health_tool_names = [t.name for t in health_tools]
    
    return health_tool_names


async def disover_ticket_tools():
    support_ticket_session = client.get_session("support-ticket")
    ticket_tools = await support_ticket_session.list_tools()
    ticket_tool_names = [t.name for t in ticket_tools]
    return ticket_tool_names


async def disover_change_tools():
    change_management_session = client.get_session("change-management")
    change_tools = await change_management_session.list_tools()
    change_tool_names = [t.name for t in change_tools]
    return change_tool_names

async def discover():
    health = await disover_health_tools()
    ticket = await disover_ticket_tools()
    change = await disover_change_tools()
    print(f"Available health tools: {health}")
    print(f"Available ticket tools: {ticket}")
    print(f"Available change tools: {change}")
    client.close_all_sessions()

if __name__ == "__main__":
    asyncio.run(discover())