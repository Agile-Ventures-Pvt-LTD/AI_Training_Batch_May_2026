import sqlite3

DB_PATH = "data/ccms.db"


#==================Checking whether dtabase is connected===================

# conn = sqlite3.connect(DB_PATH)
# cursor = conn.cursor()
# cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
# print(cursor.fetchall())
# conn.close()

"""
TABLE in database:

[('customer',), ('netbanking',), ('card_type',), ('card',), ('transaction_type',), ('transaction_terminal',), ('merchant_type',), ('merchant',), ('transaction',)]
"""


#=============== make connection to database=================

def get_connection():

    return sqlite3.connect(
        DB_PATH
    )


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
            f'PRAGMA table_info("{table_name}")'               #PRAGMA is a special command in SQLite that Get column information.  ```PRAGMA table_info(customers)```
        )

        for column in cursor.fetchall():

            schema += (
                f"{column[1]} "
                f"({column[2]})\n"
            )

    conn.close()
    return schema