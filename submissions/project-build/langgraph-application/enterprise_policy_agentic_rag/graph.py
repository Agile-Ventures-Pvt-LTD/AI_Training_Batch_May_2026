from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Dict, Any
from IPython.display import display, Image
from output_schema import FinalAnswer, Source

from langchain_groq import ChatGroq
from config import GROQ_API_KEY, GROQ_MODEL
from prompts import CLASSIFIER_PROMPT, ANSWER_PROMPT
from dotenv import load_dotenv
load_dotenv()



llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name=GROQ_MODEL,
    temperature=0
)


# STATE
class State(TypedDict):
    question: str
    query_type: str
    retrieved_context: List[Dict]
    answer: Dict
    retry_count: int
    retriever: Any
# NODE-1
def classify(state):
    res = llm.invoke(CLASSIFIER_PROMPT + state["question"])
    return {"query_type": res.content}


# NODE-2
def retrieve(state):
    retriever = state["retriever"]

    docs = retriever.invoke(state["question"])

    context = [
        {
            "text": d.page_content,
            "source_file": d.metadata.get("source_file", "UNKNOWN"),
            "chunk_id": d.metadata.get("chunk_id", "UNKNOWN"),
            "policy_domain": d.metadata.get("policy_domain", "UNKNOWN"),
        }
        for d in docs
    ]

    return {"retrieved_context": context}


# NODE- 3
def grade(state):
    if len(state.get("retrieved_context", [])) >= 1:
        return {"grade": "ANSWER"}
    return {"grade": "REWRITE_QUERY"}


# NODE- 4
def rewrite(state):
    return {
        "question": state["question"] + " include eligibility rules, limits, approval conditions",
        "retry_count": state.get("retry_count", 0) + 1
    }

# HELPER - helps to get the desired output..
def answer(state):
    context = state["retrieved_context"]

    context_text = "\n\n".join([c["text"] for c in context])

    res = llm.invoke(
        ANSWER_PROMPT.format(
            context=context_text,
            question=state["question"]
        )
    )

    final_output = FinalAnswer(
        answer=res.content,
        policy_basis=[c["chunk_id"] for c in context],
        sources=[
            Source(
                source_file=c["source_file"],
                policy_domain=c["policy_domain"],
                chunk_id=c["chunk_id"],
                snippet=c["text"][:300]
            )
            for c in context
        ],
        answerability="ANSWERED",
        confidence="HIGH" if len(context) >= 2 else "MEDIUM",
        recommended_next_step="Follow policy rules and get required approvals if applicable."
    )

    return {"answer": final_output.model_dump()}

# GRAPH BUILDER- Building main Graph here....
def build_graph():
    g = StateGraph(State)

    g.add_node("classify", classify)
    g.add_node("retrieve", retrieve)
    g.add_node("grade", grade)
    g.add_node("rewrite", rewrite)
    g.add_node("answer", answer)

    g.set_entry_point("classify")

    g.add_edge("classify", "retrieve")
    g.add_edge("retrieve", "grade")

    g.add_conditional_edges(
        "grade",
        lambda x: x["grade"],
        {
            "ANSWER": "answer",
            "REWRITE_QUERY": "rewrite"
        }
    )

    g.add_edge("rewrite", "retrieve")
    g.add_edge("answer", END)

    return g.compile()

# for generating graph img in png format and save in the folder.

#graph = build_graph()

#graph.get_graph(xray=True).draw_mermaid_png(output_file_path='policy_agentic_graph.png')