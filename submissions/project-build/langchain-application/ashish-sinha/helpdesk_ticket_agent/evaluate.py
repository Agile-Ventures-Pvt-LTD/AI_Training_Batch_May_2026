import json
from datetime import datetime

from tools import search_tickets,get_ticket_details,get_ticket_comments,calculate_sla_status,prioritize_tickets


def run_evaluation():

    results = []

    test_cases = [
        (
            "search_tickets",
            lambda: search_tickets.invoke(
                {
                    "status": "Open"
                }
            )
        ),
        (
            "prioritize_tickets",
            lambda: prioritize_tickets.invoke({})
        )
    ]

    # get real ticket id from database
    tickets = search_tickets.invoke({})

    if tickets["count"] > 0:

        ticket_id = tickets["tickets"][0]["ticket_id"]

        test_cases.extend([
            (
                "get_ticket_details",
                lambda: get_ticket_details.invoke(
                    {
                        "ticket_id": ticket_id
                    }
                )
            ),
            (
                "get_ticket_comments",
                lambda: get_ticket_comments.invoke(
                    {
                        "ticket_id": ticket_id
                    }
                )
            ),
            (
                "calculate_sla_status",
                lambda: calculate_sla_status.invoke(
                    {
                        "ticket_id": ticket_id
                    }
                )
            )
        ])

    for test_name, test_func in test_cases:

        try:

            output = test_func()

            results.append(
                {
                    "tool": test_name,
                    "status": "PASS",
                    "output": output
                }
            )

        except Exception as e:

            results.append(
                {
                    "tool": test_name,
                    "status": "FAIL",
                    "error": str(e)
                }
            )

    report = {
        "evaluation_timestamp": datetime.utcnow().isoformat(),
        "total_tests": len(results),
        "passed": sum(
            1 for r in results
            if r["status"] == "PASS"
        ),
        "failed": sum(
            1 for r in results
            if r["status"] == "FAIL"
        ),
        "results": results
    }

    with open(
        "outputs/evaluation_outputs.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            report,
            f,
            indent=4,
            default=str
        )

    print(
        "Evaluation report saved to outputs/evaluation_outputs.json"
    )


if __name__ == "__main__":
    run_evaluation()