from db_utils import run_query, mask_card_number, mask_contact


def inspect_database_schema() -> dict:
    """
    Returns the list of tables and their columns in the ccms.db database.
    Use this tool when the user asks what data is available, or when you
    need to confirm a table/column name before answering a schema question.
    This tool only inspects metadata -- it never runs user-provided SQL.
    """
    from db_utils import list_tables, table_columns

    tables = list_tables()
    schema = {t: table_columns(t) for t in tables}
    return {"tables": tables, "schema": schema}


def get_customer_profile(cust_id: str) -> dict:
    """
    Retrieves a customer's profile (name, city, state, masked email/phone)
    given their customer ID (e.g. 'CUST-1001').
    Use this tool when the customer asks for their own profile info or
    when you need to confirm which customer a card/transaction belongs to.
    """
    rows = run_query(
        "SELECT cust_id, first_name, last_name, email, phone, city, state "
        "FROM customer WHERE cust_id = ?;",
        (cust_id,),
    )
    if not rows:
        return {"found": False, "message": f"No customer found with ID '{cust_id}'."}

    r = rows[0]
    return {
        "found": True,
        "customer": {
            "cust_id": r["cust_id"],
            "name": f"{r['first_name']} {r['last_name']}",
            "email": mask_contact(r.get("email")),
            "phone": mask_contact(r.get("phone")),
            "city": r.get("city"),
            "state": r.get("state"),
        },
    }


def get_card_details(cust_id: str) -> dict:
    """
    Retrieves card details (type, masked card number, status, expiry) for a
    given customer ID. Never returns the full card number, CVV, or
    netbanking password.
    Use this tool when the customer asks about their card type, status, or
    which cards they hold.
    """
    rows = run_query(
        "SELECT card_id, card_number, card_type, expiry_date, status "
        "FROM card WHERE cust_id = ?;",
        (cust_id,),
    )
    if not rows:
        return {"found": False, "message": f"No cards found for customer '{cust_id}'."}

    cards = [
        {
            "card_id": r["card_id"],
            "card_number": mask_card_number(r.get("card_number")),
            "card_type": r.get("card_type"),
            "expiry_date": r.get("expiry_date"),
            "status": r.get("status"),
        }
        for r in rows
    ]
    return {"found": True, "count": len(cards), "cards": cards}


def search_transactions(
    cust_id: str = None,
    min_amount: float = None,
    max_amount: float = None,
    from_date: str = None,
    to_date: str = None,
    transaction_type: str = None,
    limit: int = 10,
) -> dict:
    """
    Searches transactions with optional filters: customer ID, amount range,
    date range (YYYY-MM-DD), and transaction type (e.g. 'Debit'/'Credit').
    Results are limited (default 10, capped at 50) and ordered by most recent.
    Use this tool for questions like "show my last N transactions",
    "list transactions above X", or "show transactions for customer Y".
    """
    limit = max(1, min(int(limit or 10), 50))

    query = (
        "SELECT t.txn_id, t.txn_datetime, t.amount, m.merchant_name, "
        "t.transaction_type, t.remarks "
        "FROM 'transaction' t "
        "JOIN card c ON t.card_id = c.card_id "
        "LEFT JOIN merchant m ON t.merchant_id = m.merchant_id "
        "WHERE 1=1"
    )
    params: list = []

    if cust_id:
        query += " AND c.cust_id = ?"
        params.append(cust_id)
    if min_amount is not None:
        query += " AND t.amount >= ?"
        params.append(min_amount)
    if max_amount is not None:
        query += " AND t.amount <= ?"
        params.append(max_amount)
    if from_date:
        query += " AND t.txn_datetime >= ?"
        params.append(from_date)
    if to_date:
        query += " AND t.txn_datetime <= ?"
        params.append(to_date)
    if transaction_type:
        query += " AND t.transaction_type = ?"
        params.append(transaction_type)

    query += " ORDER BY t.txn_datetime DESC LIMIT ?;"
    params.append(limit)

    rows = run_query(query, tuple(params))
    return {"count": len(rows), "transactions": rows}


def get_customer_transactions(cust_id: str, limit: int = 5) -> dict:
    """
    Returns the most recent transactions (default 5) for a given customer ID.
    Use this tool when the customer asks to see their recent activity
    (e.g. "show my last 5 transactions").
    """
    result = search_transactions(cust_id=cust_id, limit=limit)
    return {
        "customer_id": cust_id,
        "transaction_count": result["count"],
        "transactions": result["transactions"],
    }


def get_statement_summary(cust_id: str) -> dict:
    """
    Returns the latest statement summary (amount due, minimum due, statement
    date, due date, and a simple risk level) for a given customer ID.
    Use this tool for questions about dues, minimum payment, or statement
    dates.
    """
    rows = run_query(
        "SELECT s.total_amount_due, s.min_amount_due, s.statement_date, "
        "s.due_date "
        "FROM statement s "
        "JOIN card c ON s.card_id = c.card_id "
        "WHERE c.cust_id = ? "
        "ORDER BY s.statement_date DESC LIMIT 1;",
        (cust_id,),
    )
    if not rows:
        return {"found": False, "message": f"No statement found for customer '{cust_id}'."}

    r = rows[0]
    due = r.get("total_amount_due") or 0
    risk = "HIGH" if due > 50000 else "MEDIUM" if due > 10000 else "LOW"
    return {
        "found": True,
        "customer_id": cust_id,
        "total_amount_due": due,
        "min_amount_due": r.get("min_amount_due"),
        "statement_date": r.get("statement_date"),
        "due_date": r.get("due_date"),
        "risk_level": risk,
    }


def get_rewards_summary(cust_id: str) -> dict:
    """
    Returns the total reward points earned by a customer and the related
    transactions that generated them.
    Use this tool for questions about reward points or reward-generating
    purchases.
    """
    rows = run_query(
        "SELECT r.txn_id, r.points_earned "
        "FROM rewards r "
        "JOIN card c ON r.card_id = c.card_id "
        "WHERE c.cust_id = ?;",
        (cust_id,),
    )
    total_points = sum(r.get("points_earned", 0) or 0 for r in rows)
    return {
        "customer_id": cust_id,
        "reward_points": total_points,
        "related_transactions": [r["txn_id"] for r in rows],
    }


def get_merchant_spend_summary(group_by: str = "merchant_type", limit: int = 10) -> dict:
    """
    Aggregates total transaction amount and count, grouped either by
    'merchant_type' or by 'merchant' (merchant name). Returns the top
    results ordered by total spend, descending.
    Use this tool for analytical questions like "which merchants have the
    highest spend" or "show spend summary by merchant type".
    """
    limit = max(1, min(int(limit or 10), 50))

    if group_by not in ("merchant_type", "merchant"):
        group_by = "merchant_type"

    column = "m.merchant_type" if group_by == "merchant_type" else "m.merchant_name"

    rows = run_query(
        f"SELECT {column} AS group_value, SUM(t.amount) AS total_spend, "
        "COUNT(*) AS transaction_count "
        "FROM 'transaction' t "
        "JOIN merchant m ON t.merchant_id = m.merchant_id "
        f"GROUP BY {column} "
        "ORDER BY total_spend DESC "
        "LIMIT ?;",
        (limit,),
    )
    return {"group_by": group_by, "results": rows}


def detect_suspicious_transactions(amount_threshold: float = 75000, limit: int = 10) -> dict:
    """
    Flags potentially suspicious transactions using simple rule-based logic:
    amount above a threshold (default 75000), or remarks containing words
    like 'failed', 'declined', 'reversed', 'suspicious', or 'chargeback'.
    Use this tool for questions about fraud risk or suspicious activity.
    Results are NOT confirmed fraud -- always tell the user they require
    review by the risk/operations team.
    """
    limit = max(1, min(int(limit or 10), 50))

    rows = run_query(
        "SELECT txn_id, amount, remarks, txn_datetime "
        "FROM 'transaction' "
        "WHERE amount > ? "
        "   OR LOWER(remarks) LIKE '%failed%' "
        "   OR LOWER(remarks) LIKE '%declined%' "
        "   OR LOWER(remarks) LIKE '%reversed%' "
        "   OR LOWER(remarks) LIKE '%suspicious%' "
        "   OR LOWER(remarks) LIKE '%chargeback%' "
        "ORDER BY amount DESC "
        "LIMIT ?;",
        (amount_threshold, limit),
    )

    flagged = []
    for r in rows:
        reason = []
        if (r.get("amount") or 0) > amount_threshold:
            reason.append("High-value transaction")
        remarks = (r.get("remarks") or "").lower()
        for kw in ("failed", "declined", "reversed", "suspicious", "chargeback"):
            if kw in remarks:
                reason.append(f"Suspicious remark: '{kw}'")
        flagged.append(
            {
                "txn_id": r["txn_id"],
                "amount": r["amount"],
                "reason": "; ".join(reason) if reason else "Rule match",
            }
        )

    return {
        "rule_applied": f"amount > {amount_threshold} or suspicious remarks",
        "count": len(flagged),
        "flagged_transactions": flagged,
    }


def get_cards_expiring_soon(days: int = 60) -> dict:
    """
    Returns cards expiring within the next N days (default 60).
    Use this tool for questions like "which cards are expiring soon".
    """
    rows = run_query(
        "SELECT card_id, cust_id, card_type, expiry_date "
        "FROM card "
        "WHERE date(expiry_date) <= date('now', ? || ' days') "
        "  AND date(expiry_date) >= date('now');",
        (str(days),),
    )
    for r in rows:
        r.pop("card_number", None)
    return {"days": days, "count": len(rows), "cards": rows}


ALL_TOOLS = [
    inspect_database_schema,
    get_customer_profile,
    get_card_details,
    search_transactions,
    get_customer_transactions,
    get_statement_summary,
    get_rewards_summary,
    get_merchant_spend_summary,
    detect_suspicious_transactions,
    get_cards_expiring_soon,
]
