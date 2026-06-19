import json
from pathlib import Path
from graph import graph


TEST_QUESTIONS = [ # Sample Questions from PRD
    "Amit says VPN times out after MFA approval. What should we check and what is the next action?"]

def run_tests():
    """THis is used for the testing purpose"""
    results = []
    for question in TEST_QUESTIONS:
        response = graph.invoke({"user_question": question,"query_type": "","issue_type": [],"diagnosis_summary": [],"evidence_used": "","kb_sources": [],"tools_used": [],"diagnostic_signals": {},"recommended_steps": [],"escalation_required": True,"escalation_group": "","safety_notes":[],"confidence": ""})
        results.append({"question": question,"response": response.get("final_response","")})
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)
    with open(output_dir / "evaluation_results.json","w",encoding="utf-8") as f:
        json.dump(results,f,indent=4,ensure_ascii=False)
    print("Results are saved to outputs/evaluation_results.json")

if __name__ == "__main__":
    run_tests()