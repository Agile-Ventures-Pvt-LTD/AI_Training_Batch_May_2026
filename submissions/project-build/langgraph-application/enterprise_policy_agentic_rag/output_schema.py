from pydantic import BaseModel
from typing import List


class Source(BaseModel):
    source_file: str
    policy_domain: str
    chunk_id: str
    snippet: str


class FinalAnswer(BaseModel):
    answer: str
    policy_basis: List[str]
    sources: List[Source]
    answerability: str
    confidence: str
    recommended_next_step: str