
from config import DB_PATH
from pydantic_ai import Agent
from database_pydantic_ai import (
    SQLiteDatabase,
    SQLDatabaseDeps,
    SQLITE_SYSTEM_PROMPT,
    create_database_toolset,
)

def agent_tool(query):
    with SQLiteDatabase(DB_PATH) as db:
        deps = SQLDatabaseDeps(database=db, read_only=True)
        toolset = create_database_toolset()

        agent = Agent(
            "groq:openai/gpt-oss-120b",
            deps_type=SQLDatabaseDeps,
            toolsets=[toolset],
            system_prompt=SQLITE_SYSTEM_PROMPT,
        )

        result =agent.run(
            query,
            deps=deps,
        )
        return result

