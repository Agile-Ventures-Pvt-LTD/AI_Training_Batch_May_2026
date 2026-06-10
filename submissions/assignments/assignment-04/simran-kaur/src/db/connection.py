import sqlite3

DB_PATH = "data/ecommerce.db"

def get_connection():

    return sqlite3.connect(
        DB_PATH
    )

#it returns a connection object that can be used to interact with the SQLite database located at the specified path.
#You can use this connection to execute SQL queries, manage transactions, and perform various database operations.