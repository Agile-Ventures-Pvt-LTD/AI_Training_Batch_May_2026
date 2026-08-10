import logging
from typing import Dict, Any

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

import config
import output_parser as op
from tools import (
    retrieve_hr_policy,
    retrieve_travel_policy,
    retrieve_reimbursement_policy,
    retrieve_it_security_policy,
    retrieve_ai_usage_policy,
    generate_grounded_answer,
    rewrite_query,
)

logger = logging.getLogger(__name__)


AGENT_SYSTEM_PROMPT = """You are an enterprise policy assistant. Answer employee questions strictly using internal policy documents.

Follow this exact workflow:

Step 1 — Retrieve: Call the relevant retrieve tool(s) based on the question topic.
  - HR leave questions → retrieve_hr_policy
  - Travel questions → retrieve_travel_policy
  - Expense/reimbursement questions → retrieve_reimbursement_policy
  - Laptop/device/password questions → retrieve_it_security_policy
  - AI tools/customer data questions → retrieve_ai_usage_policy
  - Multi-topic questions → call multiple retrieve tools

Step 2 — Answer: Call generate_grounded_answer with the question and the JSON returned by the retrieve tool(s).

Step 3 — Respond: Return the exact JSON output from generate_grounded_answer directly to the user. Do not paraphrase, summarize, or add any text outside the JSON. Your final message must be only the raw JSON object.

If generate_grounded_answer returns NOT_FOUND:
  - Try rewrite_query once, retrieve again, then call generate_grounded_answer again.
  - If still NOT_FOUND, tell the user to contact HR, Finance, IT Security, or AI Governance.

Rules:
- Never answer from memory or general knowledge.
- Never guarantee approval of any request.
- Never invent policy rules, limits, or amounts.
"""

_agent = None


def get_agent():
    global _agent
    if _agent is not None:
        return _agent

    if not config.GROQ_API_KEY:
        raise EnvironmentError("GROQ_API_KEY is not set in .env")

    llm = ChatGroq(
        model=config.GROQ_MODEL,
        api_key=config.GROQ_API_KEY,
        temperature=0,
    )

    tools = [
        retrieve_hr_policy,
        retrieve_travel_policy,
        retrieve_reimbursement_policy,
        retrieve_it_security_policy,
        retrieve_ai_usage_policy,
        rewrite_query,
        generate_grounded_answer,
    ]

    _agent = create_react_agent(model=llm, tools=tools, prompt=AGENT_SYSTEM_PROMPT)
    return _agent


def run_agent(question: str) -> Dict[str, Any]:
    if not question or not question.strip():
        return {
            "answer": "Please enter a specific policy question.",
            "answerability": "NEEDS_CLARIFICATION",
            "confidence": "LOW",
            "sources": [],
            "recommended_next_step": "Type your question and try again.",
        }
        

    try:
        result = get_agent().invoke({"messages": [HumanMessage(content=question)]})
        messages = result.get("messages", [])

        final_text = None
        for msg in reversed(messages):
            if msg.__class__.__name__ == "AIMessage" and msg.content and msg.content.strip():
                final_text = msg.content
                break

        if not final_text:
            return {
                "answer": "No response generated. Try rephrasing your question.",
                "answerability": "NOT_FOUND",
                "confidence": "LOW",
                "sources": [],
                "recommended_next_step": "Rephrase and try again.",
            }
             
        parsed = op.parse_json_response(final_text, "agent_final_response")
        if parsed and "answer" in parsed:
            return parsed

        return {
            "answer": final_text,
            "policy_basis": [],
            "sources": [],
            "answerability": "PARTIALLY_ANSWERED",
            "confidence": "MEDIUM",
            "recommended_next_step": "Check the source policy document for full details.",
        }

    except Exception as e:
        logger.error("Agent failed for '%s': %s", question[:80], e, exc_info=True)
        return {
            "answer": "Something went wrong while processing your question.",
            "error": str(e),
            "answerability": "NOT_FOUND",
            "confidence": "LOW",
            "sources": [],
            "recommended_next_step": "Contact HR, Finance, or IT Security directly.",
        }
        
    
        
        
