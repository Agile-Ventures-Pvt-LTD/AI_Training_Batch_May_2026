import json
from langchain_groq import ChatGroq
from config import Config
from prompts import CLASSIFIER_PROMPT, QA_PROMPT

class RAGChain:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0.0,
            model_name=Config.GROQ_MODEL,
            api_key=Config.GROQ_API_KEY
        )

    def cleaning_json(self, txt: str):
        """cleaning json for preventing errors"""
        txt = txt.strip()
        if txt.startswith("```json"):
            txt = txt.split("```json")[-1].split("```")[0].strip()
        elif txt.startswith("```"):
            txt = txt.split("```")[1].strip()
        try:
            return json.loads(txt)
        except Exception as e:
            return {"error": "JSON parse error", "raw": txt}

    def classify(self, query: str):
        res = self.llm.invoke(CLASSIFIER_PROMPT.format(query=query))
        return self.cleaning_json(res.content)

    def generate(self, query: str, context: str):
        res = self.llm.invoke(QA_PROMPT.format(question=query, context=context))
        return self.cleaning_json(res.content)