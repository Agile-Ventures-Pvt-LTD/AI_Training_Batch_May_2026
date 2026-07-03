import sqlite3

DB_PATH = "db/travel_data.db"


conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())
conn.close()


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
    """
                   )

    tables = cursor.fetchall()

    schema = ""

    for table in tables:

        table_name = table[0]          

        schema += f"\nTABLE: {table_name}\n"

        cursor.execute(
            f'PRAGMA table_info("{table_name}")'     
        )          

        for column in cursor.fetchall():

            schema += (
                f"{column[1]} "
                f"({column[2]})\n"
            )

    conn.close()
    return schema

print(extract_schema())


def get_traveller_profile(
    
    id=None,
    booking_id=None,
    user_name=None,
    user_email=None
):
    """
    this tool is used to find customer information by customer ID, email, phone, or name.
    It take input as 


    """

    filters = {}

    if id:
        filters["id"] = id

    if booking_id:
        filters["booking_id"] = booking_id

    if user_name:
        filters["user_name"] = user_name

    if user_email:
        filters["user_email"] = user_email

    conn=get_connection()

    conn.row_factory=sqlite3.Row

    cursor=conn.cursor()

    values=[]
    query="""
        SELECT 
            destination,
            travel_dates,
            hotel_details
        FROM bookings 
        where 1=1 """


    if "id" in filters:
        query += " AND id = ?"
        values.append(filters["cust_id"])

    if "booking_id" in filters:
        query += " AND booking_id = ?"
        values.append(filters["booking_id"])

    if "user_name" in filters:
        query += " AND user_name = ?"
        values.append(filters["user_name"])

    if "user_email" in filters:
        query += " AND user_email = ?"
        values.append(filters["user_email"])

    cursor.execute(query, tuple(values))
        
    rows=cursor.fetchall()


    conn.close()
    count_trans=len(rows)

    traveller_info=[dict(row) for row in rows]

    return traveller_info






# result=get_traveller_profile(user_name='Bob Jones')
# print(result)