import os
from dotenv import load_dotenv

load_dotenv()

from groq import Groq
client = Groq()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")

from prompts import query_classification_prompt, answer_generation_prompt, query_message_template

MODEL_NAME = "llama-3.3-70b-versatile"  # Update with active model from https://console.groq.com/docs/models


def classify_query(user_query: str) -> str:
    """Classify user query using Groq API."""
    prompt = [
        {"role": "system", "content": query_classification_prompt(user_query)},
        {"role": "user", "content": query_message_template.format(user_query)}
    ]

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=prompt,
            temperature=0
        )
        classification = response.choices[0].message.content.strip()
    except Exception as e:
        classification = f"Error: {e}"

    return classification


def generate_answer(user_query: str, context: str = "") -> dict:
    """Generate answer based on user query and retrieved context.
    
    Args:
        user_query: The user's question
        context: Optional context or retrieved documents
        
    Returns:
        Dictionary with answer, evidence, sources, and confidence
    """
    if not context:
        context = "No additional context provided. Answer based on general knowledge."
    
    system_prompt = answer_generation_prompt(user_query, context)
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query}
    ]

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=0
        )
        answer_text = response.choices[0].message.content.strip()
        
        # Try to parse as JSON, otherwise return as plain text
        try:
            import json
            answer_json = json.loads(answer_text)
            return answer_json
        except json.JSONDecodeError:
            return {
                "answer": answer_text,
                "supporting_evidence": [],
                "sources": [],
                "confidence": "MEDIUM",
                "answerability": "ANSWERED"
            }
    except Exception as e:
        return {
            "answer": f"Error generating answer: {e}",
            "supporting_evidence": [],
            "sources": [],
            "confidence": "LOW",
            "answerability": "NOT_FOUND"
        }


def get_query_response(user_query: str, context: str) -> dict:
    """Get both query classification and answer response."""
    classification = classify_query(user_query)
    answer = generate_answer(user_query, context)
    
    return {
        "query": user_query,
        "classification": classification,
        "answer": answer
    }


if __name__ == "__main__":
    # Example usage - Test with your own query
    test_query = "What is Tesla's revenue?"
    test_context = "Tesla's 2023 revenue was $81.5 billion, up 19% from $81.5 billion in 2022."
    
    print("=" * 60)
    print("QUERY CLASSIFICATION & ANSWER GENERATION")
    print("=" * 60)
    
    # Get classification
    print(f"\n📋 USER QUERY: {test_query}\n")
    classification = classify_query(test_query)
    print(f"✓ CLASSIFICATION:\n{classification}\n")
    
    # Get answer
    print(f"📚 CONTEXT PROVIDED:\n{test_context}\n")
    answer = generate_answer(test_query, test_context)
    print(f"✓ GENERATED ANSWER:")
    import json
    print(json.dumps(answer, indent=2))
    print("=" * 60)