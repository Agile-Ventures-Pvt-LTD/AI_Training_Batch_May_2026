from src.agents.legacy_agent import llm

response = llm.invoke(
    "Say hello"
)

print(response.content)