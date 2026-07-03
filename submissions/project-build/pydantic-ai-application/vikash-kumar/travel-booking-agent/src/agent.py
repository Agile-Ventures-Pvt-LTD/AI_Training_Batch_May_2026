import os
from dataclasses import dataclass
from pydantic_ai import Agent, RunContext
from database_pydantic_ai import SQLiteDatabase, SQLDatabaseDeps, SQLITE_SYSTEM_PROMPT
from src.tools.database import toolset, db_path
from pydantic_ai.capabilities import Thinking, Capability
from src.tools.weather import weather_forecast
from src.guardrails_config import Safety

@dataclass
class Travel:
    db_deps: SQLDatabaseDeps
    safety_layer: Safety

toolkit = toolset()

agent = Agent("groq:openai/gpt-oss-120b",deps_type=Travel,toolsets=[toolkit],
    system_prompt=(f"{SQLITE_SYSTEM_PROMPT}"
        "You are the intelligent travel booking assistant agent.Use database tools to find travel data especially the travel dates"
        "and use weather tools to check live weather. You must answer user requests by querying the database for "
        "their details, and provide travel suggestions based on the weather conditions."))

@agent.tool
async def destination_weather(travel: RunContext[Travel], city: str) -> str:
    return await weather_forecast(city)

async def travel_assistant(user_prompt: str) -> str:
    safety = Safety()
    safe, user_input = safety.validate_text(user_prompt)
    if not safe:
        return user_input

    db_path = db_path()
    async with SQLiteDatabase(db_path) as db:
        db_deps = SQLDatabaseDeps(database=db, read_only=True)
        travel = Travel(db_deps=db_deps, safety_layer=safety)
        
        try:
            result = await agent.run(user_prompt, deps=travel)
            return result.output
        except Exception:
            return "Error Occured"
        
