import json
from pathlib import Path


def save_tool_discovery(tools: dict) -> None:
    """
    Save actual tools
    """
    output_path = Path("outputs/tool_discovery.json")
    output_path.parent.mkdir(parents=True,exist_ok=True)
    with open( output_path,"w",encoding="utf-8") as f:
        json.dump(tools,f,indent=4)