import os
from dotenv import load_dotenv
from src.crew import resume_screening_crew
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric, ContextualPrecisionMetric, ContextualRecallMetric, FaithfulnessMetric
import deepeval
from evaluation_prompts import expected_ouput

load_dotenv()

os.environ["LOCAL_MODEL_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["CONFIDENT_API_KEY"] = os.getenv("CONFIDENT_API_KEY")

deepeval.login(os.environ["CONFIDENT_API_KEY"])

deepeval.set_local_model(
    model="openai/gpt-oss-20b",
    base_url="https://api.groq.com/openai/v1"
)


test_case = LLMTestCase(
    input="What is the job Description?",
    actual_output=resume_screening_crew,
    expected_output=expected_ouput
)


metrics = [AnswerRelevancyMetric(), FaithfulnessMetric(), ContextualPrecisionMetric(), ContextualRecallMetric()]