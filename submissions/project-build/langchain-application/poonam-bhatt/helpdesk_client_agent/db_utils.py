import sqlite3

from config import DB_PATH


def get_connection():

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    return conn


def execute_select(
        query,
        params=()
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(query, params)

    rows = cursor.fetchall()

    conn.close()

    return [dict(r) for r in rows]


def execute_write(
        query,
        params=()
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(query, params)

    conn.commit()

    affected = cursor.rowcount

    conn.close()

    return affected