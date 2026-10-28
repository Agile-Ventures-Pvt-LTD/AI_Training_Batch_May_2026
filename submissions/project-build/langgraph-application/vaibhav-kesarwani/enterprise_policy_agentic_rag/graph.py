from tools import tools
from langgraph.graph import END, StateGraph, START
from langgraph.prebuilt import tools_condition, ToolNode
from custom_agent import (
    PolicyAgentState,
    agent,
    query_classifier_node,
    parallel_retrieval_node,
    context_grader_node,
    query_rewrite_node,
    answer_generator,
    reflection_node,
    final_response_node
)

workflow = StateGraph(PolicyAgentState)

workflow.add_node("agent", agent)
workflow.add_node("classifier", query_classifier_node)

workflow.add_node("parallel_retrieval", parallel_retrieval_node)
retrieve = ToolNode(tools)
workflow.add_node("retrieve", retrieve)

workflow.add_node("rewrite", query_rewrite_node)
workflow.add_node("generate", answer_generator)
workflow.add_node("evaluator", reflection_node)
workflow.add_node("final_answer", final_response_node)


workflow.add_edge(START, "agent")
workflow.add_edge("agent", "classifier")
workflow.add_edge("classifier", "parallel_retrieval")

workflow.add_conditional_edges(
    "parallel_retrieval",
    tools_condition,
    {
        "tools": "retrieve",
        END: END
    }
)

workflow.add_conditional_edges(
    "retrieve",
    context_grader_node,
    {
        "query_rewrite_node": "rewrite",       
        "generate": "generate",     
        END: END                    
    }
)


workflow.add_edge("rewrite", "parallel_retrieval")
workflow.add_edge("generate", "evaluator")
workflow.add_edge("evaluator", "final_answer")
workflow.add_edge("final_answer", END)

try:
    graph = workflow.compile()
except Exception as e:
    print(e)