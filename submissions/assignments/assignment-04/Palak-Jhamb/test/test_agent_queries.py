
from pathlib import Path

from src.agents.modern_agent import invoke

OUTPUT_DIR = Path("test_results")
OUTPUT_FILE = OUTPUT_DIR / "agent_output.txt"


TEST_QUERIES = [
    "What is the total revenue from completed orders?",
    "Which customer has spent the most money?",
    "Show the top 5 products by quantity sold.",
    "Which product category generated the highest revenue?",
    "How many orders are pending?",
    "Show all cancelled orders with customer names.",
    "Which customers are from Delhi?",
    "Which products have stock below 10?",
    "What is the average order value?",
    "Show total revenue by month.",
    "Which city has the highest number of customers?",
    "Which customers have placed more than 2 orders?",
    "What are the top 3 most expensive products?",
    "Which product has never been ordered?",
    "Show total sales by product category."
]


def test_agent_queries():

    report = []

    report.append("=" * 80)
    report.append("MODERN AGENT QUERY TEST REPORT")
    report.append("=" * 80)

    for idx, query in enumerate(TEST_QUERIES, start=1):

        report.append("\n" + "=" * 80)
        report.append(f"QUERY {idx}")
        report.append("=" * 80)

        report.append(f"\nQUESTION:\n{query}")

        try:

            answer = invoke(query)

            report.append("\nANSWER:")
            report.append(str(answer))

            report.append("\nSTATUS: PASS")

        except Exception as e:

            report.append("\nSTATUS: FAIL")
            report.append(f"ERROR: {str(e)}")

    OUTPUT_DIR.mkdir(exist_ok=True)

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        file.write("\n".join(report))

    print("\n".join(report))

    print(f"\nReport saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    test_agent_queries()
