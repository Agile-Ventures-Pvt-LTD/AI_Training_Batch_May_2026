try:
    from db_utils.db_connection import get_conn
    from utils.tool_utils import create_tool
    from typing import Optional
    import sqlite3
except ImportError as e:
    print(f"Error: {e}")

def search_transactions(
    transaction_id: Optional[str] = None,
    merchant_name: Optional[str] = None,
    merchant_type: Optional[str] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    transaction_type: Optional[str] = None, 
    locality: Optional[str] = None,         
    limit: int = 50,
) -> dict:
    """
    Search transactions using merchant, amount, date, debit/credit,
    and locality filters.
    """

    '''Search transactions by merchant, merchant type, amount range, date range, debit/credit type, or locality.'''
    
    try:
        conn = get_conn()
        conn.row_factory = lambda cursor, row: {
            col[0]: row[idx]
            for idx, col in enumerate(cursor.description)
        }

        cursor = conn.cursor()

        sql = """
            SELECT
                t.TXN_ID,
                t.TX_DATETIME,
                t.TX_AMOUNT,
                m.merchant,
                mt.merchant_type,
                tt.debit_credit,
                tt.lcl_intnl

            FROM "transaction" t

            LEFT JOIN merchant m
                ON t.M_ID = m.id

            LEFT JOIN merchant_type mt
                ON m.merchant_type = mt.id

            LEFT JOIN transaction_type tt
                ON t.TXN_TYPE_ID = tt.txn_type_id

            WHERE 1 = 1
        """

        conditions = []
        params = []

        if transaction_id:
            conditions.append("t.TXN_ID = ?")
            params.append(transaction_id)

        if merchant_name:
            conditions.append(
                "LOWER(m.merchant) LIKE LOWER(?)"
            )
            params.append(f"%{merchant_name}%")

        if merchant_type:
            conditions.append(
                "LOWER(mt.merchant_type) = LOWER(?)"
            )
            params.append(merchant_type)

        if min_amount is not None:
            conditions.append("t.TX_AMOUNT >= ?")
            params.append(min_amount)

        if max_amount is not None:
            conditions.append("t.TX_AMOUNT <= ?")
            params.append(max_amount)

        if from_date:
            conditions.append(
                "DATE(t.TX_DATETIME) >= DATE(?)"
            )
            params.append(from_date)

        if to_date:
            conditions.append(
                "DATE(t.TX_DATETIME) <= DATE(?)"
            )
            params.append(to_date)

        if transaction_type:
            conditions.append(
                "LOWER(tt.debit_credit) = LOWER(?)"
            )
            params.append(transaction_type)

        if locality:
            conditions.append(
                "LOWER(tt.lcl_intnl) = LOWER(?)"
            )
            params.append(locality)

        if conditions:
            sql += " AND " + " AND ".join(conditions)

        sql += """
        ORDER BY t.TX_DATETIME DESC
        LIMIT ?
        """

        params.append(min(limit, 100))

        cursor.execute(sql, params)
        rows = cursor.fetchall()

        transactions = []

        for row in rows:
            transactions.append(
                {
                    "transaction_id": row["TXN_ID"],
                    "txn_datetime": row["TX_DATETIME"],
                    "amount": float(row["TX_AMOUNT"]),
                    "merchant": row["merchant"],
                    "merchant_type": row["merchant_type"],
                    "transaction_type": row["debit_credit"],
                    "locality": row["lcl_intnl"],
                }
            )

        return {
            "records_found": len(transactions),
            "transactions": transactions,
        }

    except Exception as e:
        return {
            "error": str(e),
            "records_found": 0,
            "transactions": [],
        }

    finally:
        if "conn" in locals():
            conn.close()


def get_customer_transactions(
    customer_id: str,
    limit: int = 10
):
    """
    Return recent transactions for a customer by Customer ID.
    """

    try:
        conn = get_conn()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        query = """
            SELECT
                t.TXN_ID,
                t.TX_DATETIME,
                t.TX_AMOUNT,
                m.merchant,
                mt.merchant_type,
                tt.debit_credit,
                tt.lcl_intnl

            FROM "transaction" t
            INNER JOIN card c
                ON t.CARD_ID = c.card_number
            LEFT JOIN merchant m
                ON t.M_ID = m.id
            LEFT JOIN merchant_type mt
                ON m.merchant_type = mt.id
            LEFT JOIN transaction_type tt
                ON t.TXN_TYPE_ID = tt.txn_type_id

            WHERE c.cust_id = ?

            ORDER BY t.TX_DATETIME DESC

            LIMIT ?
        """

        cursor.execute(
            query,
            (
                customer_id,
                min(limit, 100)
            )
        )

        rows = cursor.fetchall()

        transactions = []

        for row in rows:
            transactions.append(
                {
                    "transaction_id": row["TXN_ID"],
                    "txn_datetime": row["TX_DATETIME"],
                    "amount": float(row["TX_AMOUNT"]),
                    "merchant": row["merchant"],
                    "merchant_type": row["merchant_type"],
                    "transaction_type": row["debit_credit"],
                    "locality": row["lcl_intnl"],
                }
            )

        return {
            "customer_id": customer_id,
            "transaction_count": len(transactions),
            "transactions": transactions,
        }

    except Exception as e:
        return {
            "error": str(e),
            "customer_id": customer_id,
            "transaction_count": 0,
            "transactions": [],
        }

    finally:
        if "conn" in locals():
            conn.close()

search_transactions_description = '''Search transactions by merchant, merchant type, amount range, date range, debit/credit type, or locality.'''
get_customer_transactions_description = '''Retrieve recent transaction history for a customer using their customer ID. Use for customer activity and last N transaction requests.'''


search_transactions_tool = create_tool(function=search_transactions, tool_name="search_transactions", tool_description=search_transactions_description)
get_customer_transactions_tool = create_tool(function=get_customer_transactions, tool_name="get_customer_transactions", tool_description=get_customer_transactions_description)