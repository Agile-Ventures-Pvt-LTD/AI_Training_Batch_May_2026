import json

from langchain_groq import ChatGroq
from config import GROQ_MODEL
from prompts import Query_Classification_Prompt,RAG_Prompt
from retriever import Retriever,format_context


class RAGChains:
    def __init__(self,vector_store):
        self.llm = ChatGroq(model=GROQ_MODEL,temperature=0)

        self.retriever = Retriever(vector_store)
    
    def classify_query(self,question):
        prompt = Query_Classification_Prompt.format(question=question)
        response = self.llm.invoke(prompt)

        try:
            return json.loads(response.content)
        except:
            return {
                "query_type":"OTHER",
                "requires_retrival":True
            }
    
    def generate_answer(self,question):
        docs = self.retriever.retrieve(question)

        if not docs:
            return {
                "answer":"I could not find this in the provided documents.",
                "confidence":"LOW",
                "answerability":"NOT_FOUND",
                "sources":[]
            }
        context = format_context(docs)

        prompt = RAG_Prompt.format(question=question,context=context)

        response = self.llm.invoke(prompt)

        return response.content
    
    def get_sources(self, docs):

       sources = []

       for doc in docs:

        sources.append(
            {
                "source_file":
                    doc.metadata.get("source_file"),

                "page_number":
                    doc.metadata.get("page_number"),

                "chunk_id":
                    doc.metadata.get( "chunk_id"),

                "similarity_score":
                    doc.metadata.get("similarity_score")
            }
        )

       return sources