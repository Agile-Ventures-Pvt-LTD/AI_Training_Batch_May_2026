from pydantic import BaseModel
from typing import List
from guardrails import Guard
from guardrails.hub import ProfanityFree, ToxicLanguage
from agent import user_query

from groq import Groq
import os
from config import GROQ_API_KEY, GROQ_MODEL

client = Groq(api_key=GROQ_API_KEY)
model = GROQ_MODEL

def Guard_rails(user_query):

    guard1 = Guard().use(ProfanityFree(on_fail="fix"))
    guard2 = Guard().use(ToxicLanguage, threshold=0.5, validation_method="sentence",on_fail="exception")

    response1 = guard1.validate(user_query)
    response2 = guard2.validate(user_query)

    return response1,response2



