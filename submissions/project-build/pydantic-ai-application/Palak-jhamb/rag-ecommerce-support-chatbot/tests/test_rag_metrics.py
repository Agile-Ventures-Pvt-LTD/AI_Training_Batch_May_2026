from deepeval.test_case import LLMTestCase
from deepeval.metrics import answer_relevancy, contextual_precision
from pathlib import Path
Parent_dir=Path(__file__).resolve.parent

from main import input_user,output_agent
test_case = LLMTestCase(
    input=input_user,
    actual_output=output_agent,
    expected_output=output_agent,
)

answer_relevancy.measure(test_case)
print("Score: ", answer_relevancy.score)
print("Reason: ", answer_relevancy.reason)

contextual_precision.measure(test_case)
print("Score: ", contextual_precision.score)
print("Reason: ", contextual_precision.reason)