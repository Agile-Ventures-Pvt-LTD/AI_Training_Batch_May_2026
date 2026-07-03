import sys
import os
import pytest
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric, ContextualPrecisionMetric
from deepeval.models.base_model import DeepEvalBaseLLM
from groq import Groq

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from database import initialize_database
from agent import respond

print("Initializing database for tests")
collection = initialize_database()

class GroqEvaluationModel(DeepEvalBaseLLM):
    def __init__(self, model_name="llama-3.3-70b-versatile"):
        self.model_name = model_name

        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            openai_key = os.environ.get("OPENAI_API_KEY")
            if openai_key and openai_key.startswith("gsk_"):
                api_key = openai_key
        if not api_key:
            raise ValueError("Groq API Key not found for evaluation.")
        self.client = Groq(api_key=api_key)

    def load_model(self):
        return self.client

    def generate(self, prompt: str) -> str:
        chat_completion = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.model_name,
            temperature=0.0
        )
        return chat_completion.choices[0].message.content.strip()

    async def a_generate(self, prompt: str) -> str:
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.generate, prompt)

    def get_model_name(self):
        return self.model_name

eval_model = GroqEvaluationModel()
relevancy_metric = AnswerRelevancyMetric(threshold=0.85, model=eval_model)
precision_metric = ContextualPrecisionMetric(threshold=0.80, model=eval_model)

test_cases_data = [
    {
        "input": "How is the Average Selling Price (ASP) calculated?",
        "expected": "Average Selling Price (ASP) is calculated by dividing total sales revenue by the number of items sold over a specific period."
    },
    {
        "input": "What are Detailed Seller Ratings (DSRs) and why do they matter?",
        "expected": "Detailed Seller Ratings (DSRs) are anonymous ratings left by buyers across description, communication, shipping time, and shipping cost. They impact search placement and PowerSeller status."
    },
    {
        "input": "What happens if a seller receives low Detailed Seller Ratings (DSRs)?",
        "expected": "Low DSRs can result in account restrictions, lower search placement, loss of PowerSeller status, or suspension of the seller's account."
    }
]

@pytest.mark.parametrize("case", test_cases_data)
def test_rag_chatbot_metrics(case):
    actual_output = respond(case["input"], collection)

    query_results = collection.query(
        query_texts=[case["input"]],
        n_results=5
    )
    docs = query_results.get("documents", [[]])[0]
    retrieval_context = [doc for doc in docs]
    
    test_case = LLMTestCase(
        input=case["input"],
        actual_output=actual_output,
        expected_output=case["expected"],
        retrieval_context=retrieval_context
    )
    
    assert_test(test_case, [relevancy_metric, precision_metric])
