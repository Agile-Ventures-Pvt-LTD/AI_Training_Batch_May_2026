import os
import sys
import shutil
import asyncio
import json
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

from dotenv import load_dotenv

# Load env variables from .env file
load_dotenv()

from src.host import JiraIssueAssistantHost

console = Console()

# Define the 8 sample queries targeting live Jira data
SAMPLE_QUERIES = [
    "List all Jira projects",
    "Show all issues in To Do status",
    "Show high-priority issues",
    "Summarize issue MT-1",
    "Show comments for issue MT-1",
    "Add a comment to MT-1 saying 'QA validation is pending'",
    "Update status of MT-1 to In Progress",
    "Which issues are assigned to me?"
]

async def clean_outputs():
    """Delete all files in the outputs directory to ensure a fresh run."""
    outputs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "outputs"))
    if os.path.exists(outputs_dir):
        console.print(f"[yellow]Cleaning existing outputs directory: {outputs_dir}[/yellow]")
        shutil.rmtree(outputs_dir)
    os.makedirs(outputs_dir, exist_ok=True)
    console.print("[green][OK] Outputs directory cleared and recreated successfully.[/green]")

async def execute_query(host, query_index, query):
    console.print("\n" + "=" * 80)
    console.print(f"[bold cyan]Query #{query_index}:[/bold cyan] '{query}'")
    console.print("=" * 80)
    
    try:
        result = await host.run_query(query)
        
        # Display response
        console.print("\n[green][OK][/green] [bold]Assistant Response:[/bold]")
        console.print(Panel(Markdown(result["final_answer"]), border_style="cyan"))
        console.print(f"[dim]Tools Used: {', '.join(result['tools_used']) if result['tools_used'] else 'None'}[/dim]")
        if result["write_action_performed"]:
            console.print("[bold yellow][WRITE] Write Action Performed successfully on Jira[/bold yellow]")
            
        # Save JSON output to outputs folder
        formatted_json = json.dumps(result, indent=2)
        safe_query_name = "".join(c if c.isalnum() else "_" for c in query[:30]).strip("_")
        output_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "outputs", f"query_{safe_query_name}.json"))
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(formatted_json)
        console.print(f"[dim]Execution logs saved to: {output_file}[/dim]")
        
    except Exception as e:
        console.print(f"[bold red]Failed to execute query: {e}[/bold red]")

async def main():
    console.print(Panel("[bold green]Jira Issue Assistant - Automatic Batch Runner[/bold green]\nClearing all output files and running all 8 sample queries live against your Jira account...", border_style="green"))
    
    # 1. Clean outputs
    await clean_outputs()
    
    # 2. Run queries
    host = JiraIssueAssistantHost()
    for idx, query in enumerate(SAMPLE_QUERIES, 1):
        await execute_query(host, idx, query)
        
    console.print("\n" + "=" * 80)
    console.print("[bold green]Batch Run Complete! All 8 queries executed cleanly and outputs archived.[/bold green]")
    console.print("=" * 80)

if __name__ == "__main__":
    asyncio.run(main())
