import os
from guardrails import Guard
from guardrails.hub import ProfanityFree
from guardrails_grhub_toxic_language import ToxicLanguage

# guardrails hub install hub://guardrails/toxic_language
# guardrails hub install hub://guardrails/profanity_free


input_guard=Guard().use(ProfanityFree( on_fail="exception")).use(
    ToxicLanguage( on_fail="exception"))
output_guard=Guard().use(
    ProfanityFree( on_fail="exception")).use(
        ToxicLanguage( on_fail="exception"))

def validate_input(query):
    try:
        input_guard.validate(query)
        return True
    except Exception as e:
        print(f"{e}")
        return False

def validate_output(response):
    try:
        output_guard.validate(response)
        return response
    except Exception as e:
        print(f"{e}")
        return "Cannot output the unsafe response"
    
