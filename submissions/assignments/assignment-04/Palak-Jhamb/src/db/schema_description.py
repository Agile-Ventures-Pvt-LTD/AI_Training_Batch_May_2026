# from langchain_community.utilities import SQLDatabase

# # db = SQLDatabase.from_uri("sqlite:///data/ecommerce.db")
# db = SQLDatabase.from_uri(
#     "sqlite:///data/ecommerce.db",
#     sample_rows_in_table_info=0
# )

# schema = db.get_table_info()

# print(schema)
# src/db/schema_description.py

from src.db.connection import get_db


def get_schema():
    db = get_db()
    return db.get_table_info()

