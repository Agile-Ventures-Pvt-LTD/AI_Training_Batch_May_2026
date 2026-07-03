from typing import Tuple
from guardrails import Guard
from guardrails.hub import ProfanityFree
from guardrails.hub import ToxicLanguage
from pydantic import BaseModel

class Safety:
    def __init__(self):
        self.guard = Guard().use(ProfanityFree(on_fail="fix"))
        self.guard = Guard().use(ToxicLanguage(on_fail="exception"))
        self.fallback = "Pleasse write politely."

    def validate_text(self, text: str) -> Tuple[bool, str]:
        try:
            result = self.guard.validate(text)
            if not result.validation_passed:
                return False, self.fallback
            return True, text
        except Exception:
            return False, self.fallback
