from typing import TypedDict
from typing import List
from typing import Dict
from typing import Optional
from langgraph.graph import (StateGraph,END)
from tools import (retrieve_policy_data,grade_context,rewrite_query,ask_clarification,review_answer_grounding,build_not_found_response)
from config import (MAX_RETRY_COUNT)
class PolicyAgentState(TypedDict):
    user_question: str
    query_type: str
    required_policy_domains: List[str]
    requires_clarification: bool
    rewritten_query: Optional[str]
    retrieved_context: List
    context_grade: Dict
    answer: Dict
    reflection: Dict
    retry_count: int
    final_response: Dict
def query_classifier_node(state: PolicyAgentState):
    question = state["user_question"].lower()
    domains = []
    if any(
        word in question
        for word in [
            "leave",
            "vacation",
            "holiday",
            "sick leave"
        ]
    ):
        domains.append(
            "HR_LEAVE"
        )

    if any(
        word in question
        for word in [
            "travel",
            "trip",
            "flight",
            "international"
        ]
    ):
        domains.append(
            "TRAVEL"
        )

    if any(
        word in question
        for word in [
            "claim",
            "receipt",
            "expense",
            "reimbursement",
            "meal"
        ]
    ):
        domains.append(
            "REIMBURSEMENT"
        )

    if any(
        word in question
        for word in [
            "laptop",
            "wifi",
            "password",
            "security"
        ]
    ):
        domains.append(
            "IT_SECURITY"
        )

    if any(
        word in question
        for word in [
            "ai",
            "llm",
            "chatgpt",
            "customer data"
        ]
    ):
        domains.append(
            "AI_USAGE"
        )

    clarification_terms = [
        "this",
        "that",
        "it",
        "can i claim this"
    ]

    requires_clarification = any(
        term in question
        for term in clarification_terms
    )

    query_type = "OTHER"

    if len(domains) == 1:
        query_type = domains[0]

    elif len(domains) > 1:
        query_type = "MULTI_POLICY"

    return {
        **state,
        "query_type": query_type,
        "required_policy_domains": domains,
        "requires_clarification":
            requires_clarification
    }

def clarification_node(state: PolicyAgentState):
    response = ask_clarification(state["user_question"])
    return {**state,"final_response":response}
def parallel_retrieval_node(state: PolicyAgentState):
    query = (state.get("rewritten_query") or state["user_question"])
    domains = state["required_policy_domains"]
    retrieved_docs = []
    for domain in domains:
        docs = retrieve_policy_data(query=query,domain=domain)
        retrieved_docs.extend(docs)
    return {**state,"retrieved_context":retrieved_docs}
def context_grader_node(state: PolicyAgentState):
    grade = grade_context(
        question=state["user_question"],
        retrieved_documents=
        state["retrieved_context"])
    return {**state,"context_grade":grade}
def query_rewriter_node(state: PolicyAgentState):
    retry_count = state.get("retry_count",0)
    if retry_count >= MAX_RETRY_COUNT:
        return {
            **state,
            "context_grade": {
                "decision":
                "NOT_FOUND"
            }
        }

    new_query = rewrite_query(
        state["user_question"]
    )

    return {
        **state,

        "rewritten_query":
        new_query,

        "retry_count":
        retry_count + 1
    }
def answer_generator_node(
    state: PolicyAgentState
):

    docs = state[
        "retrieved_context"
    ]

    policy_basis = []
    citations = []

    for doc in docs[:5]:

        policy_basis.append(
            doc.page_content[:150]
        )

        citations.append(
            {
                "source_file":
                doc.metadata.get(
                    "source_file"
                ),

                "policy_domain":
                doc.metadata.get(
                    "policy_domain"
                ),

                "chunk_id":
                doc.metadata.get(
                    "chunk_id"
                )
            }
        )

    answer = {

        "answer":
        (
            "Based on the retrieved "
            "policy content, relevant "
            "guidance has been found."
        ),

        "policy_basis":
        policy_basis,

        "sources":
        citations,

        "answerability":
        "ANSWERED",

        "confidence":
        "HIGH"
        if docs
        else "LOW",

        "recommended_next_step":
        (
            "Review policy citations "
            "and follow the approval "
            "process where required."
        )
    }

    return {
        **state,
        "answer":
        answer
    }
def reflection_node(state: PolicyAgentState):
    reflection = (review_answer_grounding(
            answer_text=str(
                state["answer"]
            ),

            retrieved_context=
            state[
                "retrieved_context"
            ]
        )
    )

    return {
        **state,
        "reflection":
        reflection
    }


 

def final_response_node(
    state: PolicyAgentState
):

    if state.get(
        "answer"
    ):

        return {
            **state,
            "final_response":
            state["answer"]
        }

    return {
        **state,
        "final_response":
        build_not_found_response()
    }


def route_after_classifier(
    state
):

    if state.get(
        "requires_clarification"
    ):
        return "clarification"

    return "retrieval"


def route_after_grader(
    state
):

    decision = (
        state["context_grade"]
        ["decision"]
    )

    if decision == "ANSWER":
        return "answer"

    if decision == "REWRITE_QUERY":
        return "rewrite"

    if decision == "NOT_FOUND":
        return "final"

    return "final"


def route_after_reflection(
    state
):

    if state[
        "reflection"
    ].get(
        "needs_revision"
    ):
        return "final"

    return "final"


# ==================================================
# BUILD GRAPH
# ==================================================

def build_graph():

    graph = StateGraph(
        PolicyAgentState
    )

    graph.add_node(
        "classifier",
        query_classifier_node
    )

    graph.add_node(
        "clarification",
        clarification_node
    )

    graph.add_node(
        "retrieval",
        parallel_retrieval_node
    )

    graph.add_node(
        "grader",
        context_grader_node
    )

    graph.add_node(
        "rewrite",
        query_rewriter_node
    )

    graph.add_node(
        "answer",
        answer_generator_node
    )

    graph.add_node(
        "reflection",
        reflection_node
    )

    graph.add_node(
        "final",
        final_response_node
    )

    graph.set_entry_point(
        "classifier"
    )

    graph.add_conditional_edges(
        "classifier",
        route_after_classifier,
        {
            "clarification":
            "clarification",

            "retrieval":
            "retrieval"
        }
    )

    graph.add_edge(
        "clarification",
        END
    )

    graph.add_edge(
        "retrieval",
        "grader"
    )

    graph.add_conditional_edges(
        "grader",
        route_after_grader,
        {
            "answer":
            "answer",

            "rewrite":
            "rewrite",

            "final":
            "final"
        }
    )

    graph.add_edge(
        "rewrite",
        "retrieval"
    )

    graph.add_edge(
        "answer",
        "reflection"
    )

    graph.add_conditional_edges(
        "reflection",
        route_after_reflection,
        {
            "final":
            "final"
        }
    )

    graph.add_edge(
        "final",
        END
    )

    return graph.compile()


workflow = build_graph()