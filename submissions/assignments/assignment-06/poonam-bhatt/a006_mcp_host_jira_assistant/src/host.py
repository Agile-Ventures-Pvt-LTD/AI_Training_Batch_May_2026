import os
import sys
import json
import asyncio
import logging
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.markdown import Markdown

# Add workspace directory to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.llm import GroqLLMClient
from src.mcp_client import JiraMCPClient
from src.prompts import SYSTEM_PROMPT

from src.logging_config import setup_logging

# Configure logging
setup_logging(logging.WARNING)  # Suppress logs to keep stdin/stdout clean for the server, but allow warning/error
logger = logging.getLogger("jira-assistant.host")

console = Console()

class JiraIssueAssistantHost:
    """Orchestrates the Groq LLM agent and the Jira MCP Client connection."""
    
    def __init__(self, server_script_path: Optional[str] = None):
        self.mcp_client = JiraMCPClient(server_script_path=server_script_path)
        self.llm_client = GroqLLMClient()
        
    async def run_query(self, user_query: str) -> Dict[str, Any]:
        """Executes a natural language query using the Groq LLM and the Jira MCP Server."""
        logger.info(f"Starting execution for query: '{user_query}'")
        
        # 1. Connect to the MCP Server
        await self.mcp_client.connect()
        
        tools_used = []
        write_action_performed = False
        final_answer = ""
        
        try:
            # 2. Discover Tools
            mcp_tools = await self.mcp_client.list_available_tools()
            discovered_names = [t.name for t in mcp_tools]
            logger.info(f"Discovered tools: {discovered_names}")
            
            # Convert tools to Groq schema format
            groq_tools = self.llm_client.convert_mcp_tools_to_groq(mcp_tools)
            
            # Define list of write action tool names
            write_tools = {"add_issue_comment", "update_issue_status"}
            
            # 3. Setup message history
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_query}
            ]
            
            loop_limit = 10
            loop_count = 0
            
            while loop_count < loop_limit:
                loop_count += 1
                logger.info(f"Agent reasoning loop iteration: {loop_count}")
                
                # Get response from Groq LLM
                response = self.llm_client.get_chat_response(messages=messages, tools=groq_tools)
                message = response.choices[0].message
                
                # Check for tool calls and normalize tool calling sources
                tool_calls_to_process = message.tool_calls
                
                # Intercept Llama 3 raw <|python_tag|> tags if tool_calls is empty
                current_content = message.content or ""
                if not tool_calls_to_process and "<|python_tag|>" in current_content:
                    import re
                    import ast
                    logger.info("Found raw <|python_tag|> in LLM content. Extracting tool calls.")
                    pattern = r"<\|python_tag\|>(\w+)\(([\s\S]*?)\)"
                    matches = re.findall(pattern, current_content)
                    
                    extracted_calls = []
                    for idx, (func_name, func_args_str) in enumerate(matches):
                        func_name = func_name.strip()
                        func_args_str = func_args_str.strip()
                        
                        args = {}
                        if func_args_str:
                            try:
                                args = json.loads(func_args_str)
                            except Exception:
                                try:
                                    # Fallback: parse python keywords
                                    parsed = ast.parse(f"func({func_args_str})")
                                    call_node = parsed.body[0].value
                                    for kw in call_node.keywords:
                                        try:
                                            args[kw.arg] = ast.literal_eval(kw.value)
                                        except Exception:
                                            args[kw.arg] = str(kw.value)
                                    for p_idx, val in enumerate(call_node.args):
                                        try:
                                            args[f"arg_{p_idx}"] = ast.literal_eval(val)
                                        except Exception:
                                            args[f"arg_{p_idx}"] = str(val)
                                except Exception as err:
                                    logger.error(f"Error parsing python arguments: {err}")
                                    if "=" in func_args_str:
                                        k, v = func_args_str.split("=", 1)
                                        args = {k.strip().strip("'\""): v.strip().strip("'\"")}
                                        
                        # Create Mock Tool Call
                        class MockFunction:
                            def __init__(self, name, arguments):
                                self.name = name
                                self.arguments = json.dumps(arguments)
                                
                        class MockToolCall:
                            def __init__(self, tc_id, name, arguments):
                                self.id = tc_id
                                self.type = "function"
                                self.function = MockFunction(name, arguments)
                                
                        extracted_calls.append(MockToolCall(f"llama_call_{idx}", func_name, args))
                        
                    if extracted_calls:
                        tool_calls_to_process = extracted_calls

                # Check if we have tool calls to execute
                if not tool_calls_to_process:
                    # No tool calls: LLM has formulated a final response
                    final_answer = message.content or ""
                    break
                
                # Add the assistant response (with tool calls) to message history
                # We need to construct the tool calls block in standard API format
                assistant_tool_calls = []
                for tc in tool_calls_to_process:
                    assistant_tool_calls.append({
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    })
                
                messages.append({
                    "role": "assistant",
                    "content": message.content or "",
                    "tool_calls": assistant_tool_calls
                })
                
                # Process each tool call requested by the LLM
                for tool_call in tool_calls_to_process:
                    tool_name = tool_call.function.name
                    tool_args = json.loads(tool_call.function.arguments)
                    
                    logger.info(f"LLM requested tool call: '{tool_name}' with args: {tool_args}")
                    tools_used.append(tool_name)
                    
                    # Check if this tool is a write operation
                    if tool_name in write_tools:
                        write_action_performed = True
                    
                    try:
                        # Call MCP Server tool
                        mcp_result = await self.mcp_client.call_server_tool(tool_name, tool_args)
                        
                        # Extract content from call result
                        text_blocks = []
                        if hasattr(mcp_result, "content"):
                            for content_block in mcp_result.content:
                                if hasattr(content_block, "text"):
                                    text_blocks.append(content_block.text)
                                elif isinstance(content_block, dict) and "text" in content_block:
                                    text_blocks.append(content_block["text"])
                                else:
                                    text_blocks.append(str(content_block))
                        else:
                            text_blocks.append(str(mcp_result))
                            
                        tool_output = "\n".join(text_blocks)
                        
                    except Exception as e:
                        logger.error(f"Error executing tool '{tool_name}': {e}")
                        tool_output = f"Error executing tool '{tool_name}': {str(e)}"
                    
                    # Append tool response to message history
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": tool_name,
                        "content": tool_output
                    })
            
            if loop_count >= loop_limit:
                logger.warning("Reached agent reasoning loop limit. Terminating loop.")
                final_answer = "The agent loop was terminated early due to exceeding maximum reasoning steps."
                
        finally:
            # 4. Disconnect client
            await self.mcp_client.disconnect()
            
        # Return standard format output as per FR-7
        return {
            "user_query": user_query,
            "tools_used": list(set(tools_used)),  # Unique list of tool names
            "final_answer": final_answer,
            "write_action_performed": write_action_performed
        }

async def execute_and_print(host: JiraIssueAssistantHost, query: str):
    try:
        result = await host.run_query(query)
        
        # Print natural language response
        console.print("\n[green][OK][/green] [bold]Assistant Response:[/bold]")
        console.print(Panel(Markdown(result["final_answer"]), border_style="cyan"))
        
        # Display execution details
        tools_list = ", ".join(result["tools_used"]) if result["tools_used"] else "None"
        console.print(f"[dim]Tools Used: {tools_list}[/dim]")
        if result["write_action_performed"]:
            console.print("[bold yellow][WRITE] Write Action Performed successfully on Jira[/bold yellow]")
        
        # Save JSON output to file (FR-7 compliance)
        formatted_json = json.dumps(result, indent=2)
        os.makedirs("outputs", exist_ok=True)
        # Create a clean safe filename from query
        safe_query_name = "".join(c if c.isalnum() else "_" for c in query[:30]).strip("_")
        output_file = os.path.join("outputs", f"query_{safe_query_name}.json")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(formatted_json)
        console.print(f"[dim]Execution logs saved to: {output_file}[/dim]")
    except Exception as e:
        console.print(f"[red]Error executing query: {e}[/red]", style="bold red")

async def main():
    load_dotenv()
    
    host = JiraIssueAssistantHost()
    
    # Check if a query was passed as a command-line argument
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        console.print(Panel(f"[bold blue]Jira MCP Assistant Host - Direct Execution[/bold blue]\nQuery: '{query}'", border_style="blue"))
        
        # Tool discovery output
        try:
            client = JiraMCPClient()
            await client.connect()
            mcp_tools = await client.list_available_tools()
            tool_names = [t.name for t in mcp_tools]
            await client.disconnect()
            console.print("[green][OK][/green] Tool Discovery successful. Available tools:")
            console.print(json.dumps({"available_tools": tool_names}, indent=2))
            console.print("-" * 50)
        except Exception as e:
            console.print(f"[red]Error during tool discovery: {e}[/red]")
            sys.exit(1)
            
        await execute_and_print(host, query)
    else:
        # Interactive CLI Mode
        console.print(Panel(
            "[bold green]Jira MCP Assistant Host - Interactive CLI Mode[/bold green]\n"
            "Type your query below to interact with Jira issues using the LLM agent.\n"
            "Type 'exit' or 'quit' to close the assistant.",
            border_style="green"
        ))
        
        # Initial Tool Discovery (FR-3)
        try:
            client = JiraMCPClient()
            await client.connect()
            mcp_tools = await client.list_available_tools()
            tool_names = [t.name for t in mcp_tools]
            await client.disconnect()
            console.print("[green][OK][/green] Tool Discovery successful. Available tools:")
            console.print(json.dumps({"available_tools": tool_names}, indent=2))
            console.print("-" * 50)
        except Exception as e:
            console.print(f"[red]Error during tool discovery: {e}[/red]")
            sys.exit(1)
            
        while True:
            try:
                # Ask user for input
                query = console.input("\n[bold cyan]Enter your query[/bold cyan] (or 'exit' to quit): ").strip()
                if not query:
                    continue
                if query.lower() in ("exit", "quit"):
                    console.print("[yellow]Exiting Jira MCP Assistant. Goodbye![/yellow]")
                    break
                    
                console.print(f"\n[bold blue]Processing:[/bold blue] '{query}'...")
                await execute_and_print(host, query)
                console.print("-" * 50)
            except KeyboardInterrupt:
                console.print("\n[yellow]Exiting Jira MCP Assistant. Goodbye![/yellow]")
                break
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")

if __name__ == "__main__":
    asyncio.run(main())






# Project: A006 Jira MCP Server
# Author: Poonam Bhatt
# Note: Using API v3 /search/jql for JQL queries due to Atlassian deprecation.

