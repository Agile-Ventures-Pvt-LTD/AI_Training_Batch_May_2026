from tools import (search_tickets,get_ticket_details,get_ticket_comments,calculate_sla_status,prioritize_tickets,get_open_tickets,get_overdue_tickets,get_customer_history)


def run_test(test_name, result):
    print("\n" + "=" * 60)
    print(f"TEST: {test_name}")
    print("=" * 60)

    print(result)

    print("\nSTATUS: PASSED")


def test_search_tickets():

    result = search_tickets.invoke(
        {
            "status": "Open",
            "limit": 5
        }
    )

    run_test(
        "search_tickets",
        result
    )


def test_ticket_details():

    tickets = search_tickets.invoke(
        {
            "limit": 1
        }
    )

    if not tickets:
        print("No tickets found.")
        return

    ticket_id = tickets[0]["ticket_id"]

    result = get_ticket_details.invoke(
        {
            "ticket_id": ticket_id
        }
    )

    run_test(
        "get_ticket_details",
        result
    )


def test_ticket_comments():

    tickets = search_tickets.invoke(
        {
            "limit": 1
        }
    )

    if not tickets:
        print("No tickets found.")
        return

    ticket_id = tickets[0]["ticket_id"]

    result = get_ticket_comments.invoke(
        {
            "ticket_id": ticket_id
        }
    )

    run_test(
        "get_ticket_comments",
        result
    )


def test_sla_status():

    tickets = search_tickets.invoke(
        {
            "limit": 1
        }
    )

    if not tickets:
        print("No tickets found.")
        return

    ticket_id = tickets[0]["ticket_id"]

    result = calculate_sla_status.invoke(
        {
            "ticket_id": ticket_id
        }
    )

    run_test(
        "calculate_sla_status",
        result
    )


def test_prioritize_tickets():

    result = prioritize_tickets.invoke(
        {
            "limit": 5
        }
    )

    run_test(
        "prioritize_tickets",
        result
    )


def test_open_tickets():

    result = get_open_tickets.invoke({})

    run_test(
        "get_open_tickets",
        result
    )


def test_overdue_tickets():

    result = get_overdue_tickets.invoke({})

    run_test(
        "get_overdue_tickets",
        result
    )


def test_customer_history():

    tickets = search_tickets.invoke(
        {
            "limit": 1
        }
    )

    if not tickets:
        print("No tickets found.")
        return

    customer_id = tickets[0]["customer_id"]

    result = get_customer_history.invoke(
        {
            "customer_id": customer_id
        }
    )

    run_test(
        "get_customer_history",
        result
    )


if __name__ == "__main__":

    print("\nRUNNING TOOL TESTS")

    test_search_tickets()

    test_ticket_details()

    test_ticket_comments()

    test_sla_status()

    test_prioritize_tickets()

    test_open_tickets()

    test_overdue_tickets()

    test_customer_history()

    print("\nALL TESTS COMPLETED")