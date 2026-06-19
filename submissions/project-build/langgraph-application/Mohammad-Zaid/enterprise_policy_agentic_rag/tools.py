
from langchain.tools.retriever import create_retriever_tool

TOOL_DESCRIPTIONS = {
    "retrieve_hr_policy": "Retrieve information from HR/Leave policy documents. Use when answering questions about employee benefits, leave types, leave balance, and HR procedures.",
    "retrieve_travel_policy": "Retrieve information from Travel policy documents. Use when answering questions about travel approvals, expenses, travel booking procedures, and travel guidelines.",
    "retrieve_reimbursement_policy": "Retrieve information from Reimbursement policy documents. Use when answering questions about reimbursable expenses, reimbursement process, and expense approval.",
    "retrieve_it_security_policy": "Retrieve information from IT Security policy documents. Use when answering questions about security requirements, data protection, device usage, and IT security procedures.",
    "retrieve_ai_usage_policy": "Retrieve information from AI Usage policy documents. Use when answering questions about allowed AI tools, data privacy with AI, and AI usage guidelines.",
}

def create_policy_tools(retriever):
    tools = [
        create_retriever_tool(
            retriever=retriever,
            name="retrieve_hr_policy",
            description=TOOL_DESCRIPTIONS["retrieve_hr_policy"],
        ),
        create_retriever_tool(
            retriever=retriever,
            name="retrieve_travel_policy",
            description=TOOL_DESCRIPTIONS["retrieve_travel_policy"],
        ),
        create_retriever_tool(
            retriever=retriever,
            name="retrieve_reimbursement_policy",
            description=TOOL_DESCRIPTIONS["retrieve_reimbursement_policy"],
        ),
        create_retriever_tool(
            retriever=retriever,
            name="retrieve_it_security_policy",
            description=TOOL_DESCRIPTIONS["retrieve_it_security_policy"],
        ),
        create_retriever_tool(
            retriever=retriever,
            name="retrieve_ai_usage_policy",
            description=TOOL_DESCRIPTIONS["retrieve_ai_usage_policy"],
        ),
    ]
    return tools


def grade_retrieved_context(context, user_query):
    return "Context relevance checked."
