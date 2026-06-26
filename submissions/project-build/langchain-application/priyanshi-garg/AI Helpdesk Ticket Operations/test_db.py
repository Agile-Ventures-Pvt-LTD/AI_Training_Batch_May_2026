from db_utils import execute_query

result = execute_query(
    """
    SELECT
        ticket_id,
        priority,
        status
    FROM tickets
    WHERE status='Open'
    """
)

print(result[:20])