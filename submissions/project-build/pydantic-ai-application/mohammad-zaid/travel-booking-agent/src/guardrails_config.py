# guardrails_config.py

from guardrails import Guard
from guardrails.hub import ProfanityFree
from typing import Tuple
# from guardrails.validators import ToxicLanguage

# hardcoded msg for fallback
input_msg = (
    "I understand you might be frustrated, but I'm here to help with your travel needs. "
    "Let's keep our conversation respectful. How can I assist you with your trip today?"
)

output_msg = (
    "I apologize, let me rephrase that. "
    "How else can I help you with your travel plans?"
)


def validate_input(user_input: str) -> Tuple[bool, str]:
    try:
        
        guard = Guard().use_many(
            ProfanityFree(on_fail="fix"),
            # ToxicLanguage(on_fail="fix", threshold=0.5)
        )
        
        result = guard.parse(user_input)
        
        # If output matches input, validation passed
        if str(result) == user_input:
            return True, user_input
        else:
            return False, input_msg
            
    except ImportError:
        return "try import: from guardrails.validators import ProfanityFree, ToxicLanguage"
    except Exception:
        return (user_input)


def validate_output(agent_output: str) -> Tuple[bool, str]:

    try:
        guard = Guard().use_many(
            ProfanityFree(on_fail="fix"),
            ToxicLanguage(on_fail="fix", threshold=0.5)
        )
        
        
        result = guard.parse(agent_output)
        
        if str(result) == agent_output:
            return True, agent_output
        else:
            return False, output_msg
    except ImportError:
        return "try import: from guardrails.validators import ProfanityFree, ToxicLanguage"
    except Exception:
        return (agent_output)


