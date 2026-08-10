#Extract schema: Generate schema context for LLM

# from src.db.connection import get_connection

# run ```python -m src.db.schema_description``` to execute

from .connection import get_connection


def extract_schema():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type='table';
    """)

    tables = cursor.fetchall()

    schema = ""

    for table in tables:

        table_name = table[0]         #table is a tuple ('customers',) . we need to access the first element to get the table name 

        schema += f"\nTABLE: {table_name}\n"

        cursor.execute(
            f"PRAGMA table_info({table_name})"                #PRAGMA is a special command in SQLite that Get column information.  ```PRAGMA table_info(customers)```
        )

        for column in cursor.fetchall():

            schema += (
                f"{column[1]} "
                f"({column[2]})\n"
            )

    conn.close()
    return schema


#SQLite automatically creates: sqlite_master table.
# Think:Database Directory or Table of Contents


"""

for column in cursor.fetchall():

Here cursor.fetchall() returns a list of tuples

[
 (0,'customer_id','TEXT'),
 (1,'customer_city','TEXT')
]

"""