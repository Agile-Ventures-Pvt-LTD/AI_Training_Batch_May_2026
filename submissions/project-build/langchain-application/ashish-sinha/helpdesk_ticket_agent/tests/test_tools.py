from tools import (
    search_tickets,
    get_ticket_details,
    get_ticket_comments,
    calculate_sla_status,
    prioritize_tickets,
    update_ticket_status,
    add_ticket_comment,
    recall_conversation_tool,
    recall_archival_memory_tool
)


def test_search_tickets():

    result = search_tickets.invoke(
        {
            "status": "Open"
        }
    )

    assert result is not None
    assert isinstance(result, dict)


def test_get_ticket_details():

    result = get_ticket_details.invoke(
        {
            "ticket_id": "TCK-1001"
        }
    )

    assert result is not None
    assert isinstance(result, dict)


def test_get_ticket_comments():

    result = get_ticket_comments.invoke(
        {
            "ticket_id": "TCK-1001"
        }
    )

    assert result is not None
    assert isinstance(result, dict)


def test_calculate_sla_status():

    result = calculate_sla_status.invoke(
        {
            "ticket_id": "TCK-1001"
        }
    )

    assert result is not None
    assert isinstance(result, dict)


def test_prioritize_tickets():

    result = prioritize_tickets.invoke({})

    assert result is not None
    assert isinstance(result, dict)


def test_update_ticket_status_invalid():

    result = update_ticket_status.invoke(
        {
            "ticket_id": "INVALID-ID",
            "new_status": "In Progress"
        }
    )

    assert result is not None
    assert isinstance(result, dict)


def test_add_ticket_comment_invalid():

    result = add_ticket_comment.invoke(
        {
            "ticket_id": "INVALID-ID",
            "comment": "Test comment"
        }
    )

    assert result is not None
    assert isinstance(result, dict)


def test_recall_conversation():

    result = recall_conversation_tool.invoke(
        {
            "keyword": "billing"
        }
    )

    assert result is not None
    assert isinstance(result, dict)


def test_recall_archival_memory():

    result = recall_archival_memory_tool.invoke({})

    assert result is not None
    assert isinstance(result, dict)