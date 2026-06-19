from langchain.tools import StructuredTool


from retriever import retrieve_documents



def parallel_retrieval(quey) -> dict:
    """ it is a tool used to retrieve data from database"""
    
    query = query
    try:
        retrieved_docs = retrieve_documents(query)
        
        context = "\n\n".join(
            doc.page_content
            for doc in retrieved_docs
        )
        return {"retreived_data":context}
    except Exception as e:
        print("Retriever Not Working:{e}")
        return { "error_message": f"Retriever failed: {e}"}
    
retrieval_tool = StructuredTool.from_function(parallel_retrieval) 
tools=[retrieval_tool]

