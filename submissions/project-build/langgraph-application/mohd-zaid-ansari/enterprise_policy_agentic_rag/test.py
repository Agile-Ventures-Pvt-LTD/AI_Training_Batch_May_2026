from loaders import load_pdf
from chunking import create_chunks
from embedding import get_embedding_model
from vector_store import create_vectorstore, index_chunks_to_vectorstore
from retrievers import get_retriever
from config import POLICY_DATA_PATH, CHUNK_SIZE, CHUNK_OVERLAP
from tools import classify_query, retrieve_hr_policy, retrieve_travel_policy,retrieve_reimbursement_policy,retrieve_it_security_policy,retrieve_ai_usage_policy, grade_context, generate_grounded_answer

pdf_load = load_pdf(POLICY_DATA_PATH)
chunker = create_chunks(pdf_load)
embedding_model = get_embedding_model()
vectorstore = create_vectorstore(embedding_model)
index_chunks_to_vectorstore(
    chunks=chunker,
    vectorstore=vectorstore
)
retriever = get_retriever(vectorstore)

print(f"Documents: {len(pdf_load)}")
print(f"Chunks: {len(chunker)}")
print(vectorstore._collection.count())


def test_classify_query():
    sample_query = "How do I request approval for a business travel expense?"
    classification = classify_query(sample_query)
    print("Classification result:", classification)


def test_retrieve_hr_policy():
    """Test HR policy retrieval tool"""
    sample_queries = [
       "How many annual leave days can an employee carry forward?"
    ]
    
    for query in sample_queries:
        print(f"\n--- Query: {query} ---")
        results = retrieve_hr_policy(query, retriever)
        for i, doc in enumerate(results):
            if "error" in doc:
                print(f"Error: {doc['error']}")
            else:
                print(f"Result {i+1}:")
                print(f"  Source: {doc['source']}")
                print(f"  Content: {doc['content'][:200]}...")



def test_retrieve_travel_policy():
    """Test travel policy from retriever."""
    sample_queries = [
       "Can I claim meals for same-day domestic business travel? "
    ]
    
    for query in sample_queries:
        print(f"\n--- Query: {query} ---")
        results = retrieve_travel_policy(query, retriever)
        for i, doc in enumerate(results):
            if "error" in doc:
                print(f"Error: {doc['error']}")
            else:
                print(f"Result {i+1}:")
                print(f"  Source: {doc['source']}")
                print(f"  Content: {doc['content'][:200]}...")



def test_retrieve_reimbursement_policy():
    """Test reimbursement policy from retriever."""
    sample_queries = [
       "What documents are needed for hotel reimbursement?"
    ]
    
    for query in sample_queries:
        print(f"\n--- Query: {query} ---")
        results = retrieve_reimbursement_policy(query, retriever)
        for i, doc in enumerate(results):
            if "error" in doc:
                print(f"Error: {doc['error']}")
            else:
                print(f"Result {i+1}:")
                print(f"  Source: {doc['source']}")
                print(f"  Content: {doc['content'][:200]}...")


def test_retrieve_it_security_policy():
    """Test IT Security policy from retriever."""
    sample_queries = [
       "Can I use my personal laptop for office work? "
    ]
    
    for query in sample_queries:
        print(f"\n--- Query: {query} ---")
        results = retrieve_it_security_policy(query, retriever)
        for i, doc in enumerate(results):
            if "error" in doc:
                print(f"Error: {doc['error']}")
            else:
                print(f"Result {i+1}:")
                print(f"  Source: {doc['source']}")
                print(f"  Content: {doc['content'][:200]}...")


def test_retrieve_ai_usage_policy():
    """Test Ai Usage policy from retriever."""
    sample_queries = [
       "Can customer data be uploaded to a public AI tool?"
    ]
    
    for query in sample_queries:
        print(f"\n--- Query: {query} ---")
        results = retrieve_ai_usage_policy(query, retriever)
        for i, doc in enumerate(results):
            if "error" in doc:
                print(f"Error: {doc['error']}")
            else:
                print(f"Result {i+1}:")
                print(f"  Source: {doc['source']}")
                print(f"  Content: {doc['content'][:200]}...")



def test_grounded_answer_generation():
    """Test the groundness of the generated answer based on context."""
    query="Will my reimbursement definitely be approved? "

    Classification=classify_query(query)
    if[Classification=="HR_LEAVE"]:
        retrieved_docs=retrieve_hr_policy(query,retriever)
    elif[Classification=="TRAVEL"]:
        retrieved_docs=retrieve_travel_policy(query,retriever)
    elif[Classification=="REIMBURSEMENT"]:
        retrieved_docs=retrieve_reimbursement_policy(query,retriever)
    elif[Classification=="IT_SECURITY"]:
        retrieved_docs=retrieve_it_security_policy(query,retriever)
    elif[Classification=="AI_USAGE"]:
        retrieved_docs=retrieve_ai_usage_policy(query,retriever)
    else:
        retrieved_docs=[]
    answer=generate_grounded_answer(query,retrieved_docs)
    print("Query:", query)
    print("Answer:", answer)


if __name__ == "__main__":
      print("Testing classify_query:")
      test_classify_query()
      print("Testing retrieve_hr_policy:")
      test_retrieve_hr_policy()
      print("Testing retrieve_travel_policy:")
      test_retrieve_travel_policy()
      print("Testing retrieve_reimbursement_policy:")
      test_retrieve_reimbursement_policy()
      print("Testing retrieve_it_security_policy:")
      test_retrieve_it_security_policy()
      print("Testing retrieve_ai_usage_policy:")
      test_retrieve_ai_usage_policy()
      print("Testing gounded answer:")
      test_grounded_answer_generation()

