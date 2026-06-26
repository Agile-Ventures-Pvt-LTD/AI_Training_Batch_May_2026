from langgraph.graph import StateGraph, END
from tools import PolicyAgentState

# Import nodes
from tools import*
REWRITE_MAX_ATTEMPTS = 2

def build_policy_assistant_graph():
    graph = StateGraph(PolicyAgentState)

    # Nodes
    graph.add_node("classify", query_classifier)
    graph.add_node("clarify", clarification_handler)
    graph.add_node("rewrite", query_rewriter)
    graph.add_node("retrieve_single", normal_retrieval)
    graph.add_node("retrieve_multi", parallel_retrieval)
    graph.add_node("grade", context_grader)
    graph.add_node("answer", answer_generator_node)
    graph.add_node("reflect", reflection_node)
    graph.add_node("final", final_response_node)

    graph.set_entry_point("classify")

    graph.add_conditional_edges(
        "classify",
        lambda state: state.classification.get("query_type", "NORMAL"),
        {
            "AMBIGUOUS": "clarify",
            "MULTI_DOMAIN": "retrieve_multi",
            "SINGLE_DOMAIN": "retrieve_single",
            "NORMAL": "retrieve_single"
        }
    )

    graph.add_edge("clarify", "final")

    graph.add_conditional_edges(
        "retrieve_single",
        lambda state: "REWRITE" if state.rewrite_count < REWRITE_MAX_ATTEMPTS else "CONTINUE",
        {
            "REWRITE": "rewrite",
            "CONTINUE": "grade"
        }
    )

    graph.add_conditional_edges(
        "retrieve_multi",
        lambda state: "REWRITE" if state.rewrite_count < REWRITE_MAX_ATTEMPTS else "CONTINUE",
        {
            "REWRITE": "rewrite",
            "CONTINUE": "grade"
        }
    )

    graph.add_conditional_edges(
        "rewrite",
        lambda state: "DONE",
        {
            "DONE": "retrieve_single"  # dynamic routing inside retrieval for multi
        }
    )

    graph.add_conditional_edges(
        "grade",
        lambda state: state.context_grade.get("decision"),
        {
            "ANSWER": "answer",
            "REWRITE_QUERY": "rewrite",
            "ASK_CLARIFICATION": "clarify",
            "NOT_FOUND": "final"
        }
    )

    graph.add_edge("answer", "reflect")

    graph.add_edge("reflect", "final")

    graph.add_edge("final", END)

    return graph.compile()