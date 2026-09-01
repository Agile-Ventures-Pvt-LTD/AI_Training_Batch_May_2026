from langchain_core.prompts import ChatPromptTemplate

QUERY_CLASSIFICATION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an AI assistant that classifies user queries for a RAG system.
     Classify the query into one of the following types:
     FACTUAL_LOOKUP
     SUMMARY
     COMPARISON
     RISK_ANALYSIS
     UNANSWERABLE_OR_SPECULATIVE
     OTHER
     
     {format_instructions}
     
     IMPORTANT: Return ONLY the JSON object. No conversational filler.
     """),
     ("human", "{query}")
])

RAG_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an enterprise knowledge assistant.
     Answer the user question using only the context given.
     Rules:
     - Do not use outside knowledge.
     - If the answer is not available in the context, say: "I couldn't find it in the documents."
     - Mention the source file and page number or chunk ID for each key claim.
     - Do not invent numbers, dates, risks, or conclusions.

     Retrieved context:
     {context}

     {format_instructions}

     IMPORTANT: Return ONLY the JSON object. No conversational filler or preamble.
     """),
     ("human","{query}")
])