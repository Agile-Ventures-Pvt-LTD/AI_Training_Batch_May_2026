try:
    from db_utils.db_connection import get_conn
    from utils.tool_utils import create_tool
    from typing import Optional
    import sqlite3
except ImportError as e:
    print(f"Error: {e}")

def get_merchant_spend_summary(
    group_by: Optional[str] = "merchant"
):
    
    '''Return ranked spending summaries by merchant or merchant type.'''
    
    try:
        conn = get_conn()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        if group_by == "merchant":

            query = """
            SELECT
                m.merchant AS grouping,
                SUM(t.TX_AMOUNT) AS total_spend,
                COUNT(*) AS transaction_count

            FROM "transaction" t

            JOIN merchant m
                ON t.M_ID = m.id

            GROUP BY m.merchant

            ORDER BY total_spend DESC
            """

        elif group_by == "merchant_type":

            query = """
            SELECT
                mt.merchant_type AS grouping,
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

        else:
            return {
                "error": "group_by must be merchant or merchant_type"
            }

        cursor.execute(query)

        rows = cursor.fetchall()

        results = []

        for row in rows:

            item = {
                "total_spend": float(row["total_spend"]),
                "transaction_count": row["transaction_count"]
            }

            item[group_by] = row["grouping"]

            results.append(item)

        return {
            "group_by": group_by,
            "results": results
        }

    except Exception as e:

        return {
            "error": str(e),
            "group_by": group_by,
            "results": []
        }

    finally:
        if "conn" in locals():
            conn.close()


get_merchant_spend_summary_description = '''Return ranked spending summaries by merchant or merchant type. Use for top merchants, merchant categories, and spending rankings.'''

get_merchant_spend_summary_tool = create_tool(function=get_merchant_spend_summary, tool_name="get_merchant_spend_summary", tool_description=get_merchant_spend_summary_description)