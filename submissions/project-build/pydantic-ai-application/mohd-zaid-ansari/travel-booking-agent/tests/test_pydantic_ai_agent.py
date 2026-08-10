import pytest
from pydantic_ai import Agent
from deepeval import assert_test
from deepeval.dataset import EvaluationDataset, Golden
from deepeval.integrations.pydantic_ai import DeepEvalInstrumentationSettings
from deepeval.metrics import AnswerRelevancyMetric

agent = Agent(
    "groq:llama-3.1-8b-instant",
    system_prompt="Be concise, reply with one sentence.",
    instrument=DeepEvalInstrumentationSettings(name="my-agent"),
)
dataset = EvaluationDataset(
    goldens=[
        Golden(input="What's the weather in Paris?"),
        Golden(input="What's the weather in London?"),
    ]
)

@pytest.mark.parametrize("golden", dataset.goldens)
def test_agent(golden: Golden):
    agent.run_sync(golden.input)
    assert_test(golden=golden, metrics=[AnswerRelevancyMetric()])