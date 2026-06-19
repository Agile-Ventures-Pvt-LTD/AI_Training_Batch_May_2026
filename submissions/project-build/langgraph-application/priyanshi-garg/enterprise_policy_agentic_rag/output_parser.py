from pydantic import BaseModel

class QueryClassification(BaseModel):

    query_type:str
    required_policy_domains:list
    requires_parallel_retrieval:bool
    requires_clarification:bool
