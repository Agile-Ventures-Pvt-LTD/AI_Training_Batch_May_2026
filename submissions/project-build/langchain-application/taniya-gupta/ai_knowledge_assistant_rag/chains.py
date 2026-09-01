from langchain_groq import ChatGroq
from langchain_core.runnables import RunnableLambda
from prompts import QUERY_CLASSIFICATION_PROMPT, RAG_PROMPT
from output_parser import classification_parser, answer_parser

from operator import itemgetter

class ChainManager:
    def __init__(self, api_key, model_name):
        self.llm = ChatGroq(
            groq_api_key=api_key,
            model_name=model_name,
            temperature=0
        )

    def get_classification_chain(self):
        return ({"query": itemgetter("query"), "format_instructions": lambda _: classification_parser.get_format_instructions()} 
                | QUERY_CLASSIFICATION_PROMPT | self.llm | classification_parser)

    def get_rag_chain(self):
        def format_docs(docs):
            formatted = []
            for doc in docs:
                content = doc.page_content
                metadata = doc.metadata
                source = metadata.get("source_file", "unknown")
                page = metadata.get("page_number", "unknown")
                chunk_id = metadata.get("chunk_id", "unknown")
                formatted.append(f"Source: {source}, Page: {page}, Chunk: {chunk_id}\nContent: {content}")
            return "\n\n".join(formatted)

        return ({"context": itemgetter("context") | RunnableLambda(format_docs), 
                 "query": itemgetter("question"),
                 "format_instructions": lambda _: answer_parser.get_format_instructions()}
            | RAG_PROMPT | self.llm | answer_parser)

