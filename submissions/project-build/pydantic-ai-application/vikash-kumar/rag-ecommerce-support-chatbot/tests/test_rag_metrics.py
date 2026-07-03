import os
import pytest
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import FaithfulnessMetric, AnswerRelevancyMetric
from src.agent import RAGChatbot

@pytest.fixture(scope="module")
def app_workflow():
    return RAGChatbot()

def test_compliance(app_workflow):
    query = "What is the shipping time"
    expected_output = "Ship within 24 hours of receiving payment."

    result = app_workflow.run_query(query)

    test_case = LLMTestCase(input=query,actual_output=result["answer"],expected_output=expected_output,retrieval_context=result["retrieval_context"])

    faithfulness_metric = FaithfulnessMetric(threshold=0.8)
    relevance_metric = AnswerRelevancyMetric(threshold=0.8)

    assert_test(test_case, [faithfulness_metric, relevance_metric])

def test_profit(app_workflow):
    query = "How do you calculate Conversion Rate on the platform?"
    
    result = app_workflow.run_query(query)
    
    test_case = LLMTestCase(input=query,actual_output=result["answer"],retrieval_context=result["retrieval_context"])
    
    faithfulness_metric = FaithfulnessMetric(threshold=0.8)
    assert_test(test_case, [faithfulness_metric])
