import os
from guardrails import Guard
from guardrails.hub import ProfanityFree, ToxicLanguage, DetectPII
from dotenv import load_dotenv
from agent import agent

load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

model = "groq:openai/gpt-oss-20b"

guard = Guard()

guard.use(DetectPII(pii_entites="pii", on_fail="exception"), on="messages") # For Inputs
guard.use(ProfanityFree(on_fail="exception"), ToxicLanguage(on_fail="exception"))   # For LLM Outputs 

try:
    response = guard(
        agent,
        messages={"role" : "user", "content" : "Tell me how many are going to visit france?"},
        model=model,
    )

except Exception as e:
    print(f"Guradrails Error {e}")


print("Validation Passed : ", response.validation_passed)
print("Validation output : ", response.validated_output)