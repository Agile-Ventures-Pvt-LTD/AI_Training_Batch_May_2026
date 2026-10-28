import os
from dotenv import load_dotenv
from prebuilt_agent import agent
from deepeval.test_case import ToolCall, LLMTestCase
from deepeval.metrics import ToolCorrectnessMetric, AnswerRelevancyMetric, ContextualPrecisionMetric, ContextualRecallMetric
import deepeval

load_dotenv()

os.environ["LOCAL_MODEL_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["CONFIDENT_API_KEY"] = os.getenv("CONFIDENT_API_KEY")

deepeval.login(os.environ["CONFIDENT_API_KEY"])

deepeval.set_local_model(
    model="openai/gpt-oss-20b",
    base_url="https://api.groq.com/openai/v1"
)

user_question = "How many annual leave days can an employee carry forward?"
response = agent.invoke({"messages": [{"role": "user", "content": user_question}]})

tool_name = "policies_retriever"
 
test_case = LLMTestCase(
    input=response["messages"][0].content,              
    tools_called=[ToolCall(name=tool_name)],            
    actual_output=response["messages"][-1].content,     
    expected_output=response["messages"][-1].content,   
    expected_tools=[ToolCall(name=tool_name)]       
)    

deepeval.evaluate([test_case], [ToolCorrectnessMetric(), AnswerRelevancyMetric(), ContextualPrecisionMetric(), ContextualRecallMetric()])
