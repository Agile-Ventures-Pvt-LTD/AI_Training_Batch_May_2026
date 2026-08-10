from retrievers import get_vectorstore, retrieve_hr_policy, retrieve_travel_policy, retrieve_reimbursement_policy, retrieve_it_security_policy, retrieve_ai_usage_policy

vs = None

def get_vs():
    global vs
    if vs is None:
        vs = get_vectorstore()
    return vs

def retrieve_hr_policy_tool(query):
    return retrieve_hr_policy(get_vs(), query)

def retrieve_travel_policy_tool(query):
    return retrieve_travel_policy(get_vs(), query)

def retrieve_reimbursement_policy_tool(query):
    return retrieve_reimbursement_policy(get_vs(), query)

def retrieve_it_security_policy_tool(query):
    return retrieve_it_security_policy(get_vs(), query)

def retrieve_ai_usage_policy_tool(query):
    return retrieve_ai_usage_policy(get_vs(), query)