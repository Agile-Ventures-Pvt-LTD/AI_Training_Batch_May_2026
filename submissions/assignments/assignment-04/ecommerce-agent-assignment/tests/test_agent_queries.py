"""
test_agent_queries.py
"""

from src.agents.modern_agent import (
    run_agent
)


TEST_QUERIES = [

    "How many customers exist?",

    "How many products exist?",

    "How many orders exist?",

    "Show top 5 customers by spending.",

    "What is total revenue?",

    "Show low stock products.",

    "How many pending orders are there?",

    "Show cancelled orders.",

    "What is the average order value?"
]


def run_agent_tests():

    print("AGENT TESTS")

    for i, query in enumerate(
        TEST_QUERIES,
        start=1
    ):

        print("\n" + "-" * 60)

        print(
            f"Test {i}: {query}"
        )

        try:

            response = run_agent(
                query
            )

            print("\nResponse:")

            print(response)

            print(
                "\nQuery executed"
            )

        except Exception as error:

            print(
                f"\n Failed: {error}"
            )


if __name__ == "__main__":
    run_agent_tests()