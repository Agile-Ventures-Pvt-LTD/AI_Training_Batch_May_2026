from deepeval import evaluate
from deepeval.metrics import AnswerRelevancyMetric, ContextualPrecisionMetric
from deepeval.test_case import LLMTestCase
from src.agent import run_rag_pipeline

cases = [

    

    (
        "How to Optimize your listings for search engines?",
        "How to Refine promotion strategy?",
        "What is UPS Savings Program for eBay PowerSellers?"
    ),

   
]

metric1 = AnswerRelevancyMetric(
    threshold=8.5
)

metric2 = ContextualPrecisionMetric(
    threshold=8.0
)

tests = []

for question, expected in cases:

    actual = run_rag_pipeline(question)

    tests.append(
        LLMTestCase(
            input=question,
            actual_output=str(actual),
            expected_output=expected
        )
    )

evaluate(
    test_cases=tests,
    metrics=[metric1,metric2]
)


# Project: P005 RAG Ecommerce support chatbot
# Author: Poonam Bhatt