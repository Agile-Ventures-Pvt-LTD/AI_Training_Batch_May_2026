from deepeval.test_case import LLMTestCase
from deepeval.metrics import answer_relevancy, contextual_precision
from pathlib import Path
Parent_dir=Path(__file__).resolve.parent
from src.agent import Agent
test_case = LLMTestCase(
    input="should i go to delhi",
    actual_output=Agent.run("should i go to delhi"),
    expected_output=Agent.run("should i go to delhi"),
)

answer_relevancy.measure(test_case)
print("Score: ", answer_relevancy.score)
print("Reason: ", answer_relevancy.reason)

contextual_precision.measure(test_case)
print("Score: ", contextual_precision.score)
print("Reason: ", contextual_precision.reason)