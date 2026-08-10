from langchain.tools import tool
from db_utils import execute_query
from datetime import datetime, timedelta


# inspect database schema
@tool
def inspect_database_schema():
    """list tables and schema"""

    tables_data = execute_query(
        "SELECT name FROM sqlite_master WHERE type='table';"
    )

    tables = []
    for t in tables_data:
        tables.append(t["name"])

    schema = {}

    for table in tables:
        cols_data = execute_query(
            f'PRAGMA table_info("{table}");'
        )

        cols = []
        for c in cols_data:
            cols.append(c["name"])

        schema[table] = cols

    return {
        "tables": tables,
        "schema": schema
    }


# get_customer_profile
@tool
def get_customer_profile(
    cust_id: int | str = None,
    email: str = None,
    phone: str = None,
    name: str = None
):
    """find customer by customer ID, email, phone, or name."""

    query = """
    SELECT *
    FROM customer
    WHERE 1=1
    """

    params = []

    if cust_id is not None:
        try:
            cust_id = int(cust_id)
        except (ValueError, TypeError):
            pass
        query += " AND cust_id = ?"
        params.append(cust_id)

    if email:
        query += " AND email = ?"
        params.append(email)

    if phone:
        query += " AND phone = ?"
        params.append(phone)

    if name:
        query += " AND (first_name || ' ' || last_name) LIKE ?"
        params.append(f"%{name}%")

    result = execute_query(query, tuple(params))

    if not result:
        return {"found": False, "customer": None}

    row = result[0]

    email_val = row["email"]
    phone_val = row["phone"]

    masked_email = email_val[:2] + "***" if email_val else None
    masked_phone = "****" + phone_val[-4:] if phone_val else None

    return {
        "found": True,
        "customer": {
            "cust_id": row["cust_id"],
            "name": row["first_name"] + " " + row["last_name"],
            "email": masked_email,
            "phone": masked_phone,
            "city": row["city"],
            "state": row["state"]
        }
    }


# get card info tool
@tool
def get_card_details(cust_id: int | str = None, card_number: str = None):
    """get card info by customer ID or card number."""

    query = """
    SELECT *
    FROM card
    WHERE 1=1
    """

    params = []

    if cust_id is not None:
        try:
            cust_id = int(cust_id)
        except (ValueError, TypeError):
            pass
        query += " AND cust_id = ?"
        params.append(cust_id)

    if card_number:
        query += " AND card_number = ?"
        params.append(card_number)

    result = execute_query(query, tuple(params))

    if not result:
        return {"found": False, "cards": []}

    cards = []

    for row in result:
        number = str(row["card_number"])
        masked_number = "**** **** **** " + number[-4:]

        cards.append({
            "card_number": masked_number,
            "card_type_id": row["card_type_id"],
            "expiry": row["expiry"],
            "cust_id": row["cust_id"]
        })

    return {"found": True, "cards": cards}


# search_transactions tool
@tool
def search_transactions(
    cust_id: int | str = None,
    card_id: str = None,
    min_amount: float | str = None,
    max_amount: float | str = None,
    start_date: str = None,
    end_date: str = None,
    txn_type_id: int | str = None,
    merchant_id: int | str = None,
    limit: int | str = 5
):
    """search transactions with filters"""

    try:
        limit = int(limit)
    except:
        limit = 5

    try:
        if min_amount is not None:
            min_amount = float(min_amount)
    except:
        min_amount = None

    try:
        if max_amount is not None:
            max_amount = float(max_amount)
    except:
        max_amount = None

    try:
        if txn_type_id is not None:
            txn_type_id = int(txn_type_id)
    except:
        txn_type_id = None

    try:
        if merchant_id is not None:
            merchant_id = int(merchant_id)
    except:
        merchant_id = None

    query = """
    SELECT
        t.TXN_ID,
        t.TX_DATETIME,
        t.TX_AMOUNT,
        t.CARD_ID,
        tt.debit_credit,
        tt.lcl_intnl,
        m.merchant
    FROM "transaction" t
    LEFT JOIN transaction_type tt
        ON t.TXN_TYPE_ID = tt.txn_type_id
    LEFT JOIN merchant m
        ON t.M_ID = m.id
    WHERE 1=1
    """

    params = []

    if cust_id is not None:
        try:
            cust_id = int(cust_id)
        except (ValueError, TypeError):
            pass
        cards = execute_query(
            "SELECT card_number FROM card WHERE cust_id = ?",
            (cust_id,)
        )

        if not cards:
            return {"count": 0, "transactions": []}

        card_ids = [c["card_number"] for c in cards]

        placeholders = ",".join(["?"] * len(card_ids))
        query += f" AND t.CARD_ID IN ({placeholders})"
        params.extend(card_ids)

    if card_id:
        query += " AND t.CARD_ID = ?"
        params.append(card_id)

    if min_amount is not None:
        query += " AND t.TX_AMOUNT >= ?"
        params.append(min_amount)

    if max_amount is not None:
        query += " AND t.TX_AMOUNT <= ?"
        params.append(max_amount)

    if start_date:
        query += " AND t.TX_DATETIME >= ?"
        params.append(start_date)

    if end_date:
        query += " AND t.TX_DATETIME <= ?"
        params.append(end_date)

    if txn_type_id is not None:
        query += " AND t.TXN_TYPE_ID = ?"
        params.append(txn_type_id)

    if merchant_id is not None:
        query += " AND t.M_ID = ?"
        params.append(merchant_id)

    query += " ORDER BY t.TX_DATETIME DESC LIMIT ?"
    params.append(limit)

    result = execute_query(query, tuple(params))

    if not result:
        return {"count": 0, "transactions": []}

    transactions = []

    for row in result:
        card = str(row["CARD_ID"])
        masked_card = "**** **** **** " + card[-4:]

        transactions.append({
            "txn_id": row["TXN_ID"],
            "txn_datetime": row["TX_DATETIME"],
            "merchant": row["merchant"],
            "transaction_type": row["debit_credit"],
            "transaction_scope": row["lcl_intnl"],
            "amount": row["TX_AMOUNT"],
            "card": masked_card
        })

    return {"count": len(transactions), "transactions": transactions}


# get_customer_transactions
@tool
def get_customer_transactions(cust_id: int | str, limit: int | str = 5):
    """get transactions for a customer"""

    try:
        limit = int(limit)
    except:
        limit = 5

    try:
        cust_id = int(cust_id)
    except (ValueError, TypeError):
        pass

    cards = execute_query(
        "SELECT card_number FROM card WHERE cust_id = ?",
        (cust_id,)
    )

    if not cards:
        return {"count": 0, "transactions": []}

    card_ids = [c["card_number"] for c in cards]

    placeholders = ",".join(["?"] * len(card_ids))

    query = f"""
    SELECT TXN_ID, TX_DATETIME, TX_AMOUNT, CARD_ID
    FROM "transaction"
    WHERE CARD_ID IN ({placeholders})
    ORDER BY TX_DATETIME DESC
    LIMIT ?
    """

    params = card_ids + [limit]

    result = execute_query(query, tuple(params))

    if not result:
        return {"count": 0, "transactions": []}

    transactions = []

    for row in result:
        transactions.append({
            "txn_id": row["TXN_ID"],
            "date": row["TX_DATETIME"],
            "amount": row["TX_AMOUNT"],
            "card_id": row["CARD_ID"]
        })

    return {"count": len(transactions), "transactions": transactions}


# get statement summary
@tool
def get_statement_summary(cust_id: int | str):
    """Generate a statement summary for a customer based on transaction history."""

    try:
        cust_id = int(cust_id)
    except (ValueError, TypeError):
        pass

    cards = execute_query(
        "SELECT card_number FROM card WHERE cust_id = ?",
        (cust_id,)
    )

    if not cards:
        return {
            "found": False,
            "message": f"No cards found for customer {cust_id}"
        }

    card_ids = [c["card_number"] for c in cards]

    placeholders = ",".join(["?"] * len(card_ids))

    transactions = execute_query(
        f"""
        SELECT TX_AMOUNT, TX_DATETIME
        FROM "transaction"
        WHERE CARD_ID IN ({placeholders})
        ORDER BY TX_DATETIME DESC
        """,
        tuple(card_ids)
    )

    if not transactions:
        return {
            "found": False,
            "message": f"No transactions found for customer {cust_id}"
        }

    total_due = sum(float(t["TX_AMOUNT"]) for t in transactions)

    min_due = round(total_due * 0.05, 2)

    latest_date = transactions[0]["TX_DATETIME"]

    statement_date = datetime.strptime(latest_date, "%Y-%m-%d %H:%M:%S")

    due_date = statement_date + timedelta(days=15)

    if total_due >= 50000:
        risk_level = "HIGH"
    elif total_due >= 10000:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return {
        "customer_id": cust_id,
        "total_amount_due": round(total_due, 2),
        "min_amount_due": min_due,
        "statement_date": statement_date.strftime("%Y-%m-%d"),
        "due_date": due_date.strftime("%Y-%m-%d"),
        "risk_level": risk_level
    }


# get rewards summary
@tool
def get_rewards_summary(cust_id: int | str):
    """
    Get reward points summary for a customer.
    Use this tool when the user asks:
    - reward points
    - rewards summary
    - loyalty points
    - earned points
    - points balance
    """

    try:
        cust_id = int(cust_id)
    except (ValueError, TypeError):
        pass

    cards = execute_query(
        "SELECT card_number FROM card WHERE cust_id = ?",
        (cust_id,)
    )

    if not cards:
        return {
            "customer_id": cust_id,
            "reward_points": 0,
            "related_transactions": 0
        }

    card_ids = [c["card_number"] for c in cards]

    placeholders = ",".join(["?"] * len(card_ids))

    transactions = execute_query(
        f"""
        SELECT TX_AMOUNT
        FROM "transaction"
        WHERE CARD_ID IN ({placeholders})
        """,
        tuple(card_ids)
    )

    if not transactions:
        return {
            "customer_id": cust_id,
            "reward_points": 0,
            "related_transactions": 0
        }

    total_spend = sum(float(row["TX_AMOUNT"]) for row in transactions)

    reward_points = int(total_spend // 100)

    return {
        "customer_id": cust_id,
        "reward_points": reward_points,
        "related_transactions": len(transactions)
    }


# detect suspicious transactions
@tool
def detect_suspicious_transactions(cust_id: int | str, multiplier: float | int | str = 3):
    """
    Detect potentially suspicious transactions.
    Use this tool when the user asks:
    - suspicious transactions
    - fraud detection
    - unusual spending
    - abnormal transactions
    - risky transactions
    """

    try:
        multiplier = float(multiplier)
    except:
        multiplier = 3.0

    try:
        cust_id = int(cust_id)
    except (ValueError, TypeError):
        pass

    cards = execute_query(
        """
        SELECT card_number, mean_amount, std_amount
        FROM card
        WHERE cust_id = ?
        """,
        (cust_id,)
    )

    if not cards:
        return {
            "customer_id": cust_id,
            "suspicious_count": 0,
            "transactions": []
        }

    suspicious_transactions = []

    for card in cards:

        card_number = card["card_number"]

        mean_amount = float(card["mean_amount"] or 0)
        std_amount = float(card["std_amount"] or 0)

        threshold = mean_amount + (multiplier * std_amount)

        transactions = execute_query(
            """
            SELECT t.TXN_ID, t.TX_DATETIME, t.TX_AMOUNT, m.merchant
            FROM "transaction" t
            LEFT JOIN merchant m ON t.M_ID = m.id
            WHERE t.CARD_ID = ? AND t.TX_AMOUNT > ?
            ORDER BY t.TX_AMOUNT DESC
            """,
            (card_number, threshold)
        )

        for txn in transactions:
            suspicious_transactions.append({
                "txn_id": txn["TXN_ID"],
                "date": txn["TX_DATETIME"],
                "amount": txn["TX_AMOUNT"],
                "merchant": txn["merchant"],
                "reason": f"Amount exceeds normal spending threshold ({round(threshold, 2)})"
            })

    return {
        "customer_id": cust_id,
        "suspicious_count": len(suspicious_transactions),
        "transactions": suspicious_transactions
    }


# get merchant spend summary
@tool
def get_merchant_spend_summary():
    """Aggregate transaction amount by merchant type."""

    query = """
    SELECT
        mt.merchant_type,
        ROUND(SUM(t.TX_AMOUNT), 2) AS total_spend,
        COUNT(*) AS transaction_count
    FROM "transaction" t
    JOIN merchant m ON t.M_ID = m.id
    JOIN merchant_type mt ON m.merchant_type = mt.id
    GROUP BY mt.merchant_type
    ORDER BY total_spend DESC
    """

    result = execute_query(query)

    if not result:
        return {"group_by": "merchant_type", "results": []}

    results = []

    for row in result:
        results.append({
            "merchant_type": row["merchant_type"],
            "total_spend": row["total_spend"],
            "transaction_count": row["transaction_count"]
        })

    return {"group_by": "merchant_type", "results": results}


# get notification summary
@tool
def get_notification_summary(cust_id: str = None):
    """Return notification-style alerts for high-value or unusual transactions."""

    query = """
    SELECT t.TXN_ID, t.TX_DATETIME, t.TX_AMOUNT, m.merchant, tt.debit_credit
    FROM "transaction" t
    LEFT JOIN merchant m ON t.M_ID = m.id
    LEFT JOIN transaction_type tt ON t.TXN_TYPE_ID = tt.txn_type_id
    LEFT JOIN card c ON t.CARD_ID = c.card_number
    WHERE t.TX_AMOUNT > 50000
    """

    params = []

    if cust_id:
        query += " AND c.cust_id = ?"
        params.append(cust_id)

    query += " ORDER BY t.TX_DATETIME DESC LIMIT 20"

    result = execute_query(query, tuple(params) if params else None)

    if not result:
        return {"count": 0, "notifications": []}

    notifications = []

    for row in result:
        notifications.append({
            "txn_id": row["TXN_ID"],
            "txn_datetime": row["TX_DATETIME"],
            "amount": row["TX_AMOUNT"],
            "merchant": row["merchant"],
            "transaction_type": row["debit_credit"],
            "alert": "High-value transaction alert"
        })

    return {"count": len(notifications), "notifications": notifications}


# get cards expiring soon
@tool
def get_cards_expiring_soon(days: int | str = 60):
    """Find cards that are expiring within the specified number of days from now."""

    try:
        days = int(days)
    except:
        days = 60

    query = """
    SELECT c.card_number, c.expiry, cust.first_name, cust.last_name, cust.cust_id
    FROM card c
    LEFT JOIN customer cust ON c.cust_id = cust.cust_id
    WHERE date(c.expiry) BETWEEN date('now') AND date('now', '+' || ? || ' days')
    ORDER BY c.expiry ASC
    """

    result = execute_query(query, (days,))

    if not result:
        return {"days": days, "count": 0, "cards_expiring": []}

    cards = []

    for row in result:
        card_number = str(row["card_number"])

        cards.append({
            "customer_id": row["cust_id"],
            "customer_name": row["first_name"] + " " + row["last_name"],
            "card_number": "**** **** **** " + card_number[-4:],
            "expiry": row["expiry"]
        })

    return {"days": days, "count": len(cards), "cards_expiring": cards}


# get top customers by due
@tool
def get_top_customers_by_due(limit: int | str = 10):
    """Find customers with the highest amount due based on transaction history."""

    try:
        limit = int(limit)
    except:
        limit = 10

    query = """
    SELECT cust.cust_id, cust.first_name, cust.last_name,
           COALESCE(SUM(CASE WHEN tt.debit_credit = 'Debit' THEN t.TX_AMOUNT ELSE 0 END), 0) as total_debits,
           COALESCE(SUM(CASE WHEN tt.debit_credit = 'Credit' THEN t.TX_AMOUNT ELSE 0 END), 0) as total_credits
    FROM customer cust
    LEFT JOIN card c ON cust.cust_id = c.cust_id
    LEFT JOIN "transaction" t ON t.CARD_ID = c.card_number
    LEFT JOIN transaction_type tt ON t.TXN_TYPE_ID = tt.txn_type_id
    GROUP BY cust.cust_id
    HAVING total_debits > total_credits
    ORDER BY (total_debits - total_credits) DESC
    LIMIT ?
    """

    result = execute_query(query, (limit,))

    if not result:
        return {"count": 0, "top_customers": []}

    customers = []

    for row in result:
        amount_due = round(row["total_debits"] - row["total_credits"], 2)

        customers.append({
            "cust_id": row["cust_id"],
            "name": row["first_name"] + " " + row["last_name"],
            "amount_due": amount_due
        })

    return {"count": len(customers), "top_customers": customers}


# get transaction type summary
@tool
def get_transaction_type_summary():
    """Summarize total transaction amounts by debit/credit type and local/international."""

    query = """
    SELECT tt.debit_credit, tt.lcl_intnl,
           SUM(t.TX_AMOUNT) as total_amount,
           COUNT(t.TXN_ID) as transaction_count
    FROM "transaction" t
    LEFT JOIN transaction_type tt ON t.TXN_TYPE_ID = tt.txn_type_id
    GROUP BY tt.debit_credit, tt.lcl_intnl
    ORDER BY total_amount DESC
    """

    result = execute_query(query)

    if not result:
        return {"results": []}

    results = []

    for row in result:
        results.append({
            "debit_credit": row["debit_credit"],
            "local_international": row["lcl_intnl"],
            "total_amount": row["total_amount"],
            "transaction_count": row["transaction_count"]
        })

    return {"results": results}