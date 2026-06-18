from datetime import datetime, timedelta
from langchain_core.tools import tool
from db_utils import get_connection


def _mask_email(email: str) -> str:
    if not email or "@" not in email:
        return email
    local, domain = email.split("@", 1)
    return local[0] + "****@" + domain


def _mask_phone(phone: str) -> str:
    if not phone:
        return "****"
    phone = str(phone).strip()
    if len(phone) <= 4:
        return "****"
    return phone[:2] + "****" + phone[-2:]


def _mask_card_number(card_number) -> str:
    s = str(card_number).strip()
    return "**** **** **** " + s[-4:]


def _parse_cust_id(value: str):
    if value is None:
        return None
    value = str(value).strip()
    if value.isdigit():
        return int(value)
    upper = value.upper()
    if upper.startswith("CUST-"):
        suffix = value[5:]
        if suffix.isdigit():
            return int(suffix)
    return None


@tool
def inspect_database_schema() -> dict:
    """Returns all table names and their column names from the ccms.db database schema. Use this tool first to understand what data is available before answering any question."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    schema = {}
    for table in tables:
        cursor.execute(f'PRAGMA table_info("{table}")')
        schema[table] = [row[1] for row in cursor.fetchall()]
    conn.close()
    return {"tables": tables, "schema": schema}


@tool
def get_customer_profile(search_value: str) -> dict:
    """Finds a customer profile by customer ID number, email address, phone number, first name, or last name. Pass the customer ID as a plain number such as 1 or 42. Email and phone are masked in the response."""
    conn = get_connection()
    cursor = conn.cursor()
    cust_id_int = _parse_cust_id(search_value)

    if cust_id_int is not None:
        cursor.execute(
            """
            SELECT cust_id, first_name, last_name, email, phone, city, state
            FROM customer
            WHERE cust_id = ?
            """,
            (cust_id_int,),
        )
    else:
        cursor.execute(
            """
            SELECT cust_id, first_name, last_name, email, phone, city, state
            FROM customer
            WHERE email = ?
            OR phone = ?
            OR first_name LIKE ?
            OR last_name LIKE ?
            """,
            (search_value, search_value, f"%{search_value}%", f"%{search_value}%"),
        )

    row = cursor.fetchone()
    conn.close()

    if not row:
        return {"found": False, "customer": None}

    return {
        "found": True,
        "customer": {
            "cust_id": row[0],
            "name": f"{row[1]} {row[2]}",
            "email": _mask_email(row[3]),
            "phone": _mask_phone(str(row[4]) if row[4] else ""),
            "city": row[5],
            "state": row[6],
        },
    }


@tool
def get_card_details(customer_id: str) -> dict:
    """Returns all card details for a customer. Pass the customer ID as a plain number. Full card number, security code, and passwords are never returned. Only the last 4 digits are shown."""
    conn = get_connection()
    cursor = conn.cursor()
    cust_id_int = _parse_cust_id(customer_id)

    if cust_id_int is None:
        return {"found": False, "cards": []}

    cursor.execute(
        """
        SELECT c.card_number, c.valid_from, c.expiry, c.cust_id,
               ct.card_type, ct.card_network, ct.privilege
        FROM card c
        JOIN card_type ct ON c.card_type_id = ct.card_type_id
        WHERE c.cust_id = ?
        """,
        (cust_id_int,),
    )

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return {"found": False, "cards": []}

    cards = [
        {
            "card_number": _mask_card_number(row[0]),
            "valid_from": row[1],
            "expiry": row[2],
            "cust_id": row[3],
            "card_type": row[4],
            "card_network": row[5],
            "privilege": row[6],
        }
        for row in rows
    ]

    return {"found": True, "cards": cards}


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
    limit: int = 10,
) -> dict:
    """Searches transactions using optional filters. transaction_type accepts Debit or Credit. merchant_type accepts a category name such as supermarket or electronics specialty. Dates must be in YYYY-MM-DD format. customer_id must be a plain number."""
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT t.TXN_ID, t.TX_DATETIME, t.TX_AMOUNT, m.merchant,
               tt.debit_credit, tt.lcl_intnl, mt.merchant_type
        FROM "transaction" t
        LEFT JOIN merchant m ON t.M_ID = m.id
        LEFT JOIN merchant_type mt ON m.merchant_type = mt.id
        LEFT JOIN transaction_type tt ON t.TXN_TYPE_ID = tt.txn_type_id
        LEFT JOIN card c ON t.CARD_ID = c.card_number
        WHERE 1=1
    """
    params = []

    if customer_id:
        cust_id_int = _parse_cust_id(customer_id)
        if cust_id_int is not None:
            query += " AND c.cust_id = ?"
            params.append(cust_id_int)

    if card_last4:
        query += " AND CAST(c.card_number AS TEXT) LIKE ?"
        params.append(f"%{card_last4}")

    if merchant_name:
        query += " AND m.merchant LIKE ?"
        params.append(f"%{merchant_name}%")

    if merchant_type:
        query += " AND mt.merchant_type LIKE ?"
        params.append(f"%{merchant_type}%")

    if transaction_type:
        query += " AND tt.debit_credit = ?"
        params.append(transaction_type)

    if min_amount is not None:
        query += " AND t.TX_AMOUNT >= ?"
        params.append(min_amount)

    if max_amount is not None:
        query += " AND t.TX_AMOUNT <= ?"
        params.append(max_amount)

    if from_date:
        query += " AND t.TX_DATETIME >= ?"
        params.append(from_date)

    if to_date:
        query += " AND t.TX_DATETIME <= ?"
        params.append(to_date)

    query += " ORDER BY t.TX_DATETIME DESC LIMIT ?"
    params.append(limit)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    transactions = [
        {
            "txn_id": row[0],
            "txn_datetime": row[1],
            "amount": row[2],
            "merchant": row[3],
            "transaction_type": row[4],
            "locality": row[5],
            "merchant_category": row[6],
        }
        for row in rows
    ]

    return {"count": len(transactions), "transactions": transactions}


@tool
def get_customer_transactions(customer_id: str, limit: int = 10) -> dict:
    """Returns recent transactions for a specific customer ordered by date descending. Pass customer_id as a plain number."""
    conn = get_connection()
    cursor = conn.cursor()
    cust_id_int = _parse_cust_id(customer_id)

    if cust_id_int is None:
        return {"customer_id": customer_id, "transaction_count": 0, "transactions": []}

    cursor.execute(
        """
        SELECT t.TXN_ID, t.TX_DATETIME, t.TX_AMOUNT, m.merchant,
               tt.debit_credit, mt.merchant_type
        FROM "transaction" t
        LEFT JOIN card c ON t.CARD_ID = c.card_number
        LEFT JOIN merchant m ON t.M_ID = m.id
        LEFT JOIN merchant_type mt ON m.merchant_type = mt.id
        LEFT JOIN transaction_type tt ON t.TXN_TYPE_ID = tt.txn_type_id
        WHERE c.cust_id = ?
        ORDER BY t.TX_DATETIME DESC
        LIMIT ?
        """,
        (cust_id_int, limit),
    )

    rows = cursor.fetchall()
    conn.close()

    transactions = [
        {
            "txn_id": row[0],
            "txn_datetime": row[1],
            "amount": row[2],
            "merchant": row[3],
            "transaction_type": row[4],
            "merchant_category": row[5],
        }
        for row in rows
    ]

    return {
        "customer_id": customer_id,
        "transaction_count": len(transactions),
        "transactions": transactions,
    }


@tool
def get_statement_summary(customer_id: str) -> dict:
    """Returns a statement and dues summary for a customer based on their debit transaction history. Risk level is LOW, MEDIUM, or HIGH. Pass customer_id as a plain number."""
    conn = get_connection()
    cursor = conn.cursor()
    cust_id_int = _parse_cust_id(customer_id)

    if cust_id_int is None:
        return {
            "customer_id": customer_id,
            "total_amount_due": 0,
            "min_amount_due": 0,
            "statement_date": None,
            "due_date": None,
            "risk_level": "LOW",
        }

    cursor.execute(
        """
        SELECT SUM(t.TX_AMOUNT), MAX(t.TX_DATETIME)
        FROM "transaction" t
        JOIN card c ON t.CARD_ID = c.card_number
        JOIN transaction_type tt ON t.TXN_TYPE_ID = tt.txn_type_id
        WHERE c.cust_id = ? AND tt.debit_credit = 'Debit'
        """,
        (cust_id_int,),
    )

    row = cursor.fetchone()
    conn.close()

    if not row or row[0] is None:
        return {
            "customer_id": customer_id,
            "total_amount_due": 0,
            "min_amount_due": 0,
            "statement_date": None,
            "due_date": None,
            "risk_level": "LOW",
        }

    total_due = round(row[0], 2)
    statement_date = row[1]
    min_due = round(total_due * 0.05, 2)

    if total_due >= 100000:
        risk = "HIGH"
    elif total_due >= 50000:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    try:
        stmt_dt = datetime.strptime(statement_date[:10], "%Y-%m-%d")
        due_date = (stmt_dt + timedelta(days=30)).strftime("%Y-%m-%d")
    except Exception:
        due_date = None

    return {
        "customer_id": customer_id,
        "total_amount_due": total_due,
        "min_amount_due": min_due,
        "statement_date": statement_date,
        "due_date": due_date,
        "risk_level": risk,
    }


@tool
def get_rewards_summary(customer_id: str) -> dict:
    """Returns reward points earned by a customer. Points are calculated as 1 point per 100 units spent on debit transactions only. Returns the 50 most recent qualifying transactions. Pass customer_id as a plain number."""
    conn = get_connection()
    cursor = conn.cursor()
    cust_id_int = _parse_cust_id(customer_id)

    if cust_id_int is None:
        return {"customer_id": customer_id, "reward_points": 0, "related_transactions": []}

    cursor.execute(
        """
        SELECT t.TXN_ID, t.TX_AMOUNT, t.TX_DATETIME, m.merchant
        FROM "transaction" t
        JOIN card c ON t.CARD_ID = c.card_number
        JOIN transaction_type tt ON t.TXN_TYPE_ID = tt.txn_type_id
        LEFT JOIN merchant m ON t.M_ID = m.id
        WHERE c.cust_id = ? AND tt.debit_credit = 'Debit'
        ORDER BY t.TX_DATETIME DESC
        LIMIT 50
        """,
        (cust_id_int,),
    )

    rows = cursor.fetchall()
    conn.close()

    reward_points = 0
    related_transactions = []

    for row in rows:
        points = int(row[1] // 100)
        reward_points += points
        related_transactions.append(
            {
                "txn_id": row[0],
                "amount": row[1],
                "txn_datetime": row[2],
                "merchant": row[3],
                "earned_points": points,
            }
        )

    return {
        "customer_id": customer_id,
        "reward_points": reward_points,
        "related_transactions": related_transactions,
    }


@tool
def get_merchant_spend_summary(group_by: str = "merchant_type") -> dict:
    """Aggregates total transaction amounts grouped by merchant name or merchant category. group_by accepts merchant or merchant_type."""
    conn = get_connection()
    cursor = conn.cursor()

    if group_by == "merchant":
        cursor.execute(
            """
            SELECT m.merchant, SUM(t.TX_AMOUNT), COUNT(t.TXN_ID)
            FROM "transaction" t
            JOIN merchant m ON t.M_ID = m.id
            GROUP BY m.merchant
            ORDER BY SUM(t.TX_AMOUNT) DESC
            LIMIT 20
            """
        )
    else:
        cursor.execute(
            """
            SELECT mt.merchant_type, SUM(t.TX_AMOUNT), COUNT(t.TXN_ID)
            FROM "transaction" t
            JOIN merchant m ON t.M_ID = m.id
            JOIN merchant_type mt ON m.merchant_type = mt.id
            GROUP BY mt.merchant_type
            ORDER BY SUM(t.TX_AMOUNT) DESC
            """
        )

    rows = cursor.fetchall()
    conn.close()

    if group_by == "merchant":
        results = [
            {"merchant": row[0], "total_spend": round(row[1], 2), "transaction_count": row[2]}
            for row in rows
        ]
    else:
        results = [
            {"merchant_type": row[0], "total_spend": round(row[1], 2), "transaction_count": row[2]}
            for row in rows
        ]

    return {"group_by": group_by, "results": results}


@tool
def get_notification_summary(customer_id: str = None) -> dict:
    """Returns notification and transaction alert information. Note: the notification table is not present in the current version of ccms.db."""
    return {
        "status": "unavailable",
        "message": "Notification records are not available in the current database version.",
        "customer_id": customer_id,
    }


@tool
def detect_suspicious_transactions(limit: int = 50) -> dict:
    """Detects potentially suspicious transactions using rule-based logic. Rules: transaction amount above 75000, multiple transactions above 50000 on the same card, and terminal location significantly distant from the card holder typical area. These are potential flags only and require human review."""
    conn = get_connection()
    cursor = conn.cursor()

    flagged = {}

    cursor.execute(
        """
        SELECT t.TXN_ID, t.CARD_ID, t.TX_AMOUNT, t.TX_DATETIME
        FROM "transaction" t
        WHERE t.TX_AMOUNT > 75000
        ORDER BY t.TX_AMOUNT DESC
        LIMIT ?
        """,
        (limit,),
    )

    for row in cursor.fetchall():
        txn_id = row[0]
        if txn_id not in flagged:
            flagged[txn_id] = {
                "txn_id": row[0],
                "card_id": _mask_card_number(row[1]),
                "amount": row[2],
                "txn_datetime": row[3],
                "reasons": [],
            }
        flagged[txn_id]["reasons"].append("Transaction amount exceeds 75000")

    cursor.execute(
        """
        SELECT t.TXN_ID, t.CARD_ID, t.TX_AMOUNT, t.TX_DATETIME
        FROM "transaction" t
        WHERE t.CARD_ID IN (
            SELECT CARD_ID FROM "transaction"
            WHERE TX_AMOUNT > 50000
            GROUP BY CARD_ID
            HAVING COUNT(*) >= 2
        )
        AND t.TX_AMOUNT > 50000
        ORDER BY t.TX_AMOUNT DESC
        LIMIT ?
        """,
        (limit,),
    )

    for row in cursor.fetchall():
        txn_id = row[0]
        if txn_id not in flagged:
            flagged[txn_id] = {
                "txn_id": row[0],
                "card_id": _mask_card_number(row[1]),
                "amount": row[2],
                "txn_datetime": row[3],
                "reasons": [],
            }
        reason = "Multiple high-value transactions on the same card"
        if reason not in flagged[txn_id]["reasons"]:
            flagged[txn_id]["reasons"].append(reason)

    cursor.execute(
        """
        SELECT t.TXN_ID, t.CARD_ID, t.TX_AMOUNT, t.TX_DATETIME,
               ABS(tt.x_terminal_id - c."x-coordinate") + ABS(tt.y_terminal_id - c."y-coordinate") AS location_diff
        FROM "transaction" t
        JOIN transaction_terminal tt ON t.TERMINAL_ID = tt.TERMINAL_ID
        JOIN card c ON t.CARD_ID = c.card_number
        WHERE (ABS(tt.x_terminal_id - c."x-coordinate") + ABS(tt.y_terminal_id - c."y-coordinate")) > 50
        ORDER BY location_diff DESC
        LIMIT ?
        """,
        (limit,),
    )

    for row in cursor.fetchall():
        txn_id = row[0]
        if txn_id not in flagged:
            flagged[txn_id] = {
                "txn_id": row[0],
                "card_id": _mask_card_number(row[1]),
                "amount": row[2],
                "txn_datetime": row[3],
                "reasons": [],
            }
        reason = "Terminal location deviates significantly from card holder area"
        if reason not in flagged[txn_id]["reasons"]:
            flagged[txn_id]["reasons"].append(reason)

    conn.close()

    result_list = [
        {
            "txn_id": entry["txn_id"],
            "card_id": entry["card_id"],
            "amount": entry["amount"],
            "txn_datetime": entry["txn_datetime"],
            "reason": ", ".join(entry["reasons"]),
        }
        for entry in flagged.values()
    ]

    result_list.sort(key=lambda x: x["amount"], reverse=True)

    return {
        "rules_applied": [
            "Transaction amount greater than 75000",
            "Multiple transactions above 50000 on the same card",
            "Terminal location deviates significantly from card holder area",
        ],
        "count": len(result_list),
        "flagged_transactions": result_list[:limit],
    }


@tool
def get_cards_expiring_soon(days: int = 60, limit: int = 20) -> dict:
    """Returns cards that are expiring within the specified number of days. Defaults to 60 days. Card numbers are masked in the response."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT c.card_number, c.expiry, c.cust_id,
               ct.card_type, ct.card_network,
               cu.first_name, cu.last_name
        FROM card c
        JOIN card_type ct ON c.card_type_id = ct.card_type_id
        JOIN customer cu ON c.cust_id = cu.cust_id
        WHERE date(c.expiry) <= date('now', ?)
        AND date(c.expiry) >= date('now')
        ORDER BY c.expiry
        LIMIT ?
        """,
        (f"+{days} days", limit),
    )

    rows = cursor.fetchall()
    conn.close()

    cards = [
        {
            "card_number": _mask_card_number(row[0]),
            "expiry": row[1],
            "cust_id": row[2],
            "card_type": row[3],
            "card_network": row[4],
            "customer_name": f"{row[5]} {row[6]}",
        }
        for row in rows
    ]

    return {"days_window": days, "count": len(cards), "expiring_cards": cards}


@tool
def get_top_customers_by_due(limit: int = 10) -> dict:
    """Returns customers ranked by their total debit transaction spend, representing customers with the highest potential outstanding dues."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT cu.cust_id, cu.first_name, cu.last_name, cu.city, cu.state,
               SUM(t.TX_AMOUNT) AS total_due, COUNT(t.TXN_ID) AS txn_count
        FROM "transaction" t
        JOIN card c ON t.CARD_ID = c.card_number
        JOIN customer cu ON c.cust_id = cu.cust_id
        JOIN transaction_type tt ON t.TXN_TYPE_ID = tt.txn_type_id
        WHERE tt.debit_credit = 'Debit'
        GROUP BY cu.cust_id, cu.first_name, cu.last_name, cu.city, cu.state
        ORDER BY total_due DESC
        LIMIT ?
        """,
        (limit,),
    )

    rows = cursor.fetchall()
    conn.close()

    customers = [
        {
            "cust_id": row[0],
            "name": f"{row[1]} {row[2]}",
            "city": row[3],
            "state": row[4],
            "total_due": round(row[5], 2),
            "transaction_count": row[6],
        }
        for row in rows
    ]

    return {"count": len(customers), "top_customers": customers}


@tool
def get_transaction_type_summary() -> dict:
    """Returns a summary of all transactions grouped by type showing Debit vs Credit and Local vs International counts and total amounts."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT tt.debit_credit, tt.lcl_intnl, COUNT(t.TXN_ID), SUM(t.TX_AMOUNT)
        FROM "transaction" t
        JOIN transaction_type tt ON t.TXN_TYPE_ID = tt.txn_type_id
        GROUP BY tt.debit_credit, tt.lcl_intnl
        ORDER BY SUM(t.TX_AMOUNT) DESC
        """
    )

    rows = cursor.fetchall()
    conn.close()

    results = [
        {
            "transaction_type": row[0],
            "locality": row[1],
            "count": row[2],
            "total_amount": round(row[3], 2),
        }
        for row in rows
    ]

    return {"summary": results}
