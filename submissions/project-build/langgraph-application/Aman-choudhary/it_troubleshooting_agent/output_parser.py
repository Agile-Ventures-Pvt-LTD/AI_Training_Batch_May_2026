def format_output(data):
    return {"issue_type":data.get("issue_type","UNKNOWN"),
        "diagnosis_summary":
        data.get(
            "diagnosis_summary",
            ""
        ),
        "recommended_steps":
        data.get(
            "recommended_steps",
            []
        ),
        "escalation_required":
        data.get(
            "escalation_required",
            False
        ),
        "confidence":
        data.get(
            "confidence",
            "MEDIUM"
        )
    }