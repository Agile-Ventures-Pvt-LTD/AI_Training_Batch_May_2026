import json
import os
import sys

from fastmcp import Client
from fastmcp.client.transports import PythonStdioTransport


SOCKS_PROXY_VARS = {
    "ALL_PROXY", "all_proxy",
    "GRPC_PROXY", "grpc_proxy",
    "FTP_PROXY", "ftp_proxy",
    "RSYNC_PROXY",
}


def _build_subprocess_env():
    env = os.environ.copy()
    for key in SOCKS_PROXY_VARS:
        env.pop(key, None)
    return env


class JiraMCPClient:
    def __init__(self, server_script_path):
        self._transport = PythonStdioTransport(
            script_path=server_script_path,
            env=_build_subprocess_env(),
            python_cmd=sys.executable,
        )
        self._client = Client(self._transport)

    async def __aenter__(self):
        await self._client.__aenter__()
        return self

    async def __aexit__(self, *exc_info):
        await self._client.__aexit__(*exc_info)

    async def list_tools_for_groq(self):
        mcp_tools = await self._client.list_tools()
        return [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description or "",
                    "parameters": tool.inputSchema,
                },
            }
            for tool in mcp_tools
        ]

    async def call_tool(self, name, arguments):
        result = await self._client.call_tool(name, arguments)
        return json.dumps(result.data, default=str)
