import os
from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq

from langchain_core.prompts import ChatPromptTemplate
from prompts.system_prompt import SYSTEM_PROMPT
from tools.sql_tool import query_database

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.environ["GROQ_API_KEY"],
    temperature=0
)

sql_generation_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("human",
            """Convert the user's question into a SQL SELECT query.
            Return ONLY SQL.
Question:
{question}
"""
        ),
    ]
)

sql_chain = sql_generation_prompt | llm

response_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an e-commerce business analyst.

Explain database results in clear business language.

Rules:
- Do not mention SQL.
- Do not mention databases.
- Be concise.
- If no records are found, say so.
- Do not invent information.
"""
        ),
        (
            "human",
            """
User Question:
{question}

Database Result:
{result}
"""
        ),
    ]
)

response_chain = response_prompt | llm

def clean_sql(sql: str) -> str:
    return (
        sql.replace("```sql", "")
        .replace("```", "")
        .strip()
    )


def answer_business_question(question: str) -> str:
    # Step 1: Generate SQL
    sql_response = sql_chain.invoke(
        {"question": question}
    )

    sql_query = clean_sql(sql_response.content)

    print("\nGenerated SQL:")
    print(sql_query)

    # Step 2: Execute SQL
    db_result = query_database.invoke(
        {"query": sql_query}
    )

    if "error" in db_result:
        return f"Error: {db_result['error']}"

    # Step 3: Generate final answer
    final_response = response_chain.invoke(
        {
            "question": question,
            "result": str(db_result),
        }
    )

    return final_response.content