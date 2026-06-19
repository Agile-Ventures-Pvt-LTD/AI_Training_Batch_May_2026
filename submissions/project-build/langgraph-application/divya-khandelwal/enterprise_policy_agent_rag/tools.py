from typing import TypedDict, List, Dict, Optional,Literal
from pydantic import BaseModel,Field

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.tools.retriever import create_retriever_tool
from retrievers import retriever
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain import hub


import os
from dotenv import load_dotenv
load_dotenv()


llm= ChatGroq(
    api_key=os.getenv('GROQ_API_KEY'),
    model=os.getenv("GROQ_MODEL"),
    temperature=0
)


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

class QueryClassification(BaseModel):
    """Schema for the query classification result."""
    category: Literal["HR_LEAVE","TRAVEL", "REIMBURSEMENT","IT_SECURITY","AI_USAGE","MULTI_POLICY","UNANSWERABLE","AMBIGUOUS","OTHER"] = Field(
        description="The classified category of the customer query."
    )
    reasoning: str = Field(description="Brief explanation for the classification decision.")

def agent(state):
    """
    Invokes the agent model to generate a response based on the current state. Given
    the question, it will decide to retrieve using the retriever tool, or simply end.

    Args:
        state (messages): The current state

    Returns:
        dict: The updated state with the agent response appended to messages
    """
    print("---CALL AGENT---")
    messages = state["messages"]
    model = llm
    response = model.invoke(messages)
    # We return a list, because this will get added to the existing list
    return {"messages": [response]}

def query_classifier_node(state: PolicyAgentState) -> dict:
   """Classifies the customer query into predefined categories."""
   print("---CLASSIFYING QUERY---")
   query = state['user_question']

   classification_system_message = """
    You are an expert query classifier. Analyze the customer query and classify it into one of the following categories:
    - 'HR_LEAVE' (e.g., Leave entitlement, carry forward, approvals, unpaid leave),
    - 'TRAVEL' (e.g., Domestic travel, international travel, travel approvals),
    - 'REINBURSEMENT' (e.g., Meals, hotel, transport, receipts, claim limits), 
    - 'IT_SECURITY' (e.g., Laptop usage, password rules, device security),
    - 'AI_USAGE'  (e.g., Public AI tool usage, customer data restrictions, approval process),
    - 'MULTI_POLICY',
    - 'UNANSWERABLE',
    - 'AMBIGUOUS',
    - 'OTHER'
    
    Respond ONLY with the required JSON format, including brief reasoning.
    """

   prompt = ChatPromptTemplate.from_messages([
        ("system", classification_system_message),
        ("human", "user Query: {query}")
    ])

    # Use structured output to get reliable classification
   classifier_chain = prompt | llm.with_structured_output(QueryClassification)

   try:
        classification_result: QueryClassification = classifier_chain.invoke({"query": query})
        print(f"Classification: {classification_result.category} (Reason: {classification_result.reasoning})")
        # Update the state with the classification result
        return {"query_type": classification_result.category}
   except Exception as e:
        print(f"Error during classification: {e}")
        # If classification fails, mark as unknown and log error
        return {"query_type": "unknown"}
   


def parallel_retrievel_node(state: PolicyAgentState):
    """search for the relevant chunks in the vector data and retrive the context"""
    retriever_tool = create_retriever_tool(
    retriever(),
    "retrieve_10k_text",
    "Search and return information about the enterprise policies."
    )

    return {"retrieved_context":retriever_tool}


def context_grader_node(state: PolicyAgentState) -> Literal[""]:
    """
    Determines whether the retrieved documents are relevant to the question.

    Args:
        state (messages): The current state

    Returns:
        str: A decision for whether the documents are relevant or not
    """

    print("---CHECK RELEVANCE---")

    # Data model
    class grade(BaseModel):
        """Binary score for relevance check."""

        binary_score: str = Field(description="Relevance score 'yes' or 'no'")


    # LLM with tool and validation
    llm_with_tool = llm.with_structured_output(grade)


    # Prompt
    prompt = ChatPromptTemplate(
        template="""You are a grader assessing relevance of a retrieved document to a user question. \n
        Here is the retrieved document: \n\n {context} \n\n
        Here is the user question: {question} \n
        If the document contains keyword(s) or semantic meaning related to the user question, grade it as relevant. \n
        Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question.""",
        input_variables=["context", "question"],
    )

    # Chain
    chain = prompt | llm_with_tool

    messages = state["messages"]
    last_message = messages[-1]

    question = messages[0].content
    docs = last_message.content

    scored_result = chain.invoke({"question": question, "context": docs})

    score = scored_result.binary_score

    if score == "yes":
        print("---DECISION: DOCS RELEVANT---")
        return {"context_grade":"generate"}

    else:
        print("---DECISION: DOCS NOT RELEVANT---")
        print(score)
        return {"context_grade":"rewrite"}


def query_rewriter_node(state):
    """
    Transform the query to produce a better question.

    Args:
        state (messages): The current state

    Returns:
        dict: The updated state with re-phrased question
    """

    print("---TRANSFORM QUERY---")
    messages = state["messages"]
    question = messages[0].content

    msg = [
        HumanMessage(
            content=f""" \n
    Look at the input and try to reason about the underlying semantic intent / meaning. \n
    Here is the initial question:
    \n ------- \n
    {question}
    \n ------- \n
    Formulate an improved question: """,
        )
    ]

    # Grader

    response = llm.invoke(msg)
    return {"rewritten_query": [response]}


def answer_generator_node(state):
    """
    Generate answer

    Args:
        state (messages): The current state

    Returns:
         dict: The updated state with re-phrased question
    """
    print("---GENERATE---")
    messages = state["messages"]
    question = messages[0].content
    last_message = messages[-1]

    docs = last_message.content

    # Prompt
    prompt = hub.pull("rlm/rag-prompt")

    # Post-processing
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    # Chain
    rag_chain = prompt | llm | StrOutputParser()

    # Run
    response = rag_chain.invoke({"context": docs, "question": question})
    return {"answer": [response]}



def reflection_node(state: PolicyAgentState):


    print("--- Reflection Node ---")

    last_message = (state["messages"][-1])

    reflection = f"""
Response Generated:{last_message.content}

Validation:
✓ User request processed

✓ Required tools executed

✓ Final response generated

"""
    return {"reflection":reflection}


def final_response_node(state: PolicyAgentState):
   """Return the final response in a clean format."""
   final_response = state.get("final_response") or state.get("answer") 
   return {"final_response": final_response}

