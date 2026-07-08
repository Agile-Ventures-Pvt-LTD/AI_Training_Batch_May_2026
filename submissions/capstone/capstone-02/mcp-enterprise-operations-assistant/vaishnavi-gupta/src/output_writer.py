from pydantic import BaseModel
from typing import List


class GroqLLM(BaseModel):

    source: str

    page: int | None = None


class MCPHost(BaseModel):

    query_type: str

    result: str


class MCPClient(BaseModel):

    user_query: str

    response: str


