import sys
import types
import re
from typing import Dict, Any
from guardrails.validators import Validator, register_validator, PassResult, FailResult, ValidationResult
from guardrails import Guard

@register_validator(name="profanity-free", data_type="string")
class ProfanityFree(Validator):
    """Local, fast, non-network-dependent Profanity validator."""
    def __init__(self, on_fail: str = "exception"):
        super().__init__(on_fail=on_fail)
    
        self.profane_patterns = [
            r"\b(fuck|shit|bitch|cunt|asshole|bastard|dick|pussy|whore|slut|crap|damn)\b",
            r"\b(wtf|f\*ck|sh\*t|b\*tch|a\*\*hole)\b"
        ]

    def _validate(self, value: str, metadata: Dict[str, Any]) -> ValidationResult:
        for pattern in self.profane_patterns:
            if re.search(pattern, value, re.IGNORECASE):
                return FailResult(
                    error_message="Input contains profane language.",
                    fix_value="[REDACTED]"
                )
        return PassResult()

@register_validator(name="toxic-language", data_type="string")
class ToxicLanguage(Validator):
    """Local, fast, non-network-dependent Toxicity validator."""
    def __init__(self, threshold: float = 0.5, validation_method: str = "sentence", on_fail: str = "exception"):
        super().__init__(on_fail=on_fail, threshold=threshold, validation_method=validation_method)
        self.toxic_patterns = [
            r"\b(kill yourself|go die|hate you|stupid idiot|shut up|dumb|useless|scammer|trash|retard|idiot)\b",
            r"\b(abuse|attack|threaten|harass|victim)\b"
        ]

    def _validate(self, value: str, metadata: Dict[str, Any]) -> ValidationResult:
        for pattern in self.toxic_patterns:
            if re.search(pattern, value, re.IGNORECASE):
                return FailResult(
                    error_message="Input contains toxic language.",
                    fix_value="[REDACTED]"
                )
        return PassResult()
    
    
    

#### write the guardrails logic 
import guardrails

if not hasattr(guardrails, 'hub'):
    guardrails.hub = types.ModuleType('guardrails.hub')
    sys.modules['guardrails.hub'] = guardrails.hub

guardrails.hub.ProfanityFree = ProfanityFree
guardrails.hub.ToxicLanguage = ToxicLanguage

input_guard = Guard().use(ProfanityFree, on_fail="exception").use(ToxicLanguage, on_fail="exception")
output_guard = Guard().use(ProfanityFree, on_fail="exception").use(ToxicLanguage, on_fail="exception")

def scan_text(text: str, is_input: bool = True) -> tuple[bool, str]:
    """
    Scans a given text using the guard.
    Returns (is_safe, message_or_error).
    """
    Guard = input_guard if is_input else output_guard
    try:
        Guard.validate(text)
        return True, text
    except Exception as e:
        error_msg = str(e)
        if "Validation failed" in error_msg:
            return False, "Unsafe content detected."
        return False, f"Validation failed with error: {error_msg}"
