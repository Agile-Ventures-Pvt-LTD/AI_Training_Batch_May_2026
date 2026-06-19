from langgraph.prebuilt import create_react_agent
from typing import TypedDict, List,Dict,Optional
from config import llm
from tools import tools
# from tools import (
#     retrieve_hr_policy,
#     retrieve_travel_policy,
#     retrieve_reimbursement_policy,
#     retrieve_it_security_policy,
#     retrieve_ai_usage_policy,
#     grade_context,
#     rewrite_query,
#     generate_grounded_answer
# )
def PolicyAgentState(TypedDict): 
        user_question: str 
        query_type: str 
        required_policy_domains: List[str] 
        rewritten_query: Optional[str] 
        retrieved_context: List[Dict] 
        context_grade: Dict 
        answer: Dict 
        reflection: Dict 
        retry_count: int 
        final_response: str 


agent = create_react_agent(model=llm,tools= tools)