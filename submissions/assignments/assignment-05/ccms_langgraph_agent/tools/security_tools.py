try:
    from db_utils.db_connection import get_conn
    from utils.tool_utils import create_tool
    from typing import Optional
    import sqlite3
    import math
except ImportError as e:
    print(f"Error: {e}")

def detect_suspicious_transactions(
    customer_id: Optional[str] = None,
    limit: int = 10
):
    """
    Detect potentially suspicious transactions using rule-based anomaly detection.
    """

    try:
        conn = get_conn()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        query = """
        SELECT
            t.TXN_ID,
            t.TX_AMOUNT,

            c.mean_amount,
            c.std_amount,

            c."x-coordinate" AS card_x,
            c."y-coordinate" AS card_y,

            tt.x_terminal_id,
            tt.y_terminal_id

        FROM "transaction" t

        INNER JOIN card c
            ON t.CARD_ID = c.card_number

        LEFT JOIN transaction_terminal tt
            ON t.TERMINAL_ID = tt.TERMINAL_ID
        """

        params = []

        if customer_id:
            query += """
            WHERE c.cust_id = ?
            """
            params.append(customer_id)

        query += """
        LIMIT ?
        """

        params.append(min(limit, 500))

        cursor.execute(query, params)

        rows = cursor.fetchall()
        print(f"Rows returned: {len(rows)}")
        
        cursor1 = get_conn().cursor()
        cursor1.execute("""
        SELECT
            MAX(TX_AMOUNT),
            AVG(TX_AMOUNT)
        FROM "transaction"
        """)

        print(cursor1.fetchone())
        
        
        
        flagged_transactions = []

        applied_rules = set()

        for row in rows:

            txn_id = row["TXN_ID"]
            amount = float(row["TX_AMOUNT"])

            # Rule 1: High-value transaction
            if amount > 300:

                applied_rules.add("amount > 300")

                flagged_transactions.append(
                    {
                        "txn_id": txn_id,
                        "amount": amount,
                        "reason": "High-value transaction"
                    }
                )

                continue

            # Rule 2: Spending anomaly
            mean_amount = row["mean_amount"]
            std_amount = row["std_amount"]

            if (
                mean_amount is not None
                and std_amount is not None
                and amount > (mean_amount + 1.5 * std_amount)
            ):

                applied_rules.add(
                    "amount > mean_amount + 1.5 * std_amount"
                )

                flagged_transactions.append(
                    {
                        "txn_id": txn_id,
                        "amount": amount,
                        "reason": "Amount significantly above spending pattern"
                    }
                )

                continue

            # Rule 3: Location anomaly
            card_x = row["card_x"]
            card_y = row["card_y"]

            terminal_x = row["x_terminal_id"]
            terminal_y = row["y_terminal_id"]

            if (
                card_x is not None
                and card_y is not None
                and terminal_x is not None
                and terminal_y is not None
            ):

                distance = math.sqrt(
                    (card_x - terminal_x) ** 2 +
                    (card_y - terminal_y) ** 2
                )

                if distance > 100:

                    applied_rules.add(
                        "terminal distance > 100"
                    )

                    flagged_transactions.append(
                        {
                            "txn_id": txn_id,
                            "amount": amount,
                            "reason": "Transaction location anomaly"
                        }
                    )

        return {
            "rule_applied": (
                ", ".join(applied_rules)
                if applied_rules
                else "No suspicious transactions detected"
            ),
            "count": len(flagged_transactions),
            "flagged_transactions": flagged_transactions
        }

    except Exception as e:

        return {
            "error": str(e),
            "rule_applied": "",
            "count": 0,
            "flagged_transactions": []
        }

    finally:
        if "conn" in locals():
            conn.close()


detect_suspicious_transactions_description = """Identify potentially suspicious transactions using anomaly detection rules such as unusually high transaction amounts, abnormal spending patterns, and unusual transaction locations."""

detect_suspicious_transactions_tool = create_tool(function=detect_suspicious_transactions, tool_name="detect_suspicious_transactions", tool_description=detect_suspicious_transactions_description)