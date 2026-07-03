import os
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from src.database import KnowledgeBase
from src.guardrails_config import SafetyGuardrails

class SupportAgent(BaseModel):
    answer: str = Field(description="The response should match target data context")
    confidence_score: float = Field(description="Value scale 0.0 to 1.0.")

groq_model = OpenAIModel(model_name="llama-3.3-70b-versatile",base_url="https://groq.com",api_key=os.environ["GROQ_API_KEY"])

support_agent = Agent(groq_model,
    result_type=SupportAgent,
    system_prompt=(
        "You are an expert assistant. You have to provide answers based on the context provided only.\n"
              "If context cannot resolve the prompt set confidence_score to 0.0."))

class RAGChatbot:
    def __init__(self):
        self.knowledge = KnowledgeBase()
        self.guardrails = SafetyGuardrails()

    def run_user_query(self, user_query: str) -> dict:
        good_query = self.guardrails.clean_query(user_query)
        
        contexts = self.knowledge.query_context(good_query, n_results=3)
        formatted_context = "\nThe formated text is:\n".join(contexts)

        agent_prompt = f"QUERY: {good_query}\n\nCONTEXT:\n{formatted_context}"
        response_result = support_agent.run_sync(agent_prompt)
        
        structured_data = response_result.data

        return {"answer": structured_data.answer,"retrieval_context": contexts,"confidence_score": structured_data.confidence_score}
