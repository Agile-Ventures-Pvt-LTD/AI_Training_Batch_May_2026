from guardrails import Guard, OnFailAction
from guardrails.hub import ProfanityFree, ToxicLanguage
from dataclasses import dataclass
from pydantic import BaseModel, Field
from typing import Optional, Literal
from pathlib import Path

moderation_guard = Guard().use(
    ProfanityFree(on_fail=OnFailAction.EXCEPTION),
    ToxicLanguage(threshold=0.5, validation_method="full", on_fail=OnFailAction.EXCEPTION)
)

@dataclass
class SellerAgentDeps:
    sqlite_db_path: Path 
    read_only: bool = True

class AgentResponse(BaseModel):
    status: Literal["success", "fallback"] = Field(description="Whether the query was answered or handled by the fallback mechanism.")
    response_text: str = Field(description="The detailed response text meant for the seller.")


