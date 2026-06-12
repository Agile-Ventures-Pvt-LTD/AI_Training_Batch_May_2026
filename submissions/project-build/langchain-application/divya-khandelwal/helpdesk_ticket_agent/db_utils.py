import sqlite3
from config import DB_PATH



def get_connection():

    try:

        conn = sqlite3.connect(
            DB_PATH
        )

        conn.row_factory = sqlite3.Row

        return conn


    except Exception as e:

        raise Exception(
            f"Database connection failed: {str(e)}"
        )



def fetch_all(query, params=()):

    try:

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            query,
            params
        )

        rows = cursor.fetchall()

        conn.close()


        return [
            dict(row)
            for row in rows
        ]


    except Exception as e:

        return {
            "error": str(e)
        }



def fetch_one(query, params=()):

    try:

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            query,
            params
        )

        row = cursor.fetchone()

        conn.close()


        if row:
            return dict(row)

        return None


    except Exception as e:

        return {
            "error": str(e)
        }



def execute_query(query, params=()):

    try:

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            query,
            params
        )

        conn.commit()

        conn.close()


        return True


    except Exception:

        return False