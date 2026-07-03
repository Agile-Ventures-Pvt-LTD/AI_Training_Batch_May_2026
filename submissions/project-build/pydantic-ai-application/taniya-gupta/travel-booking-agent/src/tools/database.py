from database_pydantic_ai import  SQLDatabaseDeps, create_database_toolset

db="db/travel_data.db"
deps = SQLDatabaseDeps(database=db, read_only=True)
toolset = create_database_toolset()