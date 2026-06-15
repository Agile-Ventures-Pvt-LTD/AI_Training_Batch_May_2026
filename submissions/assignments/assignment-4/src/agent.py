from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from langchain_groq import ChatGroq
from tool import query_ecommerce_database
from db import SCHEMA_DESCRIPTION

SYSTEM_PROMPT = f"""You are an e-commerce data analyst assistant. You help users understand their business data by querying a SQLite database.

Database schema:
{SCHEMA_DESCRIPTION}

Rules:
- Only use SELECT queries. Never INSERT, UPDATE, or DELETE.
- Never make up numbers or invent data — only report what the query returns.
- Explain results in plain business language, not raw SQL output.
- If a query returns no data, say "No data found" and suggest why.
- Always answer the user's question directly and concisely.
"""

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
available_tools = {"query_ecommerce_database": query_ecommerce_database}
llm_with_tools = llm.bind_tools(list(available_tools.values()))

def answer(query: str) -> str:
    messages = [SystemMessage(SYSTEM_PROMPT), HumanMessage(query)]
    ai_msg = llm_with_tools.invoke(messages)
    messages.append(ai_msg)
    for tool_call in ai_msg.tool_calls:
        selected_tool = available_tools[tool_call["name"]]
        tool_output = selected_tool.invoke(tool_call["args"])
        messages.append(ToolMessage(tool_output, tool_call_id=tool_call["id"]))
    if ai_msg.tool_calls:
        final = llm.invoke(messages)
        return final.content
    return ai_msg.content
