"""
Specialist Agents Module - Pure function agents for multi-agent analysis

Each agent is an independent specialist that:
1. Takes structured input data
2. Performs specific analysis
3. Returns structured output with reasoning
4. Has no side effects
"""

from typing import Dict, Any

from backend.services.specialist_agents.base_agent import BaseAgent, AgentResult
from backend.services.specialist_agents.sales_agent import SalesAgent
from backend.services.specialist_agents.advertising_agent import AdvertisingAgent
from backend.services.specialist_agents.customer_insights_agent import CustomerInsightsAgent


# Agent registry - maps agent names to their classes
AGENTS = {
    'sales': SalesAgent,
    'advertising': AdvertisingAgent,
    'customer_insights': CustomerInsightsAgent,
}


def get_agent(agent_name: str) -> BaseAgent:
    """
    Factory function to get agent by name.

    Args:
        agent_name: Name of the agent (e.g., 'sales', 'advertising')

    Returns:
        Instantiated agent

    Raises:
        ValueError: If agent name is not found
    """
    agent_class = AGENTS.get(agent_name.lower())
    if not agent_class:
        available = list(AGENTS.keys())
        raise ValueError(f"Unknown agent: {agent_name}. Available: {available}")
    return agent_class()


def get_all_agents() -> Dict[str, BaseAgent]:
    """
    Get all available agents.

    Returns:
        Dictionary mapping agent names to instantiated agents
    """
    return {name: cls() for name, cls in AGENTS.items()}


__all__ = [
    'BaseAgent',
    'AgentResult',
    'SalesAgent',
    'AdvertisingAgent',
    'CustomerInsightsAgent',
    'get_agent',
    'get_all_agents',
    'AGENTS',
]
