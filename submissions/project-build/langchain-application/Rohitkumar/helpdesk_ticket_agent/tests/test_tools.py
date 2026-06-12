from tools import (
    search_tickets,
    get_ticket_details,
    get_overdue_tickets
)


def test_search():

    result = search_tickets.invoke(
        {
            "priority": "High"
        }
    )

    assert result is not None


def test_ticket_details():

    result = get_ticket_details.invoke(
        {
            "ticket_id": "TCK-1001"
        }
    )

    assert result is not None


def test_overdue():

    result = get_overdue_tickets.invoke({})

    assert result is not None