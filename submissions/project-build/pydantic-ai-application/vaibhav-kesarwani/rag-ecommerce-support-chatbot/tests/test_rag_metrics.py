import os
from pydantic_evals import Case, Dataset
from pydantic_evals.evaluators import LLMJudge
from src.agent import agent
from src.database import pdf_chunks
from src.schema import RagDeps, RagInputs, RagOutput
from src.prompts import agent_groundness
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

os.envinron["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
model = "openai/gpt-oss-20b"

llm = ChatGroq(model=model, api_key=os.environ["GROQ_API_KEY"])

datasets = Dataset[RagInputs, RagOutput](
    cases=[
        Case(
            name="profitability",
            inputs=RagInputs(
                query="what is the profitability to the seller?",
                expected_docs=["5", "6"],
                grounded_answer="A business's ability to increase its profits or profit margin."
            )
        ),
        Case(
            name="optimize_automate",
            inputs=RagInputs(
                query="How to optimize and automate the shipping time?",
                expected_docs=["7", "8", "9"],
                grounded_answer="When you let packages pile up, getting them out the door tends to take more time. Consider shipping daily instead of once or twice a week. Most sellers see shipping time DSRs improve when they ship within 24 hours of receiving payment. It's easier than you think, especially if you stop going to the Post Office."
            )
        ),
        Case(
            name="advance_marketing",
            inputs=RagInputs(
                query="How to do the advance marketing in eBay?",
                expected_docs=["10", "11", "12", "13"]
            )
        )
    ]
)


try:
    datasets.add_evaluator(
        LLMJudge(
            rubric=agent_groundness,    
            include_input=True,
            include_expected_output=True,
            model=llm
        )
    )

except Exception as e:
    print(e)


def rag_agent(query: str) -> RagOutput:
    result = agent.run_sync(user_prompt=query, deps=RagDeps(documents=pdf_chunks()))
    response = result.output
    
    return {"answer" : response.reponse, "used_id" : response.res_id}


report = datasets.evaluate_sync(rag_agent)
report.print()