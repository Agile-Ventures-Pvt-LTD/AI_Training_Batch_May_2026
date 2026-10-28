from guardrails import Guard
from guardrails.hub import LlmRagEvaluator
from dotenv import load_dotenv
from agent import agent

load_dotenv()

guard = Guard().use(LlmRagEvaluator(on_fail="exception"))
model = "openai/gpt-oss-20b"

try:
    response = guard(
        agent,
        messages={"role" : "user", "content" : "Tell me the ebay sells"},
        model=model,
    )

except Exception as e:
    print(e)

print("Validation Output : ", response.validated_output)
print("Validation Passed : ", response.validation_passed)