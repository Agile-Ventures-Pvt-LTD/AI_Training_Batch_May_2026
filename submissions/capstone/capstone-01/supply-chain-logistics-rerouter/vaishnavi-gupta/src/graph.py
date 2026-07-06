from langgraph.graph import StateGraph
from state import GraphState
from nodes import *
from langgraph.graph import START
from langgraph.graph import END


builder = StateGraph(GraphState)

builder.add_node(

    "parser",

    parse_incident_node

)

builder.add_node(

    "lookup",

    policy_rag_lookup_node

)

builder.add_node(

    "loader",

    load_alternative_routes_node

)

builder.add_node(

    "select",

    select_route_node

)

builder.add_node(

    "check",

    check_warehouse_node

)

builder.add_node(

    "analyzer",

    analyze_route_node

)

builder.add_node(

    "clarification",

    route_clarification_node
)

builder.add_node(

    "finalizer",

    finalize_route_node
)

builder.add_node(

    "escalator",

    escalate_incident_node
)

builder.add_node(

    "generator",

    generate_report_node
)

builder.add_node(

    "final",

    final_node
)


builder.add_edge(

    START,

    "parser"

)

builder.add_edge(

    "parser",

    "lookup"

)

builder.add_edge(

    "lookup",

    "loader"
)

builder.add_edge(

    "loader",

    "select"
)

builder.add_edge(

    "select",

    "check"
)

builder.add_edge(

    "check",

    "analyzer"
)


def route(state):

    grade = state["routing_decision"]

    if grade == "OPTIMAL_PATH_FOUND":

        return "finalizer"

    else:

        return "clarification"
    

builder.add_conditional_edges(

    "analyzer",

    route
)

builder.add_edge(

    "clarification",

    "loader"
)

builder.add_edge(

    "select",

    "check"

)

builder.add_edge(

    "check",

    "analyzer"
)

builder.add_edge(

    "finalizer",

    "escalator"
)


builder.add_edge(

    "generator",

    "final"
)

builder.add_edge(

    "final",

    END
)

graph = builder.compile()


def run(question, retriever):

    initial_input = {

        "question": question,

        "retriever": retriever,

        "incident_id": str,

        "manifest_text": str,

        "disrupted_port_id" : str

    }

    final_state = graph.invoke(

        initial_input

    )

    return final_state


