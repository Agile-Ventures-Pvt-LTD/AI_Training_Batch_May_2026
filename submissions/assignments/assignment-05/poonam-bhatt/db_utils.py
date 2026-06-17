import sqlite3
from config import DB_PATH

# db_utils.py






def execute_query(query, params=None):
    """
    Execute SQL query and return results as list of dictionaries.
    """

    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        rows = cursor.fetchall()

        conn.close()

        return [dict(row) for row in rows]

    except Exception as e:
        return [{"error": str(e)}]





# utils.py

def mask_card(card_number):
    card_number = str(card_number)

    if len(card_number) < 4:
        return "****"

    return "*" * (len(card_number) - 4) + card_number[-4:]


def mask_email(email):
    if not email or "@" not in email:
        return email

    name, domain = email.split("@")
    return name[:2] + "***@" + domain


def mask_phone(phone):
    phone = str(phone)

    if len(phone) < 4:
        return "****"

    return "*" * (len(phone) - 4) + phone[-4:]










