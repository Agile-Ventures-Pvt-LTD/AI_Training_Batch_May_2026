# tests/test_agent_queries.py

from src.agents.legacy_agent import (
    agent_executor
)


def test_customer_count_query():

    response = agent_executor.invoke(
        {
            "input":
            "How many customers are there?"
        }
    )

    assert "10" in response["output"]


def test_revenue_query():

    response = agent_executor.invoke(
        {
            "input":
            "What is the total revenue from completed orders?"
        }
    )

    assert "71,100" in response["output"] \
        or "71100" in response["output"]