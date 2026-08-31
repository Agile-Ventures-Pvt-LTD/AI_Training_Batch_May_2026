import sys
from typing import Tuple, Optional
from guardrails import Guard
from guardrails.hub import ProfanityFree, ToxicLanguage

class ContentGuardrail:
    def __init__(self):
        self.guard = Guard().use_many(ProfanityFree(threshold=0.85,on_fail="fix"),ToxicLanguage(threshold=0.85, on_fail="exception"))

    def validate_input(self, user_prompt: str) -> Tuple[bool, str]:
        try:
            self.guard.validate(user_prompt)
            return True, user_prompt
        except Exception:
            return False

    def validate_output(self, agent_response: str) -> str:
        try:
            validation_result = self.guard.validate(agent_response)
            return validation_result.validated_output or agent_response
        except Exception:
            return "I apologize, but I am unable to generate a valid response at the moment. Please try again."