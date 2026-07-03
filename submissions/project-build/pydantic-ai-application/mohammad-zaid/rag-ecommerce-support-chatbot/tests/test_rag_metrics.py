import os
import sys
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from deepeval import evaluate
from deepeval.metrics import AnswerRelevancyMetric, ContextualPrecisionMetric
from deepeval.test_case import LLMTestCase
from src.database import retrieve_documents, initialize_database
from src.agent import ask_question
import asyncio

# Test cases based on the eBay Advanced Business Seller Guide
TEST_CASES = [
    {
        "input": "How can I become a PowerSeller on eBay?",
        "expected_output": "To become a PowerSeller, you need to sustain a high volume of monthly sales, maintain 98% or better positive feedback, maintain 4.5 or better DSRs in all four areas, keep your account in good financial standing, and accept your invitation to the PowerSeller program.",
        "retrieval_context": None  # Will be populated during test
    },
    {
        "input": "What are the benefits of PowerSeller status?",
        "expected_output": "PowerSeller benefits include prioritized customer service, Final Value Fee discounts up to 20%, Unpaid Item protection, and UPS rate discounts up to 23% on UPS Ground Daily Rates.",
        "retrieval_context": None
    },
    {
        "input": "How can I improve my Detailed Seller Ratings (DSRs)?",
        "expected_output": "To improve DSRs, describe items accurately, upload clear photos, specify shipping costs and return policies, answer emails quickly, keep buyers informed of issues, ship within 24 hours, provide tracking numbers, and set fair shipping charges.",
        "retrieval_context": None
    },
    {
        "input": "What is the formula for calculating Conversion Rate?",
        "expected_output": "Conversion Rate (CR) is calculated as the number of Successful Listings (SL) divided by the number of Total Listings (TL).",
        "retrieval_context": None
    }
]

async def setup_tests():
    """Initialize the database for testing"""
    print("Setting up test environment...")
    await initialize_database(force_reset=False)

def run_tests():
    """Run the DeepEval tests"""
    # Run the async setup
    asyncio.run(setup_tests())
    
    # Initialize metrics
    answer_relevancy_metric = AnswerRelevancyMetric(threshold=0.85)
    contextual_precision_metric = ContextualPrecisionMetric(threshold=0.80)
    
    # Prepare test cases
    test_cases = []
    for case in TEST_CASES:
        # Get retrieval context
        retrieval_context = retrieve_documents(case["input"])
        case["retrieval_context"] = retrieval_context
        
        # Create LLMTestCase
        test_case = LLMTestCase(
            input=case["input"],
            actual_output=asyncio.run(ask_question(case["input"])),
            expected_output=case["expected_output"],
            retrieval_context=retrieval_context
        )
        test_cases.append(test_case)
    
    # Run evaluation
    print("Running DeepEval tests...")
    results = evaluate(
        test_cases=test_cases,
        metrics=[answer_relevancy_metric, contextual_precision_metric]
    )
    
    return results

if __name__ == "__main__":
    results = run_tests()
    print("Test evaluation complete!")