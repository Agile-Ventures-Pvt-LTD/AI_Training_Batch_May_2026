from langchain_core.tools import tool
from db_utils import execute_query
import sqlite3

DB_PATH = "data/ccms.db"

from langchain_core.tools import tool
import sqlite3
import json
import os

DB_PATH = "data/ccms.db"

@tool
def inspect_database_schema():
    """
    Inspect database schema.
    Returns all table names and their columns.
    Does NOT execute arbitrary SQL.
    """

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table';"
    )

    tables = [row[0] for row in cursor.fetchall()]

    schema = {}

    for table in tables:

        cursor.execute(
            f'PRAGMA table_info("{table}")'
        )

        schema[table] = [
            col[1]
            for col in cursor.fetchall()
        ]

    conn.close()

    result = {
        "tables": tables,
        "schema": schema
    }

    os.makedirs("tool_outputs", exist_ok=True)

    with open(
        "tool_outputs/schema_output.json",
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            result,
            f,
            indent=4
        )

    return result


@tool
def get_customer_profile(
    cust_id: str = None,
    email: str = None,
    phone: str = None,
    name: str = None
):
    """
    Find customer profile using
    customer id, email, phone or name.
    """

    query = None
    params = ()

    if cust_id:

        query = """
        SELECT *
        FROM customer
        WHERE cust_id = ?
        """

        params = (cust_id,)

    elif email:

        query = """
        SELECT *
        FROM customer
        WHERE email = ?
        """

        params = (email,)

    elif phone:

        query = """
        SELECT *
        FROM customer
        WHERE phone = ?
        """

        params = (phone,)

    elif name:

        query = """
        SELECT *
        FROM customer
        WHERE LOWER(first_name || ' ' || last_name)
              LIKE LOWER(?)
        """

        params = (f"%{name}%",)

    else:

        return {
            "found": False,
            "message": "No search criteria provided."
        }

    rows = execute_query(query, params)

    if not rows:

        return {
            "found": False,
            "customer": None
        }

    customer = rows[0]

    return {
        "found": True,
        "customer": {
            "cust_id": customer["cust_id"],
            "name": f"{customer['first_name']} {customer['last_name']}",
            "email": customer["email"],
            "phone": customer["phone"],
            "city": customer["city"],
            "state": customer["state"]
        }
    }

@tool
def get_card_details(
    cust_id: str = None,
    card_number: str = None
):
    """
    Get card details for a customer.

    Sensitive fields such as full card number
    and security code are never returned.
    """

    if cust_id:

        query = """
        SELECT
            c.card_number,
            c.valid_from,
            c.expiry,
            ct.card_type,
            ct.card_network,
            ct.privilege

        FROM card c

        JOIN card_type ct
            ON c.card_type_id = ct.card_type_id

        WHERE c.cust_id = ?
        """

        params = (cust_id,)

    elif card_number:

        query = """
        SELECT
            c.card_number,
            c.valid_from,
            c.expiry,
            ct.card_type,
            ct.card_network,
            ct.privilege

        FROM card c

        JOIN card_type ct
            ON c.card_type_id = ct.card_type_id

        WHERE c.card_number = ?
        """

        params = (card_number,)

    else:

        return {
            "found": False,
            "message": "Provide cust_id or card_number."
        }

    rows = execute_query(query, params)

    if not rows:

        return {
            "found": False,
            "card": None
        }

    card = rows[0]

    card_num = str(card["card_number"])

    masked_card = (
        "**** **** **** "
        + card_num[-4:]
    )

    return {
        "found": True,
        "card": {
            "card_number": masked_card,
            "valid_from": card["valid_from"],
            "expiry": card["expiry"],
            "card_type": card["card_type"],
            "card_network": card["card_network"],
            "privilege": card["privilege"]
        }
    }
       
@tool
def search_transactions(
    customer_id: str = None,
    card_last4: str = None,
    merchant_name: str = None,
    merchant_type: str = None,
    min_amount: float = None,
    max_amount: float = None,
    from_date: str = None,
    to_date: str = None,
    transaction_type: str = None,
    limit: str = 20
):
    """
    Search transactions using filters.
    """

    query = """
    SELECT
        t.TXN_ID,
        t.TX_DATETIME,
        t.TX_AMOUNT,
        m.merchant,
        tt.debit_credit

    FROM "transaction" t

    JOIN card c
        ON t.CARD_ID = c.card_number

    LEFT JOIN merchant m
        ON t.M_ID = m.id

    LEFT JOIN merchant_type mt
        ON m.merchant_type = mt.id

    LEFT JOIN transaction_type tt
        ON t.TXN_TYPE_ID = tt.txn_type_id

    WHERE 1=1
    """

    params = []

    # customer id
    if customer_id:
        query += " AND c.cust_id = ? "
        params.append(customer_id)

    # card last 4 digits
    if card_last4:
        query += " AND CAST(c.card_number AS TEXT) LIKE ? "
        params.append(f"%{card_last4}")

    # merchant name
    if merchant_name:
        query += " AND LOWER(m.merchant) LIKE LOWER(?) "
        params.append(f"%{merchant_name}%")

    # merchant type
    if merchant_type:
        query += " AND LOWER(mt.merchant_type) LIKE LOWER(?) "
        params.append(f"%{merchant_type}%")

    # amount filters
    if min_amount is not None:
        query += " AND t.TX_AMOUNT >= ? "
        params.append(min_amount)

    if max_amount is not None:
        query += " AND t.TX_AMOUNT <= ? "
        params.append(max_amount)

    # date filters
    if from_date:
        query += " AND DATE(t.TX_DATETIME) >= DATE(?) "
        params.append(from_date)

    if to_date:
        query += " AND DATE(t.TX_DATETIME) <= DATE(?) "
        params.append(to_date)

    # debit / credit
    if transaction_type:
        query += " AND LOWER(tt.debit_credit) = LOWER(?) "
        params.append(transaction_type)

    query += """
    ORDER BY t.TX_DATETIME DESC
    LIMIT ?
    """

    params.append(limit)

    rows = execute_query(query, tuple(params))

    transactions = []

    for row in rows:

        transactions.append(
            {
                "txn_id": row["TXN_ID"],
                "txn_datetime": row["TX_DATETIME"],
                "amount": row["TX_AMOUNT"],
                "merchant": row["merchant"],
                "transaction_type": row["debit_credit"],
                "remarks": "Transaction record"
            }
        )

    return {
        "count": len(transactions),
        "transactions": transactions
    }


@tool
def get_customer_transactions(
    customer_id: str,
    limit: str = 10
):
    """
    Return recent transactions for a customer.
    """

    query = """
    SELECT
        t.TXN_ID,
        t.TX_DATETIME,
        t.TX_AMOUNT,
        m.merchant,
        tt.debit_credit

    FROM "transaction" t

    JOIN card c
        ON t.CARD_ID = c.card_number

    LEFT JOIN merchant m
        ON t.M_ID = m.id

    LEFT JOIN transaction_type tt
        ON t.TXN_TYPE_ID = tt.txn_type_id

    WHERE c.cust_id = ?

    ORDER BY t.TX_DATETIME DESC

    LIMIT ?
    """

    rows = execute_query(
        query,
        (customer_id, limit)
    )

    transactions = []

    for row in rows:

        transactions.append(
            {
                "txn_id": row["TXN_ID"],
                "txn_datetime": row["TX_DATETIME"],
                "amount": row["TX_AMOUNT"],
                "merchant": row["merchant"],
                "transaction_type": row["debit_credit"]
            }
        )

    return {
        "customer_id": customer_id,
        "transaction_count": len(transactions),
        "transactions": transactions
    }

from langchain_core.tools import tool
from datetime import datetime, timedelta

@tool
def get_statement_summary(customer_id: str):
    """
    Generate statement summary and due information.
    """

    query = """
    SELECT
        ROUND(SUM(t.TX_AMOUNT),2) AS total_due,
        MAX(t.TX_DATETIME) AS last_txn_date

    FROM "transaction" t

    JOIN card c
        ON t.CARD_ID = c.card_number

    WHERE c.cust_id = ?
    """

    rows = execute_query(
        query,
        (customer_id,)
    )

    if not rows or rows[0]["total_due"] is None:

        return {
            "customer_id": customer_id,
            "total_amount_due": 0,
            "min_amount_due": 0,
            "statement_date": None,
            "due_date": None,
            "risk_level": "LOW"
        }

    total_due = float(rows[0]["total_due"])

    min_due = round(
        total_due * 0.05,
        2
    )

    statement_date = rows[0]["last_txn_date"]

    try:

        stmt_dt = datetime.fromisoformat(
            statement_date
        )

        due_date = (
            stmt_dt + timedelta(days=15)
        ).strftime("%Y-%m-%d")

    except:

        due_date = None

    if total_due > 50000:
        risk_level = "HIGH"

    elif total_due > 10000:
        risk_level = "MEDIUM"

    else:
        risk_level = "LOW"

    return {
        "customer_id": customer_id,
        "total_amount_due": total_due,
        "min_amount_due": min_due,
        "statement_date": statement_date,
        "due_date": due_date,
        "risk_level": risk_level
    }
from langchain_core.tools import tool

@tool
def get_rewards_summary(
    customer_id: str,
    limit: str = 20
):
    """
    Return reward summary for a customer.
    Reward points are estimated because
    database does not contain a rewards table.
    """

    points_query = """
    SELECT
        ROUND(
            SUM(t.TX_AMOUNT) / 100,
            0
        ) AS reward_points

    FROM "transaction" t

    JOIN card c
        ON t.CARD_ID = c.card_number

    WHERE c.cust_id = ?
    """

    points_result = execute_query(
        points_query,
        (customer_id,)
    )

    reward_points = (
        points_result[0]["reward_points"]
        if points_result and points_result[0]["reward_points"]
        else 0
    )

    txn_query = """
    SELECT
        t.TXN_ID,
        t.TX_DATETIME,
        t.TX_AMOUNT,
        m.merchant

    FROM "transaction" t

    JOIN card c
        ON t.CARD_ID = c.card_number

    LEFT JOIN merchant m
        ON t.M_ID = m.id

    WHERE c.cust_id = ?

    ORDER BY t.TX_AMOUNT DESC

    LIMIT ?
    """

    transactions = execute_query(
        txn_query,
        (customer_id, limit)
    )

    related_transactions = []

    for txn in transactions:

        related_transactions.append(
            {
                "txn_id": txn["TXN_ID"],
                "txn_datetime": txn["TX_DATETIME"],
                "amount": txn["TX_AMOUNT"],
                "merchant": txn["merchant"]
            }
        )

    return {
        "customer_id": customer_id,
        "reward_points": int(reward_points),
        "related_transactions": related_transactions
    }


@tool
def get_merchant_spend_summary(
    customer_id: str = None,
    group_by: str = "merchant_type"
):
    """
    Aggregate spending by merchant
    or merchant type.
    """

    if group_by not in ["merchant", "merchant_type"]:
        return {
            "error": "group_by must be merchant or merchant_type"
        }

    if group_by == "merchant":

        query = """
        SELECT
            m.merchant AS category,
            ROUND(SUM(t.TX_AMOUNT),2) AS total_spend,
            COUNT(*) AS transaction_count

        FROM "transaction" t

        JOIN merchant m
            ON t.M_ID = m.id

        JOIN card c
            ON t.CARD_ID = c.card_number

        WHERE 1=1
        """

        params = []

        if customer_id:
            query += " AND c.cust_id = ? "
            params.append(customer_id)

        query += """
        GROUP BY m.merchant
        ORDER BY total_spend DESC
        """

        rows = execute_query(
            query,
            tuple(params)
        )

        results = []

        for row in rows:

            results.append(
                {
                    "merchant": row["category"],
                    "total_spend": row["total_spend"],
                    "transaction_count": row["transaction_count"]
                }
            )

    else:

        query = """
        SELECT
            mt.merchant_type AS category,
            ROUND(SUM(t.TX_AMOUNT),2) AS total_spend,
            COUNT(*) AS transaction_count

        FROM "transaction" t

        JOIN merchant m
            ON t.M_ID = m.id

        JOIN merchant_type mt
            ON m.merchant_type = mt.id

        JOIN card c
            ON t.CARD_ID = c.card_number

        WHERE 1=1
        """

        params = []

        if customer_id:
            query += " AND c.cust_id = ? "
            params.append(customer_id)

        query += """
        GROUP BY mt.merchant_type
        ORDER BY total_spend DESC
        """

        rows = execute_query(
            query,
            tuple(params)
        )

        results = []

        for row in rows:

            results.append(
                {
                    "merchant_type": row["category"],
                    "total_spend": row["total_spend"],
                    "transaction_count": row["transaction_count"]
                }
            )

    return {
        "group_by": group_by,
        "results": results
    }


@tool
def detect_suspicious_transactions(
    limit: int = 50
):
    """
    Find potentially suspicious transactions.
    If customer_id is empty, scan all customers.
    """

    query = """
    SELECT TXN_ID,
           TX_AMOUNT
    FROM "transaction"
    WHERE TX_AMOUNT > 75000
    LIMIT ?
    """

    rows = execute_query(query, (limit,))

    return {
        "rule_applied": "amount > 75000",
        "count": len(rows),
        "flagged_transactions": [
            {
                "txn_id": row[0],
                "amount": row[1],
                "reason": "High-value transaction"
            }
            for row in rows
        ]
    }


available_tools = [
    inspect_database_schema,
    get_customer_profile,
    get_card_details,
    search_transactions,
    get_customer_transactions,
    get_statement_summary,
    get_rewards_summary,
    get_merchant_spend_summary,
    detect_suspicious_transactions
]