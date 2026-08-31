from config import llm
from tools import tools
from langchain import hub
from pydantic import BaseModel, Field
from prompts import query_classification_prompt
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import TypedDict, List, Dict, Optional, Literal


class PolicyAgentState(TypedDict): 
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


def agent(state : PolicyAgentState) -> PolicyAgentState:
    """
    Invokes the agent model to generate a response based on the current state. Given
    the question, Simply add the user question in the state

    Args:
        state: The current state

    Returns:
        dict: The updated state with the agent response appended to messages
    """
    print("---CALL AGENT---")
    question = state["user_question"]

    prompt = [
        {"role" : "system", "content" : f"Do not change the user Question. Just simply return the same question: {question}"}
    ]

    response = llm.invoke(prompt)

    return {"user_question": response}


def query_classifier_node(state : PolicyAgentState) -> PolicyAgentState:
    """
    Classify the user query before answer generation.

    Supported query types: 
    HR_LEAVE 
    TRAVEL 
    REIMBURSEMENT 
    IT_SECURITY 
    AI_USAGE 
    MULTI_POLICY 
    UNANSWERABLE 
    AMBIGUOUS 
    OTHER

    Args:
        state (question): The current state

    Returns:
        str: The type of the Query. 
    """

    class grade(BaseModel):
        """Classify the Query for the relevance"""

        query_type: str = Field(description="Decide the type of the query between this HR_LEAVE, TRAVEL, REIMBURSEMENT, IT_SECURITY, AI_USAGE, MULTI_POLICY, UNANSWERABLE, AMBIGUOUS, OTHER")
        policy_domain: list = Field(description="On the basic of the question return the list of required policy domain")

    print("---Query Classifier---")

    model = llm.with_structured_output(grade)

    question = state["user_question"]

    prompt = [
        {"role" : "system", "content" : query_classification_prompt.format(user_question=question)}
    ]

    response = model.invoke(prompt)

    return {
        "query_type" : response.query_type,
        "required_policy_domains": response.policy_domain
    }


def parallel_retrieval_node(state: PolicyAgentState) -> PolicyAgentState:
    """
    Given the question, it will decide to retrieve using the retriever tool, or simply end.
    if the agent is answering the question without any context from tool then it should realy mention the same at the begining.

    Args:
        state: The current state

    Returns:
        dict: The updated state with the agent response appended to messages
    """

    print("---parallel_retrieval_node---")

    question = state["user_question"]
    policy = state["required_policy_domains"]

    prompt = [
        {
            "role" : "system" , 
            "content" : f"""
            Retrieve the Required context using the retriever tool
            
            User Question
            {question}
            
            Required Policies
            {policy}  
            """
        }
    ]

    model = llm.bind_tools(tools)

    response = model.invoke(prompt)

    return {"retrieved_context" : response}


def context_grader_node(state: PolicyAgentState) -> Literal["query_rewrite_node", "answer_generator"]:
    """
    Determines whether the retrieved documents are relevant to the question.

    Args:
        state: The current state

    Returns: 
        str: A decision for whether the documents are relevant or not
    """
     
    print("---CHECK RELEVANCE---")


    class grade(BaseModel):
        """Binary score for relevance check."""

        binary_score: str = Field(description="Relevance score 'yes' or 'no'")


    model = llm.with_structured_output(grade)

    prompt = PromptTemplate(
        template="""You are a grader assessing relevance of a retrieved document to a user question. \n
        Here is the retrieved document: \n\n {context} \n\n
        Here is the user question: {question} \n
        If the document contains keyword(s) or semantic meaning related to the user question, grade it as relevant. \n
        Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question.""",
        input_variables=["context", "question"],
    )

    chain = prompt | model

    question = state["user_question"]
    docs = state["retrieved_context"]

    scored_result = chain.invoke({"question": question, "context": docs})

    score = scored_result.binary_score

    if score == "yes":
        print("---DECISION: DOCS RELEVANT---")
        return "answer_generator"

    else:
        print("---DECISION: DOCS NOT RELEVANT---")
        return "query_rewrite_node"
    

def query_rewrite_node(state : PolicyAgentState) -> PolicyAgentState:
    """
    Transform the query to produce a better question.

    Args:
        state: The current state

    Returns:
        dict: The updated state with re-phrased question
    """

    print("---TRANSFORM QUERY---")
    question = state["user_question"]

    prompt = [
        {"role" : "user", "contnet" : f"""
        Look at the input and try to reason about the underlying semantic intent / meaning. \n
        Here is the initial question:
        \n ------- \n
        {question}
        \n ------- \n
        Formulate an improved question: 
        """}
    ]

    response = llm.invoke(prompt)
    return {
        "rewritten_query": response,
        "user_question": response
    }


def answer_generator(state: PolicyAgentState) -> PolicyAgentState:
    """
    Generate answer one the context_grade_node return the string "answer_generator"

    Args:
        state: The current state

    Returns:
         dict: The updated state with re-phrased question
    """

    print("---GENERATE---")

    question = state["user_question"]
    docs = state["retrieved_context"]

    prompt = hub.pull("rlm/rag-prompt")

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = prompt | llm | StrOutputParser()

    response = chain.invoke({"context": docs, "question": question})
    
    return {"answer": response}


def reflection_node(state: PolicyAgentState) -> PolicyAgentState:
    """
    Generate the answer reflection the answer generator node 

    Args:
        state (answer, retrieved_context): The states

    Returns:
        dict: The updated state with the help of the answer and the context
    """

    question = state["user_question"]
    answer = state["answer"]
    context = state["retrieved_context"]

    prompt = [
        {"role" : "system", "content" : f"""
        Role: 
        You are the expert at evaluating the answer with the help of the given context
         
        Task:
        Question: {question}
        Answer: {answer}
        Retrieved Context: {context}
        """}
    ]

    response = llm.invoke(prompt)

    return {"reflection" : response}


def final_response_node(state: PolicyAgentState) -> PolicyAgentState:
    """
    Generate the final response for the user after the reflection node

    Args:
        state (answer, reflection): The states

    Return:
        Return The final response in the string.
    """

    answer = state["answer"]
    reflection = state["reflection"]

    prompt = [
        {"role" : "system", "content" : f"""
        You Task is to give the final response on the basis of the answer and the reflection
         
        Answer: {answer}
        Reflection: {reflection}
        """}
    ]

    chain = llm | StrOutputParser()
    
    response = chain.invoke(prompt)

    return {"final_response": response}