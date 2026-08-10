
import json
import sys
from typing import Optional
from config import classify_query, generate_answer
from output_parser import parse_classification, parse_answer, format_response


def print_header(title: str):
    """Print formatted header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_section(title: str):
    """Print section divider."""
    print(f"\n{'─' * 70}")
    print(f"  {title}")
    print(f"{'─' * 70}")


def get_user_query() -> str:
    """Get user query from terminal input."""
    print_header("QUERY CLASSIFICATION & ANSWER GENERATION SYSTEM")
    
    try:
        user_query = input("\nEnter your query: ").strip()
        if not user_query:
            print("Query cannot be empty!")
            return get_user_query()
        return user_query
    except KeyboardInterrupt:
        print("\n\n Process interrupted by user.")
        sys.exit(0)


def get_context() -> str:
    """Get optional context from user."""
    context_input = input(
        "\n📚 Enter context/documents (or press Enter to skip): "
    ).strip()
    return context_input if context_input else "No additional context provided."


def process_query(user_query: str, context: str = ""):
    """Process query and display results."""
    print_section("Processing...")
    
    # Get classification
    print("Classifying query...")
    classification_response = classify_query(user_query)
    classification = parse_classification(classification_response)
    
    # Get answer
    print("Generating answer...")
    answer_response = generate_answer(user_query, context)
    answer = parse_answer(answer_response)
    
    # Display results
    print_section("CLASSIFICATION RESULT")
    format_response(classification, response_type="classification")
    
    print_section("ANSWER RESULT")
    format_response(answer, response_type="answer")
    
    # Save results option
    save_results(user_query, classification, answer)


def save_results(query: str, classification: dict, answer: dict):
    """Option to save results to file."""
    save = input("\nSave results to file? (y/n): ").strip().lower()
    if save == 'y':
        filename = f"outputs/response_{len(str(query))}_chars.json"
        results = {
            "query": query,
            "classification": classification,
            "answer": answer
        }
        try:
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"✓ Results saved to {filename}")
        except Exception as e:
            print(f"Error saving file: {e}")


def run_interactive_mode():
    """Run interactive CLI mode."""
    while True:
        try:
            # Get inputs
            user_query = get_user_query()
            context = get_context()
            
            # Process
            process_query(user_query, context)
            
            # Ask to continue
            continue_input = input("\n\nProcess another query? (y/n): ").strip().lower()
            if continue_input != 'y':
                print("\nThank you for using the system. Goodbye!")
                break
                
        except KeyboardInterrupt:
            print("\n\n Process interrupted by user. Goodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")
            retry = input("Try again? (y/n): ").strip().lower()
            if retry != 'y':
                break


def run_single_query(query: str, context: str = ""):
    """Run single query mode (for scripting)."""
    process_query(query, context)


if __name__ == "__main__":
    # Check command line arguments
    if len(sys.argv) > 1:
        # Single query mode
        query = " ".join(sys.argv[1:])
        context = ""
        if "--context" in sys.argv:
            context_idx = sys.argv.index("--context")
            if context_idx + 1 < len(sys.argv):
                context = sys.argv[context_idx + 1]
        run_single_query(query, context)
    else:
        # Interactive mode
        run_interactive_mode()
