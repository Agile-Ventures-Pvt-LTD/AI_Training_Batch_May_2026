
def parse_rag_response(response_text):
    return {
        "answer": response_text,
        "supporting_evidence": [],
        "sources": [],
        "confidence": "MEDIUM",
        "answerability": "ANSWERED",
    }


def format_answer_for_display(answer_text):
    return answer_text
