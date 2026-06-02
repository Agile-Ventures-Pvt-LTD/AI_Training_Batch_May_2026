from groq_client import call_llm
from helper import run_case, save_output
import prompts as p

def run_all():

    # ZERO SHOT
    r1 = run_case("zero_shot_risk", p.ZERO_SHOT_RISK_PROMPT, call_llm)
    save_output("zero_shot_risk.json", r1)

    r2 = run_case("zero_shot_exec", p.ZERO_SHOT_EXEC_MEMO_PROMPT, call_llm)
    save_output("zero_shot_exec.json", r2)

    # FEW SHOT
    r3 = run_case("few_shot_ticket", p.FEW_SHOT_TICKET_PROMPT, call_llm)
    save_output("few_shot_ticket.json", r3)

    r4 = run_case("few_shot_api", p.FEW_SHOT_API_PROMPT, call_llm)
    save_output("few_shot_api.json", r4)

    # COT
    r5 = run_case("cot_roi", p.COT_ROI_PROMPT, call_llm)
    save_output("cot_roi.json", r5)

    r6 = run_case("cot_rca", p.COT_RCA_PROMPT, call_llm)
    save_output("cot_rca.json", r6)

    # LLM JUDGE
    r7 = run_case("llm_judge", p.LLM_JUDGE_PROMPT, call_llm)
    save_output("llm_judge.json", r7)

    r8 = run_case("llm_judge_code", p.LLM_JUDGE_CODE_PROMPT, call_llm)
    save_output("llm_judge_code.json", r8)

    # SELF CONSISTENCY
    r9 = run_case("self_consistency", p.SELF_CONSISTENCY_PROMPT, call_llm)
    save_output("self_consistency.json", r9)

    r10 = run_case("self_consistency_security", p.SELF_CONSISTENCY_SECURITY_PROMPT, call_llm)
    save_output("self_consistency_security.json", r10)

    # TREE OF THOUGHT
    r11 = run_case("tot", p.TOT_PROMPT, call_llm)
    save_output("tot.json", r11)

    r12 = run_case("tot_architecture", p.TOT_ARCHITECTURE_PROMPT, call_llm)
    save_output("tot_architecture.json", r12)

    # REPHRASE
    r13 = run_case("rephrase", p.REPHRASE_PROMPT, call_llm)
    save_output("rephrase.json", r13)

    r14 = run_case("rephrase_technical_requirement", p.REPHRASE_TECHNICAL_REQUIREMENT_PROMPT, call_llm)
    save_output("rephrase_technical_requirement.json", r14)

    print("All cases executed successfully.")

if __name__ == "__main__":
    run_all()