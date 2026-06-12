from langchain_community.utilities import SQLDatabase
from config import DB_URI


def get_db():
    return SQLDatabase.from_uri(
        DB_URI,
        sample_rows_in_table_info=0
    )

def get_db_schema():
    db = get_db()
    return db.get_table_info()