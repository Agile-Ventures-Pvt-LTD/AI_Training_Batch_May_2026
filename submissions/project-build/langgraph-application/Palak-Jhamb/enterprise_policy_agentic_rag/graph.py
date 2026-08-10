from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from typing_extensions import  Literal
from pydantic import BaseModel, Field

from tools import tools
from typing_extensions import TypedDict, Annotated
from operator import add
from langgraph.graph.message import add_messages
from langchain_groq import ChatGroq
from config import get_api_key

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    groq_api_key=get_api_key(),
)

llm_with_tools = llm.bind_tools(tools, tool_choice="auto")

class RouterState(TypedDict):
    """
    Represents the state of our query routing workflow.
    """
    customer_query: str                
    query_category: Annotated[list, add]
    retreived_data: str  |None          
    response: str | None                
    error_message: str | None 
    messages: Annotated[list, add_messages]
    reflection: str
    tools_used:  Annotated[list, add] 



class QueryClassification(BaseModel):
    """Schema for the query classification result."""
    category: Literal["ai usage category", "hr leave category", "it security category", "reimbbursement category","travel category"] = Field(
        description="The classified category of the customer query."
    )
    reasoning: str = Field(description="Brief explanation for the classification decision.")


def classify_query(state: RouterState) -> dict:
    """Classifies the customer query into predefined categories."""
    

    print("---CLASSIFYING QUERY---")
    query = state['customer_query']

    classification_system_message = """
    You are an expert query classifier. Analyze the customer query and classify it into one of the following categories:
    -ai usage category
    -hr leave category
    -it security category
    -reimbbursement category
    -travel category
    Respond ONLY with the required JSON format, including brief reasoning.
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", classification_system_message),
        ("human", "Customer Query: {query}")
    ])

    classifier_chain = prompt | llm.with_structured_output(QueryClassification)

    try:
        classification_result: QueryClassification = classifier_chain.invoke({"query": query})
        print(f"Classification: {classification_result.category} (Reason: {classification_result.reasoning})")
        
        return {"query_category": classification_result.category}
    except Exception as e:
        print(f"Error during classification: {e}")
        return {"query_category": "unknown", "error_message": f"Classification failed: {e}"}




def grade_documents(state:RouterState) -> Literal["generate", "rewrite"]:
    """
    Determines whether the retrieved documents are relevant to the question.
    Args:
        state (messages): The current state
    Returns:
        str: A decision for whether the documents are relevant or not
    """

    try:
        class grade(BaseModel):
            """Binary score for relevance check."""
            binary_score: str = Field(description="Relevance score 'yes' or 'no'")

        llm_with_tool = llm.with_structured_output(grade)

        prompt = PromptTemplate(
            template="""You are a grader assessing relevance of a retrieved document to a user question. \n
            Here is the retrieved document: \n\n {context} \n\n
            Here is the user question: {question} \n
            If the document contains keyword(s) or semantic meaning related to the user question, grade it as relevant. \n
            Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question.""",
            input_variables=["context", "question"],
        )
        chain = prompt | llm_with_tool
        question = state["customer_query"]
        docs = state["retreived_data"]
        scored_result = chain.invoke({"question": question, "context": docs})
        score = scored_result.binary_score

        if score == "yes":
            print("---DECISION: DOCS RELEVANT---")
            return "generate"

        else:
            print("---DECISION: DOCS NOT RELEVANT---")
            print(score)
            return "rewrite"
    except Exception as e:
        return { "error_message": f"Grading failed: {e}"}
    


from langchain_core.messages import HumanMessage
def reflection_node(state: RouterState) -> dict:
    """
    Reflect on the agent's reasoning and tool usage.
    """
    tools_used = state.get("tools_used", [])
    mesages=state.get("messages")
    prompt = f"""
    Act as an testing agent and your task is to reflect on completed task.
    Tools used:
    {tools_used}
    Mesages:
    {mesages}
    Evaluate:
    1. Were the correct tools selected?
    2. Was any tool unnecessary?
    3. Is the final answer complete?
    Give a concise reflection.
    """

    reflection = llm.invoke([HumanMessage(content=prompt)]).content
    return {"reflection": reflection}



tool_node = ToolNode(tools)

def rewrite(state: RouterState)->dict:
    """
    Transform the query to produce a better question.
    Args:
        state (messages): The current state
    Returns:
        dict: The updated state with re-phrased question
    """
    print("---TRANSFORM QUERY---")
    question = state["customer_query"]

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
    response = llm.invoke(msg)
    return {"messages": [response]}

def generate(state:RouterState)->dict:
    """
    Generate answer

    Args:
        state (messages): The current state

    Returns:
         dict: The updated state with re-phrased question
    """
    
    question = state['customer_query']
    retreived_data=state["retreived_data"]
    prompt =  PromptTemplate(
        template="""You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise. """,
        input_variables=["context", "question"],
    )
    rag_chain = prompt | llm | StrOutputParser()
    response = rag_chain.invoke({"context": retreived_data, "question": question})
    return {"messages": [response]}



def call_model(state: RouterState) -> dict:
    """Invokes the LLM with the current message history."""
    query= state["customer_query"]
    response = llm_with_tools.invoke(query)
    tool_names = [tool["name"] for tool in response.tool_calls]

    return {"messages": [response],"tools_used": tool_names}



graph = StateGraph(RouterState)
graph.add_node("Classify_query",classify_query)
graph.add_node("agent", call_model)
graph.add_node("tools_node", tool_node)
graph.add_node("reflection_node", reflection_node)
graph.add_node("grade_documents",grade_documents)
graph.add_node("rewrite",rewrite)
graph.add_node("generate",generate)

graph.add_edge(START, "Classify_query")
graph.add_edge("Classify_query", call_model)
graph.add_conditional_edges("agent", tools_condition,
    {
        "tools": "tools_node",
        "__end__": "reflection_node" 
    })
# graph.add_edge("tools_node", "grade_documents")

graph.add_conditional_edges(
    "tools_node",
    grade_documents,{
        "generate":generate,
        "rewrite":rewrite
    }
)
graph.add_edge("generate", "reflection_node")
graph.add_edge("rewrite", "agent")
graph.add_edge("reflection_node", END)

custom_agent = graph.compile()