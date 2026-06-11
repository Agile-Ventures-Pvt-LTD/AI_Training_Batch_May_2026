import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from src.tools.ecommerce_sql_tool import query_ecommerce_database

result = query_ecommerce_database.invoke(
    {
        "sql_query": """
        SELECT *
        FROM customers
        LIMIT 5
        """
    }
)

print(result)