try:
    from db_utils.db_connection import get_conn
    from utils.tool_utils import create_tool
    import sqlite3
    from typing import Optional
except ImportError as e:
    print(f"Error: {e}")

def get_card_details(
    customer_id: Optional[str] = None,
    card_last4: Optional[str] = None,
):
    """
    Retrieve card information by customer ID or card last 4 digits. Sensitive information is masked.
    """

    if not customer_id and not card_last4:
        return {
            "error": "Provide either customer_id or card_last4"
        }

    conn = get_conn()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = """
        SELECT
            c.card_number,
            c.valid_from,
            c.expiry,
            c.cust_id,
            ct.card_type,
            ct.card_network,
            ct.privilege,
            cust.first_name,
            cust.last_name
        FROM card c
        JOIN card_type ct
            ON c.card_type_id = ct.card_type_id
        JOIN customer cust
            ON c.cust_id = cust.cust_id
        WHERE 1=1
    """

    params = []
    
    if customer_id:
        query += " AND c.cust_id = ?"
        params.append(customer_id)

    if card_last4:
        query += " AND substr(c.card_number, -4) = ?"
        params.append(card_last4)
    
    cursor.execute(query, params)

    rows = cursor.fetchall()

    conn.close()
    
    if not rows:
        return {
            "records_found": 0,
            "cards": []
        }
    
    cards = []

    for row in rows:

        card_number = str(row["card_number"])

        masked_card = (
            "*" * (len(card_number) - 4)
            + card_number[-4:]
        )
    
        cards.append(
            {
                "customer_id": row["cust_id"],
                "customer_name": f"{row['first_name']} {row['last_name']}",
                "card_number": masked_card,
                "valid_from": row["valid_from"],
                "expiry": row["expiry"],
                "card_type": row["card_type"],
                "card_network": row["card_network"],
                "privilege": row["privilege"],
            }
        )

    return {
        "records_found": len(cards),
        "cards": cards,
        "sensitive_data_masked": True
    }


description = '''Get card information by customer ID or card last 4 digits. Returns card type, network, privilege, validity dates, and a masked card number.'''

get_card_details_tool = create_tool(function=get_card_details, tool_name="get_card_details", tool_description=description)