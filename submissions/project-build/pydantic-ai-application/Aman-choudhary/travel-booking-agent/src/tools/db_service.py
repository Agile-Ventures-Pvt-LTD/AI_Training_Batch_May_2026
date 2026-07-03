import sqlite3

def query_travel_data(query, params=()):
    conn = sqlite3.connect("db/travel_data.db")
    cursor = conn.cursor()
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results
