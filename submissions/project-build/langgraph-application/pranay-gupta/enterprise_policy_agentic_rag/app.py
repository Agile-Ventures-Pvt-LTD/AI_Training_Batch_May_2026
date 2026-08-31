from prebuilt_agent import prebuilt_agent
from output_parser import save_agent_output
import json


def parse_agent_response(response):
    if isinstance(response, str):
        try:
            return json.loads(response)
        except:
            return {
                "answer": response,
                "policy_basis": [],
                "sources": [],
                "answerability": "NOT_FOUND",
                "confidence": "LOW",
                "recommended_next_step": "Contact HR for more information."
            }
    return response


def display_result(result):
    print(" ANSWER")
    print("=" * 70)
    print(result.get('answer', 'No answer generated'))
    
    if result.get('policy_basis'):
        print(" POLICY BASIS")
        print("=" * 70)
        for basis in result.get('policy_basis', []):
            print(f"  • {basis}")
    
    if result.get('sources'):
        print(" SOURCES")
        print("=" * 70)
        for source in result.get('sources', []):
            print(f" {source.get('source_file', 'Unknown')} ({source.get('policy_domain', 'Unknown')})")
    
    print("\n" + "=" * 70)
    print(f" ANSWERABILITY: {result.get('answerability', 'UNKNOWN')}")
    print(f" CONFIDENCE: {result.get('confidence', 'UNKNOWN')}")
    print("=" * 70 + "\n")


def main():
    print(" Enterprise Policy RAG Agent")
    print("Ask any question about company policies")
    print("Type 'exit' to quit\n")
    
    while True:
        try:
            user_query = input(" Your question: ").strip()
            
            if user_query.lower() == 'exit':
                print("\n Thank you for using the Policy RAG Agent!")
                break
            
            if not user_query:
                print(" Please enter a valid question.\n")
                continue
            
            print("\n Processing your question...\n")
            
            response = prebuilt_agent(user_query)
            result = parse_agent_response(response)
            
            save_agent_output(
                answer=result.get('answer', ''),
                policy_basis=result.get('policy_basis', []),
                sources=result.get('sources', []),
                answerability=result.get('answerability', 'NOT_FOUND'),
                confidence=result.get('confidence', 'LOW'),
                recommended_next_step=result.get('recommended_next_step', 'Contact HR')
            )
            
            display_result(result)
        except KeyboardInterrupt:
            print("\n\n Thank you for using the Policy RAG Agent!")
            break
        except Exception as e:
            print(f"Error: {str(e)}")
            print("Please try again.\n")


if __name__ == "__main__":
    main()