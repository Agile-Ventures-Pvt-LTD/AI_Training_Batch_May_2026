import deepeval
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric
from deepeval.evaluate import evaluate

answer_relevancy_metric = AnswerRelevancyMetric()

test_case = LLMTestCase(
  input="Who is the current president of the United States of America?",
  actual_output=llm.invoke("Who is the current president of the United States of America? just give me the name no explainations needed").content,
)

evaluate(test_cases=[test_case], metrics=[answer_relevancy_metric])


for golden in dataset.goldens:
    test_case = LLMTestCase(
        input=golden.input,                     
        expected_output=golden.expected_output,  
        actual_output=chain.invoke(golden.input),   
        retrieval_context=[retrieve_and_format(golden.input)]  
    )

    dataset.add_test_case(test_case)