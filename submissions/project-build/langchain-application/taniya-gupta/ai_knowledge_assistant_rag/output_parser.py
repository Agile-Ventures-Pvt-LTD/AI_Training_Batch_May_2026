from pydantic import BaseModel, Field
from typing import List
from langchain_core.output_parsers import JsonOutputParser

class QueryClassification(BaseModel):
    query_type: str =Field(description="Type of query")
    requires_retrieval: bool =Field(description="whether query needs document retrieval")
    requires_comparison: bool=Field(description="whether query needs comparing document sections")
    answer_style:str =Field(description="Style for the answer")
    reasoning_summary:str =Field(description="reasoning for the classification")

class Evidence(BaseModel):
    claim:str = Field(description="A claim made in the answer")
    source_file:str = Field(description="Source file name")
    page_number:str = Field(description="Page number if available")
    chunk_id:str = Field(description="Chunk ID")

class Source(BaseModel):
    source_file:str = Field(description="Source file name")
    page_number:str = Field(description="Page number if available")
    chunk_id:str = Field(description="Chunk ID")
    snippet:str = Field(description="Relevant snippet from the source")

class GroundedAnswer(BaseModel):
    answer:str = Field(description="The answer to the user's question")
    supporting_evidence: List[Evidence] = Field(description="List of supporting evidence for the answer")
    sources: List[Source] = Field(description="List of sources cited in the answer")
    confidence:str = Field(description="Confidence level (HIGH, MEDIUM, LOW)")
    answerability:str = Field(description="Answerability status (ANSWERED, PARTIALLY_ANSWERED, NOT_FOUND)")

classification_parser = JsonOutputParser(pydantic_object=QueryClassification)
answer_parser = JsonOutputParser(pydantic_object=GroundedAnswer)
