from src.agents.modern_agent import run_agent


def test_total_revenue():

    response = run_agent(
        "What is the total revenue from completed orders?"
    )

    assert response


def test_top_customer():

    response = run_agent(
        "Which customer has spent the most money?"
    )

    assert response


def test_pending_orders():

    response = run_agent(
        "How many orders are pending?"
    )

    assert response