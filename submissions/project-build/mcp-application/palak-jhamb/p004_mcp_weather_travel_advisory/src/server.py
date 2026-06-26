from mcp_use.server import MCPServer
from tool import router as tools_router
from prompts import router as prompts_router
from resources import router as resources_router

server = MCPServer(name="weather_server")
server.include_router(tools_router)
server.include_router(prompts_router)
server.include_router(resources_router)

if __name__ == "__main__":
    server.run(transport="streamable-http")