from guardrails import Guard
from guardrails.hub import ProfanityFree
from guardrails.hub import ToxicLanguage


guard = Guard(
    validators=[
        ProfanityFree(),
        ToxicLanguage(),
    ]
)

def safe_input(text: str) -> str:
    """Raise if input violates guardrails."""
    result = guard.validate(text, on_fail="exception")
    return result

def safe_output(text: str) -> str:
    """Sanitize output; on violation return a polite fallback."""
    try:
        return guard.validate(text, on_fail="exception")
    except Exception:
        return (
            "I’m sorry, I can’t process that request. "
            "Let’s keep our conversation respectful."
        )