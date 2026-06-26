# tests/test_crewai_llm.py

from src.config import llm

response = llm.call(
    "What is 2+2?"
)

print(response)