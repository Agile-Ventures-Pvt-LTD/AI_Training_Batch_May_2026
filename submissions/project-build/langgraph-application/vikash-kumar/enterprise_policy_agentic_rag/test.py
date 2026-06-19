import json
from pathlib import Path
from graph import graph


TEST_QUESTIONS = [ # Sample Questions from PRD
    "How many annual leave days can an employee carry forward?",
    "Can I claim meals for same-day domestic business travel?",
    "What documents are needed for hotel reimbursement?",
    "Can I use my personal laptop for office work?",
    "What approvals are needed for international travel?",
    "Can customer data be uploaded to a public AI tool?",
    "Will my reimbursement definitely be approved?",
    "What should I do if the policy does not mention my scenario?"]

def run_tests():
    """THis is used for the testing purpose"""
    results = []
    for question in TEST_QUESTIONS:
        response = graph.invoke({"user_question": question,"query_type": "","required_policy_domains": [],"requires_clarification": False,"rewritten_query": "","retrieved_context": [],"context_grade": {},"answer": {},"reflection": {},"retry_count": 0,"final_response": ""})
        results.append({"question": question,"response": response.get("final_response","")})
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)
    with open(output_dir / "evaluation_results.json","w",encoding="utf-8") as f:
        json.dump(results,f,indent=4,ensure_ascii=False)
    print("Results saved to outputs/evaluation_results.json")

if __name__ == "__main__":
    run_tests()