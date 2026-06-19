
from loaders import load_documents
from chunking import split_and_set_metadata
from retrievers import initialize_vector_store, get_retriever
from tools import create_policy_tools
from prebuilt_agent import initialize_llm, create_agent, run_agent
from output_parser import parse_agent_output, format_final_response

# Load and process documents
docs = load_documents()
chunks = split_and_set_metadata(docs)

# Setup vector store and retriever
vector_db = initialize_vector_store(chunks)
retriever = get_retriever(vector_db)

# Create tools and agent
tools = create_policy_tools(retriever)
llm = initialize_llm()
agent = create_agent(llm, tools)

# Example query
user_query = "What should I do if the policy does not mention my scenario?"
response = run_agent(agent, user_query)
structured_output = parse_agent_output(response)
formatted_response = format_final_response(structured_output)
print(formatted_response)
