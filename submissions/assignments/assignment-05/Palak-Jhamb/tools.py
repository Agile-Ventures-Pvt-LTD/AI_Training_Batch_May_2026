from db_utils import get_schema, get_db

import sqlite3


def inspect_database_schema():
    """ This is a tool used to inspect schema of database"""
    return get_schema()



def get_customer_profile(cust_id: str = None,email: str = None,phone: str = None,name: str = None):
    """ This tool is used to get customer details .Find customer information by customer ID, email, phone, or name"""
    query = None
    params = ()

    if cust_id:
        query = "SELECT * FROM customer WHERE cust_id = ?"
        params = (cust_id,)

    elif email:
        query = "SELECT * FROM customer WHERE email = ?"
        params = (email,)

    elif phone:
        query = "SELECT * FROM customer WHERE phone = ?"
        params = (phone,)

    elif name:
        query = """
        SELECT * FROM customer
        WHERE LOWER(first_name || ' ' || last_name) LIKE LOWER(?)
        """
        params = (f"%{name}%",)

    else:
        return {
            "found": False,
            "message": "No search criteria provided."
        }

    conn = get_db()
    conn.row_factory = sqlite3.Row
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        customer = cursor.fetchone()
        if not customer:
            return {
                "found": False,
                "customer": None
            }
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

    finally:
        conn.close()


def get_card_details(cust_id: str=None, card_number: str=None):
    """This is a tool used to retreive data related to card. this function will used when user asks for any card related information. """
    query = None
    params = ()
    if cust_id:
        query = "SELECT * FROM card WHERE cust_id = ?"
        params = (cust_id,)

    elif card_number:
        query = "SELECT * FROM card WHERE card_number = ?"
        params = (card_number,)
    else:
        return {
            "found": False,
            "message": "No search criteria provided."
        }
    
    conn = get_db()
    conn.row_factory = sqlite3.Row

    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        card_detail = cursor.fetchone()
        if not card_detail:
            return {
                "found": False,
                "card": None
            }
        card_no = str(card_detail["card_number"])
        masked_card = f"**** **** **** {card_no[-4:]}"
        return {
            "found": True,
            "card": {
                "card_number": masked_card,
                "valid_from": card_detail["valid_from"],
                "expiry": card_detail["expiry"],
                "card_type_id": card_detail["card_type_id"]
            }
        }

    finally:
        conn.close()



def search_transactions(cust_id=None,merchant_name=None,min_amount=None,max_amount=None,limit=10):
    """
    Search transactions using different filters, it is used to get detail about overall transactions .
    """
    query = """
        SELECT t.TXN_ID, t.TX_DATETIME, t.TX_AMOUNT, m.merchant, tt.debit_credit FROM "transaction" t
        JOIN merchant m ON t.M_ID = m.id JOIN transaction_type tt ON t.TXN_TYPE_ID = tt.txn_type_id
        JOIN card c ON t.CARD_ID = c.card_number
        WHERE 1=1
        """
    params = []

    if cust_id:
            query += " AND c.cust_id = ?"
            params.append(cust_id)

    if merchant_name:
            query += " AND m.merchant LIKE ?"
            params.append(f"%{merchant_name}%")

    if min_amount:
            query += " AND t.TX_AMOUNT >= ?"
            params.append(min_amount)

    if max_amount:
            query += " AND t.TX_AMOUNT <= ?"
            params.append(max_amount)

    query += " ORDER BY t.TX_DATETIME DESC LIMIT ?"
    params.append(limit)

    conn = get_db()
    conn.row_factory = sqlite3.Row

    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        transactions = []
        for row in rows:
            transaction = {
                "txn_id": row["TXN_ID"],
                "txn_datetime": row["TX_DATETIME"],
                "amount": row["TX_AMOUNT"],
                "merchant": row["merchant"],
                "transaction_type": row["debit_credit"]
            }

            transactions.append(transaction)

        return {
            "count": len(transactions),
            "transactions": transactions
        }

    finally:
        conn.close()



def get_customer_transactions(cust_id: str = None):
    """
    Get all transactions of a customer.
    """
    query = """
        SELECT t.TXN_ID, t.TX_DATETIME, t.TX_AMOUNT FROM "transaction" t
        JOIN card c ON t.CARD_ID = c.card_number
        WHERE c.cust_id = ?
        LIMIT 20
        """

    if not cust_id:
        return {
            "found": False,
            "message": "Customer ID is required."
        }

    conn = get_db()
    conn.row_factory = sqlite3.Row

    try:
        cursor = conn.cursor()
        cursor.execute(query, (cust_id,))
        rows = cursor.fetchall()
        if not rows:
            return {
                "found": False,
                "transactions": []
            }

        transactions = []
        for row in rows:
            transactions.append(
                {
                    "txn_id": row["TXN_ID"],
                    "date": row["TX_DATETIME"],
                    "amount": row["TX_AMOUNT"]
                }
            )

        return {
            "found": True,
            "customer_id":cust_id,
            "count": len(transactions),
            "transactions": transactions
        }

    finally:
        conn.close()


def get_statement_summary(cust_id: str = None):
    """
    Get statement summary of a customer.Return statement summary for a customer including
        total amount due, statement date and risk level.
        Use this tool when the user asks about:
        - statement summary
        - amount due
        - outstanding balance
        - due information
        - customer risk level
"""
    

    if not cust_id:
        return {
            "found": False,
            "message": "Customer ID is required."
        }

    conn = get_db()
    conn.row_factory = sqlite3.Row

    try:
        cursor = conn.cursor()
        query = """
        SELECT SUM(t.TX_AMOUNT) AS total_amount_due FROM "transaction" t
        JOIN card c ON t.CARD_ID = c.card_number
        WHERE c.cust_id = ?
        """
        cursor.execute(query, (cust_id,))
        row = cursor.fetchone()
        total_due = row["total_amount_due"] or 0

        if total_due >= 100000:
            risk_level = "HIGH"
        elif total_due >= 50000:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        return {
            "customer_id": cust_id,
            "total_amount_due": round(total_due, 2),
            "statement_date": "2026-06-01",
            "risk_level": risk_level
        }

    finally:
        conn.close()


def get_rewards_summary(cust_id: str = None):
    """
    Get reward points earned by a customer.
    """

    if not cust_id:
        return {
            "found": False,
            "message": "Customer ID is required."
        }

    conn = get_db()
    conn.row_factory = sqlite3.Row

    try:
        cursor = conn.cursor()
        query = """
        SELECT t.TXN_ID, t.TX_AMOUNT FROM "transaction" t
        JOIN card c ON t.CARD_ID = c.card_number
        WHERE c.cust_id = ?
        LIMIT 10
        """

        cursor.execute(query, (cust_id,))
        rows = cursor.fetchall()
        if not rows:
            return {
                "customer_id": cust_id,
                "reward_points": 0,
                "related_transactions": []
            }

        reward_points = 0
        related_transactions = []
        for row in rows:
            points = int(row["TX_AMOUNT"] // 100)
            reward_points += points
            related_transactions.append(
                {
                    "txn_id": row["TXN_ID"],
                    "amount": row["TX_AMOUNT"],
                    "points_earned": points
                }
            )

        return {
            "customer_id": cust_id,
            "reward_points": reward_points,
            "related_transactions": related_transactions
        }

    finally:
        conn.close()



def get_merchant_spend_summary(group_by: str = "merchant_type"):
    """
    Get spending summary grouped by merchant or merchant type.
    """
    conn = get_db()
    conn.row_factory = sqlite3.Row

    try:
        cursor = conn.cursor()
        if group_by == "merchant":
            query = """
            SELECT
                m.merchant,
                SUM(t.TX_AMOUNT) AS total_spend,
                COUNT(*) AS transaction_count
            FROM "transaction" t
            JOIN merchant m
                ON t.M_ID = m.id
            GROUP BY m.merchant
            ORDER BY total_spend DESC
            """

        else:

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

        cursor.execute(query)
        rows = cursor.fetchall()
        results = []
        for row in rows:

            if group_by == "merchant":
                results.append(
                    {
                        "merchant": row["merchant"],
                        "total_spend": row["total_spend"],
                        "transaction_count": row["transaction_count"]
                    }
                )
            else:
                results.append(
                    {
                        "merchant_type": row["merchant_type"],
                        "total_spend": row["total_spend"],
                        "transaction_count": row["transaction_count"]
                    }
                )

        return {
            "group_by": group_by,
            "results": results
        }

    finally:
        conn.close()

def detect_suspicious_transactions():
    """
    Find potentially risky transactions.
    """

    conn = get_db()
    conn.row_factory = sqlite3.Row

    try:
        cursor = conn.cursor()

        query = """
        SELECT TXN_ID, TX_AMOUNT FROM "transaction"
        WHERE TX_AMOUNT > 75000
        """

        cursor.execute(query)
        rows = cursor.fetchall()
        flagged_transactions = []
        for row in rows:
            flagged_transactions.append(
                {
                    "txn_id": row["TXN_ID"],
                    "amount": row["TX_AMOUNT"],
                    "reason": "High-value transaction"
                }
            )

        return {
            "rule_applied": "amount > 75000",
            "count": len(flagged_transactions),
            "flagged_transactions": flagged_transactions
        }

    finally:
        conn.close()



tools = [inspect_database_schema, get_customer_profile, get_card_details, search_transactions, get_customer_transactions, get_statement_summary, get_rewards_summary, get_merchant_spend_summary, detect_suspicious_transactions]

