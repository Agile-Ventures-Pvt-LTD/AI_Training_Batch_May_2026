from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from src.prompts.system_prompts import SYSTEM_PROMPT
from src.tools.ecommerce_sql_tool import query_ecommerce_database

import os
from dotenv import load_dotenv
load_dotenv()

os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')

class EcommerceAgent:

    def __init__(self):

        self.llm = ChatGroq(
            api_key=os.environ['GROQ_API_KEY'],
            model="openai/gpt-oss-120b",
            temperature=0
        )

        self.sql_generation_chain = LLMChain(
            llm=self.llm,
            prompt=self._sql_prompt()
        )

        self.answer_chain = LLMChain(
            llm=self.llm,
            prompt=self._answer_prompt()
        )

    def _sql_prompt(self):

        template = """
        {system_prompt}

        Convert the user question into a valid SQLite SELECT query.

        Rules:

        - Return ONLY SQL
        - No explanation
        - No markdown
        - Only SELECT statements

        User Question:
        {question}
        """

        return PromptTemplate(
            input_variables=[
                "system_prompt",
                "question"
            ],
            template=template
        )

    def _answer_prompt(self):

        template = """
        You are an Ecommerce Business Analyst.

        User Question:
        {question}

        SQL Result:
        {result}

        Create a concise business-friendly answer.

        Do not mention SQL.

        If no data found, clearly say so.
        """

        return PromptTemplate(
            input_variables=[
                "question",
                "result"
            ],
            template=template
        )

    def run(self, user_question):

        generated_sql = self.sql_generation_chain.run(
            {
                "system_prompt": SYSTEM_PROMPT,
                "question": user_question
            }
        )

        print("\nGenerated SQL:\n")
        print(generated_sql)

        sql_result = query_ecommerce_database.run(
            generated_sql
        )

        print("\nDatabase Result:\n")
        print(sql_result)

        final_answer = self.answer_chain.run(
            {
                "question": user_question,
                "result": sql_result
            }
        )

        return {
            "generated_sql": generated_sql,
            "database_result": sql_result,
            "final_answer": final_answer
        }