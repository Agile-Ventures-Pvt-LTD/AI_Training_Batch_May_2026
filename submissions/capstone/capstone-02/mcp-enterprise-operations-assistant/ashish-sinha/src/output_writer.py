import json
from pathlib import Path
from typing import Dict, Any

OUTPUT_DIR = Path("outputs")
SAMPLE_RUNS_PATH = OUTPUT_DIR / "sample_run_outputs.md"

def ensure_output_dir():
    OUTPUT_DIR.mkdir(exist_ok=True)

def write_tool_discovery(tools: Dict[str, Any]):
    ensure_output_dir()
    with open(OUTPUT_DIR / "tool_discovery.json", "w") as f:
        json.dump(tools, f, indent=2)

def write_mandatory_results(results: list):
    ensure_output_dir()
    with open(OUTPUT_DIR / "mandatory_query_results.json", "w") as f:
        json.dump(results, f, indent=2)

def append_single_sample_run(res: dict):
    """Appends a single query result to the markdown file safely."""
    ensure_output_dir()
    file_exists = SAMPLE_RUNS_PATH.exists()
    
    with open(SAMPLE_RUNS_PATH, "a", encoding="utf-8") as f:
        if not file_exists:
            f.write("# Sample Run Outputs\n\n")
        
        f.write(f"## {res.get('query_id', 'Query')}\n\n")
        f.write(f"**User Query:**\n{res.get('user_query', '')}\n\n")
        f.write(f"**Servers Used:**\n- {', '.join(res.get('servers_used', [])) if res.get('servers_used') else 'None'}\n\n")
        f.write(f"**Tools Used:**\n- {', '.join(res.get('tools_used', [])) if res.get('tools_used') else 'None'}\n\n")
        f.write(f"**Final Answer:**\n```json\n{json.dumps(res, indent=2)}\n```\n\n")
        f.write("---\n\n")

def write_sample_runs(results: list):
    """Processes a list of results and appends them one by one."""
    for res in results:
        append_single_sample_run(res)
