from langchain_community.utilities.sql_database import SQLDatabase

def get_database():
    db = SQLDatabase.from_uri("sqlite:///data/olist.sqlite")
    return db