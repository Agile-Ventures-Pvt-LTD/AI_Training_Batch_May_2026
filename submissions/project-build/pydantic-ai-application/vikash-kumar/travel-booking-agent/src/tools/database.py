import os
from database_pydantic_ai import SQLiteDatabase, SQLDatabaseDeps, create_database_toolset

def path() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "../../db/travel_data.db"))

def toolset():
    return create_database_toolset()
