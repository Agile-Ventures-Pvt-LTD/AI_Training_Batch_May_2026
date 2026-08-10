from pathlib import Path

from src.tools.ecommerce_sql_tool import (
    query_ecommerce_database
)


OUTPUT_DIR = Path("test_results")
OUTPUT_FILE = OUTPUT_DIR / "tool_output.txt"


def test_sql_tool():

    report = []

    report.append("=" * 60)
    report.append("SQL TOOL TEST REPORT")
    report.append("=" * 60)

    # Tool Found
    report.append("\nTool Found: PASS")

    # Tool Name
    report.append(
        f"Tool Name: {query_ecommerce_database.name}"
    )

    # Tool Description
    report.append(
        f"\nTool Description:\n{query_ecommerce_database.description}"
    )

    # Simple Tool Invocation Test
    try:

        result = query_ecommerce_database.invoke(
            {
                "sql_query":
                "SELECT COUNT(*) FROM customers;"
            }
        )

        report.append("\nTool Invocation: PASS")

        report.append(
            f"Sample Result:\n{result}"
        )

    except Exception as e:

        report.append("\nTool Invocation: FAIL")

        report.append(str(e))

    OUTPUT_DIR.mkdir(exist_ok=True)

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        f.write("\n".join(report))

    print("\n".join(report))

    print(
        f"\nReport saved to: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    test_sql_tool()