from langgraph.graph import END, StateGraph, START
from tools import agent, query_classifier_node,parallel_retrievel_node,context_grader_node,query_rewriter_node,answer_generator_node,reflection_node,final_response_node
from tools import PolicyAgentState
workflow = StateGraph(PolicyAgentState)

workflow.add_edge(START,agent)
workflow.add_node("agent", agent)  

workflow.add_node("retrieve", parallel_retrievel_node)
workflow.add_node("grader",context_grader_node)
workflow.add_node("rewrite", query_rewriter_node)  
workflow.add_node("generate", answer_generator_node)  
workflow.add_node("reflection",reflection_node)
workflow.add_node("final_response",final_response_node)

workflow.add_edge(agent,query_classifier_node)
workflow.add_conditional_edges(query_classifier_node,context_grader_node{
    "rewrite":"query_rewriter_node",
    "generate":"answer_generator_node",
})

workflow.add_edge(query_rewriter_node,parallel_retrievel_node)
workflow.add_edge(answer_generator_node,reflection_node)
workflow.add_edge(reflection_node,final_response_node)
workflow.add_edge(final_response_node,END)

graph = workflow.compile()