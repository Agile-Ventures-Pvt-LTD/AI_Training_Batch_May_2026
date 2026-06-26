from config import SCREENING_RUBRIC_PATH
import deepeval
from config import llm
!deepeval set-local-model --model="openai/gpt-oss-20b" --base-url="https://api.groq.com/openai/vi"

from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric
from deepeval.evaluate import evaluate

answer_relevancy_metric = AnswerRelevancyMetric()

test_case = LLMTestCase(
  input="Screen CAND-001 for the AI Engineer role.",
  actual_output=llm.invoke("Screen CAND-001 for the AI Engineer role.",
)
)
evaluate(test_cases=[test_case], metrics=[answer_relevancy_metric])

from deepeval.test_case import LLMTestCase
from deepeval.metrics import ContextualPrecisionMetric
from deepeval.evaluate import evaluate

contextual_precision_metric = ContextualPrecisionMetric(
    # threshold= 1.0
)

from deepeval.test_case import LLMTestCase
from deepeval.metrics import ContextualPrecisionMetric
from deepeval.evaluate import evaluate

contextual_precision_metric = ContextualPrecisionMetric(
    # threshold= 1.0
)

test_case = LLMTestCase(
  input="",
  actual_output= llm.invoke("").content,
#   retrieval_context=["Gender Bias, Racial Bias, Ethnic Bias, Religious Bias, Political Bias, Cultural Bias, Educational Bias,Linguistic Bias"],
# retrieval_context=[llm.invoke("What are the types of Bias an LLM can generate, give me just the heading").content],
retrieval_context=[llm.invoke("").content.replace(" ",", ")],
expected_output="""   """

)

evaluate(test_cases=[test_case], metrics=[answer_relevancy_metric])

def test_report_recommendation_matches_score_band():
    report = SCREENING_RUBRIC_PATH
    percentage = report["percentage"]
    recommendation = report["recommendation"]
    if percentage >= 80:
         assert recommendation == "STRONG_MATCH"
    elif percentage >= 60:
         assert recommendation == "MODERATE_MATCH"
    elif percentage >= 40:
        assert recommendation == "WEAK_MATCH"
    else:
        assert recommendation == "NEEDS_MANUAL_REVIEW"

import pytest
@pytest.mark.integration
def test_single_candidate_run_creates_json_report():
    pass
