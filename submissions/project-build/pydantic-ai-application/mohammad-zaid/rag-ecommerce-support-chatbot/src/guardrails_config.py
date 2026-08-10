from guardrails import Guard
from guardrails.validator_base import FailResult, PassResult
from guardrails.hub import ProfanityFree, ToxicLanguage

input_guard = Guard().use_many(
    ProfanityFree(on_fail="exception"),
    ToxicLanguage(on_fail="exception", threshold=0.5)
)


output_guard = Guard().use_many(
    ProfanityFree(on_fail="fix"),  
    ToxicLanguage(on_fail="fix", threshold=0.5)
)

def validate_input(user_input: str) -> tuple[bool, str]:
    """
    Validate user input using guardrails
    Returns: (is_valid, sanitized_input_or_error_message)
    """
    try:
        result = input_guard.parse(user_input)
        return True, result
    except Exception as e:

        return False, "your message contains inappropriate content. Please rephrase your question."

def validate_output(llm_output: str) -> tuple[bool, str]:
    """
    Validate LLM output using guardrails
    Returns: (is_valid, sanitized_output_or_fallback)
    """
    try:
        result = output_guard.parse(llm_output)
        return True, result
    except Exception as e:
        return False, "I apologize, but I cannot provide a response to that. Please try a different question about eBay seller operations."