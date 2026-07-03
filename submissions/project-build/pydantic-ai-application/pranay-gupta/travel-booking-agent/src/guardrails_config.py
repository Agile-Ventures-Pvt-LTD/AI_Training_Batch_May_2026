from pydantic import BaseModel
from typing import List
from guardrails import Guard
from guardrails.hub import ProfanityFree, ToxicLanguage


def input_guardrails(user_query):

    guard = Guard().use(ProfanityFree(on_fail="fix")).use(ToxicLanguage(threshold=0.5, validation_method="sentence",on_fail="exception"))

    res1 = guard.validate(user_query)

    return res1

def output_guardrails(response):

    guard = Guard().use(ProfanityFree(on_fail="fix")).use(ToxicLanguage(threshold=0.5, validation_method="sentence",on_fail="exception"))

    res2 = guard.validate(response)

    return res2

