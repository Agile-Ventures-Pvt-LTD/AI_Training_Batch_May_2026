from groq_client import call_llm
from config import run_case, save_output
import prompts as p

def run_all():

    # ZERO SHOT
    r1 = run_case("zero_shot_output", p.ZERO_SHOT_PROMPT, call_llm)
    save_output("sample_blog_output.json", r1)

    #ZERO SHOT 2
    r2 = run_case("zero_shot_3_output", p.ZERO_SHOT_PROMPT_02, call_llm)
    save_output("sample_blog_output.json", r2)

    # ROLE SHOT
    r3 = run_case("role_shot_ticket", p.ROLE_SHOT_PROMPT, call_llm)
    save_output("sample_blog_output.json", r3)

    # FEW SHOT
    r4= run_case("few_shot_prompt", p.FEW_SHOT_PROMPT, call_llm)
    save_output("sample_blog_output.json", r4)

    # COT
    r5 = run_case("cot_prompt", p.COT_PROMPT, call_llm)
    save_output("sample_blog_output.json", r5)

    #TOT
    r6 = run_case("tot_prompt", p.TOT_PROMPT, call_llm)
    save_output("sample_blog_output.json", r6)

    
    print("All cases executed successfully.")

if __name__ == "__app__":
    run_all()