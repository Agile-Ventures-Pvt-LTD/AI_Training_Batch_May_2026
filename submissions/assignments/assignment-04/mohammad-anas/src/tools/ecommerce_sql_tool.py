import sqlite3
from langchain_core.tools import tool
from src.db.connection import get_db_connection

@tool("query_ecommerce_database")
def query_ecommerce_database(query: str) -> str:
    """
    Use this tool to query the SQLite ecommerce database. The database contains customers, products, orders, and order_items tables.
    Only use SELECT queries. Do not perform INSERT, UPDATE, DELETE, DROP, ALTER, or TRUNCATE operations.
    
    Args:
        query: A SQL SELECT query.
    """
    cln_query = query.strip()
    
    if not cln_query.upper().startswith("SELECT"):
        return "Error: Only SELECT queries are allowed. Unsafe operation blocked."
    if ";" in cln_query[:-1]:
        return "Error: Multiple SQL statements are not allowed."
    
    try:
        conn = get_db_connection()
        if not conn:
            return "Error: Could not connect to the database."
            
        cursor = conn.cursor()
        cursor.execute(cln_query)
        rows = cursor.fetchall()
        conn.close()
        
        if len(rows) > 50:
            rows = rows[:50]
            prefix = "Result limited to first 50 rows:\n"
        else:
            prefix = ""
            
        if not rows:
            return "No matching data was found."
            
        results = [dict(row) for row in rows]
        return prefix + str(results)
        
    except sqlite3.Error as e:
        return f"Database Error: {e}"
    except Exception as e:
        return f"Application Error: {e}"