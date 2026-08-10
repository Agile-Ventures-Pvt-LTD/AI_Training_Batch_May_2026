from query_classifier import classify_query_tool
from vector_retriever import retrieve_tool
from user_profile import get_user_profile_tool
from device_status import get_device_status_tool
from known_incident import get_known_incident_tool
from diagnostic import make_diagnostic_tool

tools = [
    classify_query_tool,
    retrieve_tool,
    get_user_profile_tool,
    get_device_status_tool,
    get_known_incident_tool,
    make_diagnostic_tool
]