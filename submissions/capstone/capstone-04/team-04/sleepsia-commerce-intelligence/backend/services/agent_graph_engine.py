"""
Multi-Agent Graph Orchestration Engine in Python.
"""

from typing import Dict, Any, Optional
from .multi_agent_supervisor import run_orchestrated_agent_pipeline

async def execute_multi_agent_graph(data: Dict[str, Any], selected_date: Optional[str] = None) -> Dict[str, Any]:
    """
    Executes the multi-agent graph DAG for data validation, domain intelligence, and synthesis.
    """
    return run_orchestrated_agent_pipeline(data, selected_date)
