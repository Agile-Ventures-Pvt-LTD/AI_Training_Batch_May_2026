import os
import deepeval
from dotenv import load_dotenv
from deepeval.test_case import LLMTestCase, ToolCall
from deepeval.dataset import EvaluationDataset
from deepeval.metrics import AnswerRelevancyMetric, ContextualPrecisionMetric, ToolCorrectnessMetric

load_dotenv()

os.environ["LOCAL_MODEL_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["CONFIDENT_API_KEY"] = os.getenv("CONFIDENT_API_KEY")

deepeval.login(os.environ["CONFIDENT_API_KEY"])

deepeval.set_local_model(
    model="openai/gpt-oss-20b",
    base_url="https://api.groq.com/openai/v1"
)


test_cases = [
    LLMTestCase(
        input="Who is Travelling to France?",
        tools_called=[ToolCall("search_database_tool")],
        actual_output="Alice Smith is Travelling to France",
        expected_output="Alice Smith is Travelling to France",
        expected_tools=[ToolCall("search_database_tool")]
    ),
    LLMTestCase(
        input="What is the Weather of Berlin",
        tools_called=[ToolCall("search_weather_tool")],
        actual_output="20 degree celsius",
        expected_output="20 degree celsius",
        expected_tools=[ToolCall("search_weather_tool")]
    ),
    LLMTestCase(
        input="Were is Bob jones is going travel?",
        tools_called=[ToolCall("search_database_tool")],
        actual_output="Tokyo and Japan",
        expected_output="Tokyo and Japan",
        expected_tools=[ToolCall("search_database_tool")]
    ),
    LLMTestCase(
        input="Which of them are going travel same city?",
        tools_called=[ToolCall("search_database_tool")],
        actual_output="Charlie Davis and Diana Prince",
        expected_output="Charlie Davis and Diana Prince",
        expected_tools=[ToolCall("search_database_tool")]
    ),
    LLMTestCase(
        input="What is the weather going to be like for Alice Smith in upcoming trip?",
        tools_called=[ToolCall("search_database_tool"), ToolCall("search_weather_tool")],
        actual_output="The weather of France and Paris is going to be 26 degree celsius",
        expected_output="The weather of France and Paris is going to be 26 degree celsius",
        expected_tools=[ToolCall("search_database_tool"), ToolCall("search_weather_tool")]
    )
]


dataset = EvaluationDataset()
dataset.add_test_case(test_case=test_cases)

deepeval.evaluate(dataset.test_cases, metrics=[AnswerRelevancyMetric(threshold=0.85), ContextualPrecisionMetric(threshold=0.80), ToolCorrectnessMetric()])
