try:
    from langchain.tools import StructuredTool
except ImportError as e:
    print(f"Langchain library not installed. Error: {e}")

def create_tool(function, tool_name: str | None, tool_description: str | None):
    tool = StructuredTool.from_function(
        func=function,
        name=tool_name,
        description=tool_description
    )
    return tool