#Use legacy langchain for this test file

print("Use legacy langchain for this test file")
from src.agents.legacy_agent import agent


def ask(question: str) -> str:
    response = agent.invoke(
        {"input": question}
    )

    return response["output"]


def test_customer_count_query():
    answer = ask(
        "How many customers are there?"
    )

    assert answer
    assert "10" in answer or "customer" in answer.lower()


def test_low_stock_products_query():
    answer = ask(
        "Which products have stock below 10?"
    )

    assert answer
    assert len(answer) > 0


def test_top_customer_query():
    answer = ask(
        "Which customer has spent the most money?"
    )

    assert answer
    assert len(answer) > 0


def test_pending_orders_query():
    answer = ask(
        "How many orders are pending?"
    )

    assert answer
    assert len(answer) > 0


def test_cancelled_orders_query():
    answer = ask(
        "Show all cancelled orders with customer names."
    )

    assert answer
    assert len(answer) > 0