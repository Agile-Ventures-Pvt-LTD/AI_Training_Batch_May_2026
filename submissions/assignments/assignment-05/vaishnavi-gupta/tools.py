from typing import Optional
from datetime import datetime, timedelta
from langchain_core.tools import tool

from db_utils import (
    execute_query,
    execute_single,
    get_all_tables,
    get_table_schema
)

# Helper Functions

def mask_email(email: str | None):

    if not email:
        return None

    if "@" not in email:
        return email

    username, domain = email.split("@")

    if len(username) <= 2:
        return f"**@{domain}"

    return f"{username[:2]}*****@{domain}"


def mask_phone(phone: str | None):

    if not phone:
        return None

    if len(phone) < 4:
        return "****"

    return f"******{phone[-4:]}"


def mask_card(card_number: str | None):

    if not card_number:
        return None

    digits = str(card_number)

    return f"**** **** **** {digits[-4:]}"

#Tool 1

@tool
def inspect_database_schema():
    """
    Return database tables and schema.
    """

    schema = {}

    tables = get_all_tables()

    for table in tables:
        cols = get_table_schema(table)

        schema[table] = [
            column["name"]
            for column in cols
        ]

    return {
        "tool_used": "inspect_database_schema",
        "records_found": len(tables),
        "answer": schema,
        "sensitive_data_masked": True
    }

#Tool 2

@tool
def get_customer_profile(customer_id: str):
    """
    Retrieve customer profile information by customer ID.
    """

    query = """
    SELECT *
    FROM customer
    WHERE cust_id = ?
    """

    customer = execute_single(
        query,
        (customer_id,)
    )

    if not customer:
        return {
            "tool_used": "get_customer_profile",
            "records_found": 0,
            "answer": "Customer not found",
            "sensitive_data_masked": True
        }

    customer["email"] = mask_email(
        customer["email"]
    )

    customer["phone"] = mask_phone(
        customer["phone"]
    )

    return {
        "tool_used": "get_customer_profile",
        "records_found": 1,
        "answer": customer,
        "sensitive_data_masked": True
    }

# Tool 3

@tool
def get_card_details(customer_id: str):
    """
    Retrieve masked card details for a customer.
    """

    query = """
    SELECT
        c.card_number,
        c.valid_from,
        c.expiry,
        ct.card_type,
        ct.card_network,
        ct.privilege
    FROM card c
    LEFT JOIN card_type ct
        ON c.card_type_id = ct.card_type_id
    WHERE c.cust_id = ?
    """

    cards = execute_query(
        query,
        (customer_id,)
    )

    for card in cards:
        card["card_number"] = mask_card(
            card["card_number"]
        )

    return {
    "tool_used": "get_card_details",
    "records_found": len(cards),
    "answer": cards,
    "sensitive_data_masked": True
}

# Tool 4

@tool
def get_customer_transactions(
    customer_id: str,
    limit: str = "10"
):
    """
    Retrieve recent transactions for a customer.
    """

    try:
        limit = int(limit)
    except Exception:
        limit = 10

    query = """
    SELECT
        t.TXN_ID,
        t.TX_DATETIME,
        t.TX_AMOUNT,
        m.merchant,
        tt.debit_credit
    FROM card c
    JOIN "transaction" t
        ON c.card_number = t.CARD_ID
    LEFT JOIN merchant m
        ON t.M_ID = m.id
    LEFT JOIN transaction_type tt
        ON t.TXN_TYPE_ID = tt.txn_type_id
    WHERE c.cust_id = ?
    ORDER BY t.TX_DATETIME DESC
    LIMIT ?
    """

    transactions = execute_query(
        query,
        (customer_id, limit)
    )

    return {
    "tool_used": "get_customer_transactions",
    "records_found": len(transactions),
    "answer": transactions,
    "sensitive_data_masked": True
}


# Tool 5

@tool
def search_transactions(
    merchant_name: str = "",
    min_amount: float = 0,
    limit: int = 20
):
    """
    Search transactions using merchant name and amount filters.

    """

    query = """
    SELECT
        t.TXN_ID,
        t.TX_DATETIME,
        t.TX_AMOUNT,
        m.merchant,
        tt.debit_credit
    FROM "transaction" t
    LEFT JOIN merchant m
        ON t.M_ID = m.id
    LEFT JOIN transaction_type tt
        ON t.TXN_TYPE_ID = tt.txn_type_id
    WHERE 1=1
    """

    params = []

    if merchant_name:

        query += """
        AND LOWER(m.merchant)
        LIKE LOWER(?)
        """

        params.append(
            f"%{merchant_name}%"
        )

    if min_amount > 0:

        query += """
        AND t.TX_AMOUNT >= ?
        """

        params.append(min_amount)

    query += """
    ORDER BY t.TX_AMOUNT DESC
    LIMIT ?
    """

    params.append(limit)

    rows = execute_query(
        query,
        tuple(params)
    )

    return {
    "tool_used": "search_transactions",
    "records_found": len(rows),
    "answer": rows,
    "sensitive_data_masked": True
}

# Tool 6

@tool
def get_merchant_spend_summary():
    """
    Generate merchant spend aggregation summary.
    """

    query = """
    SELECT
        mt.merchant_type,
        SUM(t.TX_AMOUNT) AS total_spend,
        COUNT(*) AS transaction_count
    FROM "transaction" t
    JOIN merchant m
        ON t.M_ID = m.id
    JOIN merchant_type mt
        ON m.merchant_type = mt.id
    GROUP BY mt.merchant_type
    ORDER BY total_spend DESC
    """

    results = execute_query(query)

    return {
        "tool_used": "get_merchant_spend_summary",
        "records_found": len(results),
        "answer": results,
        "sensitive_data_masked": True
    }

# Tool 7

@tool
def detect_suspicious_transactions():
    """
    Identify potentially suspicious transactions using rule-based checks.

    """

    query = """
    SELECT
        TXN_ID,
        TX_AMOUNT
    FROM "transaction"
    WHERE TX_AMOUNT > 75000
    ORDER BY TX_AMOUNT DESC
    """

    rows = execute_query(query)

    flagged = []

    for row in rows:

        flagged.append(
            {
                "txn_id": row["TXN_ID"],
                "amount": row["TX_AMOUNT"],
                "reason": "High-value transaction"
            }
        )

    return {
    "tool_used": "detect_suspicious_transactions",
    "records_found": len(flagged),
    "answer": flagged,
    "sensitive_data_masked": True
}

# Tool 8

@tool
def get_cards_expiring_soon(days: str = "60"):
    """
    Find cards expiring within the specified number of days.
    """

    try:
        days = int(days)
    except Exception:
        days = 60

    query = """
    SELECT
        card_number,
        expiry,
        cust_id
    FROM card
    """

    cards = execute_query(query)

    today = datetime.today()
    threshold = today + timedelta(days=days)

    expiring_cards = []

    for card in cards:

        try:
            expiry_date = datetime.strptime(
                card["expiry"],
                "%Y-%m-%d"
            )

            if today <= expiry_date <= threshold:

                expiring_cards.append(
                    {
                        "card_number": mask_card(
                            str(card["card_number"])
                        ),
                        "expiry": card["expiry"],
                        "cust_id": card["cust_id"]
                    }
                )

        except Exception:
            continue

    return {
        "tool_used": "get_cards_expiring_soon",
        "records_found": len(expiring_cards),
        "answer": expiring_cards,
        "sensitive_data_masked": True
    }

# Tool 9

@tool
def get_statement_summary(customer_id: str):
    """Get statement summary."""

# Tool 10

@tool
def get_rewards_summary(customer_id: str):
    """Get rewards summary."""    

# Tool Registery

TOOLS = [
    inspect_database_schema,
    get_customer_profile,
    get_card_details,
    search_transactions,
    get_customer_transactions,
    get_merchant_spend_summary,
    detect_suspicious_transactions,
    get_cards_expiring_soon, 
    get_statement_summary,
    get_rewards_summary
]