from datetime import datetime


def format_response(user_question,answer,tools_used=None,records_found=0):
    return {
        "timestamp": datetime.now().isoformat(),
        "user_question": user_question,
        "implementation_choice": "prebuilt_react_agent",
        "tools_used": tools_used or [],
        "records_found": records_found,
        "answer": answer,
        "sensitive_data_masked": True
    }