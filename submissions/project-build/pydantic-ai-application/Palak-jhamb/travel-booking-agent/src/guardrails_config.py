from guardrails import Guard
from guardrails.hub import ProfanityFree
from guardrails_grhub_toxic_language import ToxicLanguage


def profinity_guard(query:str):
   guard = Guard().use(ProfanityFree(on_fail="exception"))
   res = guard.validate(query)
   return {
      "found":res.validation_passed,
      'result':res.validated_output
   }


def toxic_guard(query:str):
   guard = Guard().use(ToxicLanguage, threshold=0.5, validation_method="sentence", on_fail="exception")
   res = guard.validate(query)
   return {
      "found":res.validation_passed,
      'result':res.validated_output
   }


