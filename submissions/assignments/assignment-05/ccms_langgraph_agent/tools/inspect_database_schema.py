try:
    from db_utils.db_connection import get_conn
    from utils.tool_utils import create_tool
except ImportError as e:
    print(f"Error: {e}")

def inspect_database_schema():
    
    """Inspect the database schema and return table names and column names."""
    
    conn = get_conn()
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    result = {
        "tables": [],
        "schema": {}
    }
    
    for (table_name,) in tables:
        result["tables"].append(table_name)
        result["schema"][f"{table_name}"] = []
        # Get column info for specific table
        cursor.execute(f"PRAGMA table_info('{table_name}');")
        columns = cursor.fetchall()
        for col in columns:
            result["schema"][f"{table_name}"].append(col[1])
    
    conn.close()
    return result


inspect_database_schema_description = """Inspect the database schema and return table names and column names. Use for database structure discovery only."""

inspect_database_schema_tool = create_tool(function=inspect_database_schema, tool_name="inspect_database_schema", tool_description=inspect_database_schema_description)