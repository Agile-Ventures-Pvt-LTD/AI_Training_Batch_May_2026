from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric, ContextualPrecisionMetric
import pytest


from src.agent import input_query, final_result


@pytest.mark.parametrize(
    "input_query,final_result",
    [
      (input_query),(final_result)
         ],
)
def test_faq_answers_are_relevant(input_query, final_result):
    test_case = LLMTestCase(input=input_query, actual_output=final_result)
    assert_test(test_case, [AnswerRelevancyMetric(threshold>=0.85)])
    assert_test(test_case,[ContextualPrecisionMetric(threshold ≥ 0.80)])