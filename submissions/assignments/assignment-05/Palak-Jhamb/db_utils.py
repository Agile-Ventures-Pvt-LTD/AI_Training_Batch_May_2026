from config import DB_PATH
import sqlite3

#get_db function is defined to get connected to database by providing the DB_PATH.
def get_db():
    try:
        return sqlite3.connect(DB_PATH)
    except sqlite3.Error as e:
        print(f"Database not found: {e}")
        raise

# get_schema function is defined to get details about all tables in database.         
def get_schema():
    conn = get_db()

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        result = {
            "tables": [],
            "schema": {}
        }

        for table in tables:
            table_name = table[0]
            result["tables"].append(table_name)
            cursor.execute(
                f'PRAGMA table_info("{table_name}");'
            )
            columns = cursor.fetchall()
            column_names = []
            for column in columns:
                column_names.append(column[1])
            result["schema"][table_name] = column_names

        return result
    except sqlite3.Error as e:
        print("Got an error in getting schema of database: {e}",)
        raise

    finally:
        conn.close()