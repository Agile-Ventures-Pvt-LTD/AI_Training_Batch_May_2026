from langchain_core.tools import tool
from retrievers import retrieve_by_domain
from prompts import CLASSIFIER_PROMPT,CONTEXT_GRADER_PROMPT,QUERY_REWRITE_PROMPT,ANSWER_PROMPT,REFLECTION_PROMPT
from config import GROQ_API_KEY,GROQ_MODEL
from langchain_groq import ChatGroq
from retrievers import retrieve_policies

llm = ChatGroq(api_key=GROQ_API_KEY,model=GROQ_MODEL,temperature=0)
from output_parser import safe_json_parse

def query_classifier_node(state):
    """This will classify the user query"""
    question = state["user_question"]
    prompt = f"""{CLASSIFIER_PROMPT}
            Question:{question}"""
    response = llm.invoke(prompt)
    result = safe_json_parse(response.content)
    if not result:
        question_lower = question.lower()
        if "leave" in question_lower:
            result = {"query_type": "HR_LEAVE","required_policy_domains": ["HR_LEAVE"],"requires_clarification": False}

        elif ("travel" in question_lower or "trip" in question_lower):
            result = {"query_type": "TRAVEL","required_policy_domains": ["TRAVEL"],"requires_clarification": False}

        elif ("reimbursement" in question_lower or "claim" in question_lower or "expense" in question_lower):
            result = {"query_type":"REIMBURSEMENT","required_policy_domains": ["REIMBURSEMENT"],"requires_clarification":False}

        elif ("password" in question_lower or "security" in question_lower or "laptop" in question_lower):
            result = {"query_type":"IT_SECURITY","required_policy_domains": ["IT_SECURITY"],"requires_clarification":False}

        elif ("ai" in question_lower or "customer data" in question_lower):
            result = {"query_type":"AI_USAGE","required_policy_domains": ["AI_USAGE"],"requires_clarification":False}

        else:
            result = {"query_type":"OTHER","required_policy_domains":[],"requires_clarification":False}

    return {"query_type":result.get("query_type","OTHER"),"required_policy_domains":result.get("required_policy_domains",[],),      "requires_clarification":result.get("requires_clarification",False)}

def parallel_retrieval_node(state):
    """This is for parallel retrieval node"""
    question = (state["rewritten_query"]
        if state.get("rewritten_query")
        else state["user_question"])

    domains = state["required_policy_domains"]
    docs = retrieve_policies(question,domains)
    context = []
    for doc in docs:
        context.append({"content":doc.page_content,"source_file":doc.metadata.get("source_file"),"policy_domain":doc.metadata.get("policy_domain"),"chunk_id":doc.metadata.get("chunk_id")})
    return {"retrieved_context":context}

def context_grader_node(state):
    """This is for context grading then next steps will be executed"""
    if not state["retrieved_context"]:
        return {"context_grade": {"decision":"NOT_FOUND"}}

    prompt = f"""{CONTEXT_GRADER_PROMPT}
    Question:{state["user_question"]}
    Context:{state["retrieved_context"]}"""
    response = llm.invoke(prompt)
    result = safe_json_parse(response.content)
    if not result:
        result = {"decision": "ANSWER"}
    return {"context_grade":result}

def query_rewriter_node(state):
    """This will repharse and rewrite the query """
    prompt = f"""{QUERY_REWRITE_PROMPT}
    Question:{state["user_question"]}"""
    response = llm.invoke(prompt)
    return {"rewritten_query":response.content.strip(),"retry_count":state["retry_count"] + 1}

def answer_generator_node(state):
    """This will generate answer according to the query"""
    prompt = f"""{ANSWER_PROMPT}
    Question:{state["user_question"]}
    Context:{state["retrieved_context"]}"""
    response = llm.invoke(prompt)
    result = safe_json_parse(response.content)
    if not result:
        result = {"answer":response.content,"confidence":"MEDIUM"}
    return {"answer":result}

def reflection_node(state):
    """This will tells that either revision is required or not"""
    return {"reflection": {"needs_revision":False}}

def final_response_node(state):
    """This will finally respond to the user query """
    if state.get("requires_clarification",False):
        return {"final_response":"I am not able to find the policy, can you provide more relevant information!"}
    
    answer = state.get("answer",{})
    if not answer:
        return {"final_response":"There is no policy for this"}
    return {"final_response":str(answer)}

def route_after_classifier(state):
    """This will route the path and may be requires clarification"""
    if state["requires_clarification"]:
        return "clarification"
    return "retrieve"

def route_after_grader(state):
    """This will route after grader that either answer the query or rewrite the query"""
    decision = state["context_grade"].get("decision","NOT_FOUND")
    if decision == "ANSWER":
        return "answer"
    if (decision == "REWRITE_QUERY" and state["retry_count"] < 1):
        return "rewrite"
    return "final"

def route_after_reflection(state):
    """THis will route after reflection"""
    return "final"

@tool
def retrieve_hr_policy(question: str):
    """Retrieve hr policy domain"""
    return retrieve_by_domain(question,"HR_LEAVE")

@tool
def retrieve_travel_policy(question: str):
    """THis will give hte travel policy"""
    return retrieve_by_domain(question,"TRAVEL")

@tool
def retrieve_reimbursement_policy(question: str):
    """This will give the reimbursement policy"""
    return retrieve_by_domain(question,"REIMBURSEMENT")

@tool
def retrieve_it_security_policy(question: str):
    """THis will give the security policy"""
    return retrieve_by_domain(question,"IT_SECURITY")

@tool
def retrieve_ai_usage_policy(question: str):
    """THis will give the retrieve ai usage policy"""
    return retrieve_by_domain(question,"AI_USAGE")

