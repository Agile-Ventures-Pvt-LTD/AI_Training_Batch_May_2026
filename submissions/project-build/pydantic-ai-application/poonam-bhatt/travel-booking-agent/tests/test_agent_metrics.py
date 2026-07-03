import os
import sys
import pytest
import asyncio
from dotenv import load_dotenv
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric,ContextualPrecisionMetric
from deepeval.models import DeepEvalBaseLLM
from groq import Groq

# Add parent directory to path for importing local modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.tools.database import SQLProductDatabase
from src.agent import run_db_pipeline

load_dotenv()

# =====================================================================
# 1. Custom DeepEval LLM Wrapper for Groq
# =====================================================================
class GroqDeepEvalModel(DeepEvalBaseLLM):
    def __init__(self, model_name="llama-3.3-70b-versatile"):
        self.model_name = model_name
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def load_model(self):
        return self.model_name

    def generate(self, prompt: str) -> str:
        completion = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        return completion.choices[0].message.content

    async def a_generate(self, prompt: str) -> str:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.generate, prompt)

    def get_model_name(self):
        return self.model_name

# =====================================================================
# 2. Automated DB Agent Evaluation Tests (Pytest)
# =====================================================================

@pytest.mark.asyncio
async def test_db_travel_relevancy():
    """Verify that the database agent correctly answers travel lookup queries using DeepEval."""
    db_connection = SQLProductDatabase("db/travel_data.db")
    
    query = "What is Alice Smith travel destination."
    
    res = await run_db_pipeline(query, db_connection)
    
    assert res["status"] == "SUCCESS", f"DB pipeline failed: {res.get('reason')}"
    
    actual_output = res["answer"]
    
    # Raw SQL logging details returned by the database tool
    retrieval_context = [res["db_logged_data"]]
    
    expected_output = (
        "Alice Smith's travel destination is Paris, France. She is scheduled to travel from 2026-08-15 to 2026-08-20 and stay at the Le Meurice Hotel."
    )
    
    eval_model = GroqDeepEvalModel()
    relevancy_metric = AnswerRelevancyMetric(threshold=0.85, model=eval_model)
    contextual_metric = ContextualPrecisionMetric(threshold=0.80, model=eval_model)
    
    test_case = LLMTestCase(
        input=query,
        actual_output=actual_output,
        expected_output=expected_output,
        retrieval_context=retrieval_context
    )
    
    assert_test(test_case, [relevancy_metric,contextual_metric])
