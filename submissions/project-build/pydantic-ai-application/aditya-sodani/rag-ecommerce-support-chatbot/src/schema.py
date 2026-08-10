from pydantic import BaseModel
from typing import List, TypedDict

class DocumentChunk(BaseModel):
    id: str
    text: str


class RagAnswer(BaseModel):
    response: str
    res_id: List[str]


class RagDeps(BaseModel):
    documents: List[DocumentChunk]


class RagOutput(TypedDict):
    answer: str
    used_id: List[str]


class RagInputs(BaseModel):
    query: str
    expected_docs: List[str]
    grounded_answer: str