from datetime import datetime, timedelta
from db_utils import execute_select_query

def inspect_database_schema() -> dict:
    """
    Inspect database schema and return tables with columns.
    """
    query = """SELECT name FROM sqlite_master WHERE type='table' ORDER BY name """

    response = execute_select_query(query)
    schema = {}
    for table in response:
        table_name = table["name"]

        columns = execute_select_query(f"PRAGMA table_info('{table_name}')")
        schema[table_name] = [column["name"] for column in columns]

    return {"tables": [table["name"] for table in response],"schema": schema,}

def get_customer_profile(cust_id: int):
    """
    Get customer profile by customer id.
    """
    query = """SELECT cust_id,first_name,last_name,email,city,state FROM customer WHERE cust_id = ? """

    result = execute_select_query(query,(cust_id,))
    if not result:
        return {"found": False,"message": "Customer not found"}

    cust = result[0]

    return {"found": True,"customer": {"cust_id": cust["cust_id"],"name": f"{cust['first_name']} {cust['last_name']}","email": cust["email"],"city": cust["city"],"state": cust["state"]}}


def get_card_details(cust_id: int):
    """
    Get card details for a customer.
    Never expose:
    - Full card number
    - CVV
    """

    query = """SELECT c.card_number,c.valid_from,c.expiry,ct.card_type,ct.card_network,ct.privilege FROM card c JOIN card_type ct ON c.card_type_id = ct.card_type_id WHERE c.cust_id = ? """

    rows = execute_select_query(query,(cust_id,))

    if not rows:
        return {"found": False,"message": "No cards found"}

    cards = []
    for row in rows:
        card_number = str(row["card_number"])

        cards.append({"card_number": f"**** **** **** {card_number[-4:]}","valid_from": str(row["valid_from"]),"expiry": str(row["expiry"]),"card_type": row["card_type"],"card_network": row["card_network"],"privilege": row["privilege"]})

    return {"found": True,"customer_id": f"CUST-{cust_id}","cards": cards}

def search_transactions(min_amount: float = 0,max_amount: float = 999999999,limit: int = 5) -> dict:
    """
    Search transactions by amount range.
    """
    query = """SELECT t.TXN_ID, t.TX_DATETIME,t.TX_AMOUNT,m.merchant,tt.debit_credit FROM "transaction" t LEFT JOIN merchant m ON t.M_ID = m.id LEFT JOIN transaction_type tt ON t.TXN_TYPE_ID = tt.txn_type_id WHERE t.TX_AMOUNT BETWEEN ? AND ? ORDER BY t.TX_DATETIME DESC LIMIT ?"""

    rows = execute_select_query(query,(min_amount, max_amount, limit))

    transactions = []
    for row in rows:
        transactions.append({"txn_id": f"TXN-{row['TXN_ID']}","txn_datetime": str(row["TX_DATETIME"]),"amount": float(row["TX_AMOUNT"]),"merchant": row["merchant"],"transaction_type": row["debit_credit"],"remarks": "Online purchase"})

    return {"count": len(transactions),"transactions": transactions}

def get_customer_transactions(cust_id: int,limit: int = 10) -> dict:
    """
    Get recent transactions for a customer.
    """
    query = """SELECT t.TXN_ID,t.TX_DATETIME,t.TX_AMOUNT,m.merchant,tt.debit_credit FROM card c JOIN "transaction" t ON c.card_number = t.CARD_ID LEFT JOIN merchant m ON t.M_ID = m.id LEFT JOIN transaction_type tt ON t.TXN_TYPE_ID = tt.txn_type_id WHERE c.cust_id = ? ORDER BY t.TX_DATETIME DESC LIMIT ?"""

    rows = execute_select_query(query,(cust_id, limit))
    transactions = []
    for row in rows:
        transactions.append({"txn_id": f"TXN-{row['TXN_ID']}","txn_datetime": str(row["TX_DATETIME"]),"amount": float(row["TX_AMOUNT"]),"merchant": row["merchant"],"transaction_type": row["debit_credit"]})

    return {"customer_id": f"CUST-{cust_id}","transaction_count": len(transactions),"transactions": transactions}


def get_statement_summary(cust_id: int) -> dict:
    """
    Generate statement summary for a customer.
    """
    query = """SELECT COALESCE(SUM(t.TX_AMOUNT), 0) AS total_amount FROM card c JOIN "transaction" t ON c.card_number = t.CARD_ID WHERE c.cust_id = ? """
    rows = execute_select_query(query,(cust_id,))
    row = rows[0]
    total_amount_due = round(float(row["total_amount"]),2)

    min_amount_due = round(total_amount_due * 0.05,2)

    statement_date = datetime.now().strftime("%Y-%m-%d")

    due_date = (datetime.now() + timedelta(days=20)).strftime("%Y-%m-%d")

    if total_amount_due >= 10000:
        risk_level = "HIGH"
    elif total_amount_due >= 5000:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return {"customer_id": f"CUST-{cust_id}","total_amount_due": total_amount_due,"min_amount_due": min_amount_due,"statement_date": statement_date,"due_date": due_date,"risk_level": risk_level}

def get_rewards_summary(cust_id: int) -> dict:
    """
    Get rewards summary for a customer.
    """
    query = """SELECT t.TXN_ID,t.TX_AMOUNT FROM card c JOIN "transaction" t ON c.card_number = t.CARD_ID WHERE c.cust_id = ? """
    rows = execute_select_query(query,(cust_id,))

    reward_points = 0
    related_transactions = []
    for row in rows:
        txn_id = row["TXN_ID"]
        amount = float(row["TX_AMOUNT"])
        reward_points += int(amount / 100)
        related_transactions.append({"txn_id": f"TXN-{txn_id}","amount": amount})

    return {"customer_id": f"CUST-{cust_id}","reward_points": reward_points,"related_transactions": related_transactions}

def get_merchant_spend_summary(group_by: str = "merchant_type") -> dict:
    """
    Get spend summary grouped by merchant type.
    """
    query = """SELECT mt.merchant_type,ROUND(SUM(t.TX_AMOUNT), 2) AS total_spend,COUNT(*) AS transaction_count FROM "transaction" t JOIN merchant m ON t.M_ID = m.id JOIN merchant_type mt ON m.merchant_type = mt.id GROUP BY mt.merchant_type ORDER BY total_spend DESC"""

    rows = execute_select_query(query)
    results = []
    for row in rows:
        results.append({"merchant_type": row["merchant_type"],"total_spend": float(row["total_spend"]),"transaction_count": int(row["transaction_count"])})

    return {"group_by": group_by,"results": results}

def detect_suspicious_transactions() -> dict:
    """
    Detect suspicious transactions.

    Rule:
    - Amount > 75000
    """
    query = """SELECT TXN_ID,TX_AMOUNT FROM "transaction" WHERE TX_AMOUNT > 75000"""
    rows = execute_select_query(query)
    flagged_transactions = []
    for row in rows:
        flagged_transactions.append({"txn_id": f"TXN-{row['TXN_ID']}","amount": float(row["TX_AMOUNT"]),"reason": "High-value transaction"})

    return {"rule_applied": "amount > 75000 or suspicious remarks","count": len(flagged_transactions),"flagged_transactions": flagged_transactions}