# src/db/connection.py

from langchain_community.utilities import SQLDatabase

DB_URI = "sqlite:///data/ecommerce.db"


def get_db():
    return SQLDatabase.from_uri(
        DB_URI,
        sample_rows_in_table_info=0
    )