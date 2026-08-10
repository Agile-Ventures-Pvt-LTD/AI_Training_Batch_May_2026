from pydantic import BaseModel
from typing import List


class Citation(BaseModel):

    source: str

    page: int | None = None



class FinalAnswer(BaseModel):

    answer: str

    citations: List[Citation]