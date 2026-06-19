import json
from datetime import datetime
from config import OUTPUT_DIR


def save_agent_output(answer,policy_basis,sources,answerability="ANSWERED",confidence="HIGH",
                      recommended_next_step="",
                      filename="evaluation_results.json"):
    """Save final agent output in expected format to evaluation_results.json"""
    
    output = {
        "answer": answer,
        "policy_basis": policy_basis,
        "sources": sources,
        "answerability": answerability,
        "confidence": confidence,
        "recommended_next_step": recommended_next_step
    }
    
    filepath = OUTPUT_DIR / filename
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    with open(filepath, "w") as f:
        json.dump(output, f, indent=2)
    
    return str(filepath)
