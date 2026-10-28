from langchain.tools.retriever import create_retriever_tool
from retrievers import retriever

retriever_tool = create_retriever_tool(
    retriever=retriever,
    name="policies_retriever",
    description="Search and return information about Enterprise policies."
)
    
tools = [retriever_tool]