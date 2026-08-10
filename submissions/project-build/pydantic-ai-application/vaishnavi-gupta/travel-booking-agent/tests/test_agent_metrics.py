import os 
import deepeval
from deepeval.test_case import LLMTestCase
from deepeval.test_case import ToolCall
from deepeval.metrics import AnswerRelevancyMetric
from deepeval.metrics import ContextualPrecisionMetric
from deepeval.dataset import EvaluationDataset


dataset = EvaluationDataset()
dataset.add_test_case(test_case)

os.environ["LOCAL_MODEL_API_KEY"] = os.environ["OPENAI_API_KEY"]

test_case = LLMTestCase(

    input=question,           

    tools_called=[ToolCall(name=get_tools_called(result)[-1])],                

    actual_output=result.output,    

    expected_output=result.output,  

    expected_tools=[ToolCall(name = 'retrieve_docs')] 
    )


print(test_case.input)

print(test_case.actual_output)

print(test_case.expected_output)

print(test_case.tools_called)

print(test_case.expected_tools)


deepeval.evaluate(dataset.test_cases, metrics= [AnswerRelevancyMetric()])
deepeval.evaluate(dataset.test_cases, metrics= [ContextualPrecisionMetric()])