from langchain_core.prompts import PromptTemplate

grade_context_prompt = PromptTemplate(
    template="""
You are a policy retrieval evaluator.
Question:
{question}
Context:
{context}
Return only one:
HIGHLY_RELEVANT
PARTIALLY_RELEVANT
WEAK
NOT_RELEVANT
"""
)

rewrite_query_prompt = PromptTemplate(
    template= """
Rewrite this enterprise policy question
to improve retrieval quality.
Question:
{question}
"""
)
ask_clarification_prompt = PromptTemplate(
    template= """
The user question is ambiguous.
Question:
{question}
Ask one clear clarification question.
"""
)

generate_grounded_answer_promot = PromptTemplate(
    template= """
You are an Enterprise Policy Assistant.
Use only the provided context.
Question:
{question}
Context:
{context}
Requirements:
- Do not hallucinate.
- Do not invent policy rules.
- Mention if information is missing.
- Include source references.
"""
)

review_answer_grounding_prompt = PromptTemplate(
    template= """
Review the answer.
Answer:
{answer}
Context:
{context}
Return:
GROUNDED
or
NOT_GROUNDED
with a short reason.
"""
)