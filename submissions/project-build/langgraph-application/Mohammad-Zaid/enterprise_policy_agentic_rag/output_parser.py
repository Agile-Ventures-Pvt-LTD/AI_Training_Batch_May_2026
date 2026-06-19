def parse_agent_output(response):
    if isinstance(response, dict):
        output = response.get("output", "")
    else:
        output = str(response)
    
    return {
        "answer": output,
        "supporting_evidence": extract_evidence(output),
        "sources": extract_sources(output),
        "confidence": determine_confidence(output),
    }


def extract_evidence(output):
    if "Supporting Evidence:" in output:
        return output.split("Supporting Evidence:")[1].split("\n")[0]
    return "See full response for evidence"


def extract_sources(output):
    sources = []
    if "Source:" in output:
        lines = output.split("\n")
        for line in lines:
            if "Source:" in line:
                sources.append(line.strip())
    return sources if sources else ["See full response for sources"]


def determine_confidence(output):
    if "could not find" in output.lower():
        return "Low"
    elif "Confidence: High" in output:
        return "High"
    elif "Confidence: Medium" in output:
        return "Medium"
    else:
        return "Medium"


def format_final_response(structured_output):
    return f"""
ANSWER:
{structured_output.get('answer', 'No answer available')}

SUPPORTING EVIDENCE:
{structured_output.get('supporting_evidence', 'N/A')}

SOURCES:
{', '.join(structured_output.get('sources', ['N/A']))}

CONFIDENCE: {structured_output.get('confidence', 'Unknown')}
""".strip()
