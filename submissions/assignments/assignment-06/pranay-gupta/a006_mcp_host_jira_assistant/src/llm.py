import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
class GroqLLM:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model_name = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    def format_mcp_tools(self,mcp_tools:list) -> list:
        groq_tool = []
        for tool in mcp_tools:
            groq_tool.append({
                "type":"function",
                "function":{
                    'name':tool.name,
                    "description":tool.description,
                    "parameters":tool.inputSchema
                }
            })
        return groq_tool

    def generate_chat_response(self,messages:list,tools:list=None):
        return self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=0.0,
            tools=tools or None,
            tool_choice="auto" if tools else None,
        )