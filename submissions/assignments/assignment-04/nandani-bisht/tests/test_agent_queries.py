from src.agents.modern_agent import create_ecommerce_agent


def test_customer_count():

    agent = create_ecommerce_agent()

    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "How many customers are there?"
                }
            ]
        }
    )

    assert response is not None


def test_total_revenue():

    agent = create_ecommerce_agent()

    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "What is the total revenue from completed orders?"
                }
            ]
        }
    )

    assert response is not None