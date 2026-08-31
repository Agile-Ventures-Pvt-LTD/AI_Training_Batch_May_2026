import json
from pathlib import Path
from typing import Dict, Any

OUTPUT_DIR = Path("outputs")

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

def write_sample_runs(results: list):
    ensure_output_dir()
    with open(OUTPUT_DIR / "sample_run_outputs.md", "w") as f:
        f.write("# Sample Run Outputs\n\n")
        for res in results:
            f.write(f"## {res.get('query_id', 'Query')} \n")
            f.write(f"**User Query:**\n{res.get('user_query', '')}\n\n")
            f.write(f"**Servers Used:**\n{', '.join(res.get('servers_used', []))}\n\n")
            f.write(f"**Tools Used:**\n{', '.join(res.get('tools_used', []))}\n\n")
            f.write(f"**Final Answer:**\n```json\n{json.dumps(res, indent=2)}\n```\n\n---\n")