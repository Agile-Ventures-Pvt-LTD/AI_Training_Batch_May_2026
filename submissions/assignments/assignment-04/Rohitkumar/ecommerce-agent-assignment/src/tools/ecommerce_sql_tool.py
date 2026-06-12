from langchain.tools import tool, Tool
from src.db.connection import get_connection



# COMMON FUNCTION (CORE LOGIC)

def execute_query(query: str):
    """Core DB execution logic"""

    # normalize query
    query_clean = query.strip().lower()

    # allow only SELECT
    if not query_clean.startswith("select"):
        return "Only SELECT queries are allowed."

    # block multiple queries
    if ";" in query_clean:
        return "Multiple queries are not allowed."

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(query)

        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        conn.close()

        if not rows:
            return "No data found."

        rows = rows[:10]

        result = [dict(zip(columns, row)) for row in rows]

        return result

    except Exception as e:
        return f"Error: {str(e)}"


# MODERN TOOL (LangChain >=1 style)

@tool
def query_ecommerce_database(query: str):
    """Execute safe SELECT query on ecommerce database"""
    return execute_query(query)



# LEGACY TOOL (LangChain <1 style)

def run_query_legacy(query: str):
    return execute_query(query)


ecommerce_sql_tool_legacy = Tool(
    name="Ecommerce SQL Tool",
    func=run_query_legacy,
    description="Use this tool to query the ecommerce database using SQL SELECT queries"
)