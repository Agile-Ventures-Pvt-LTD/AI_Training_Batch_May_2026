import json
from typing import Optional


def parse_agent_output(agent_response):
    """
    Parse agent response into standardized JSON format.
    Ensures all required fields are present.
    """
    
    # Extract output from agent response
    if isinstance(agent_response, dict):
        if "messages" in agent_response:
            # New format: messages list from langgraph
            messages = agent_response.get("messages", [])
            if messages:
                # Get last message content
                last_msg = messages[-1]
                if hasattr(last_msg, 'content'):
                    output = last_msg.content
                else:
                    output = str(last_msg)
            else:
                output = "No response from agent"
        else:
            # Fallback to old format
            output = agent_response.get("output", str(agent_response))
    else:
        output = str(agent_response)
    
    parsed = {
        "issue_type": extract_issue_type(output),
        "diagnosis_summary": extract_diagnosis(output),
        "evidence_used": extract_evidence(agent_response),
        "recommended_steps": extract_steps(output),
        "escalation_required": check_escalation(output),
        "escalation_group": extract_escalation_group(output),
        "safety_notes": extract_safety_notes(output),
        "confidence": determine_confidence(output)
    }
    
    return parsed


def extract_issue_type(output: str) -> str:
    """Extract or infer issue type from output."""
    output_lower = output.lower()
    
    types = {
        "VPN": ["vpn", "connection timeout", "mfa"],
        "OUTLOOK_EMAIL": ["outlook", "email", "webmail", "sync"],
        "LAPTOP_PERFORMANCE": ["slow", "cpu", "memory", "disk", "performance"],
        "PASSWORD_RESET": ["password", "login", "reset", "account locked"],
        "NETWORK_CONNECTIVITY": ["network", "internet", "dns", "connectivity"],
        "PRINTER": ["printer", "printing", "driver"],
    }
    
    for issue_type, keywords in types.items():
        if any(kw in output_lower for kw in keywords):
            return issue_type
    
    return "UNKNOWN"


def extract_diagnosis(output: str) -> str:
    """Extract diagnosis summary from agent output."""
    lines = output.split("\n")
    
    for i, line in enumerate(lines):
        if "diagnosis" in line.lower() or "issue" in line.lower():
            return line.strip()
    
    return lines[0] if lines else "Unable to extract diagnosis"


def extract_evidence(agent_response) -> dict:
    """Extract evidence from tools used and KB sources."""
    evidence = {
        "kb_sources": [],
        "tools_used": [],
        "diagnostic_signals": []
    }
    
    # Parse tool calls from agent response
    if "intermediate_steps" in agent_response:
        for step in agent_response["intermediate_steps"]:
            if hasattr(step[0], "tool"):
                evidence["tools_used"].append(step[0].tool)
    
    return evidence


def extract_steps(output: str) -> list:
    """Extract recommended steps from output."""
    steps = []
    lines = output.split("\n")
    
    step_keywords = ["step", "action", "next", "check", "verify", "run"]
    
    for line in lines:
        line = line.strip()
        if any(kw in line.lower() for kw in step_keywords) and len(line) > 5:
            steps.append(line)
    
    return steps[:5] if steps else ["Review knowledge base", "Verify user identity", "Check device status"]


def check_escalation(output: str) -> bool:
    """Check if escalation is recommended."""
    escalation_keywords = ["escalate", "escalation", "assign to", "contact", "critical", "urgent"]
    return any(kw in output.lower() for kw in escalation_keywords)


def extract_escalation_group(output: str) -> Optional[str]:
    """Extract escalation group if applicable."""
    groups = {
        "Identity Access Management": ["identity", "password", "account", "mfa"],
        "Network Support": ["vpn", "network", "connectivity", "dns"],
        "Messaging Support": ["outlook", "email", "webmail"],
        "Endpoint Support": ["endpoint", "device", "laptop", "performance"],
        "Workplace IT": ["printer", "peripheral", "workspace"]
    }
    
    output_lower = output.lower()
    for group, keywords in groups.items():
        if any(kw in output_lower for kw in keywords):
            return group
    
    return None


def extract_safety_notes(output: str) -> list:
    """Extract safety recommendations from output."""
    safety_keywords = [
        "do not ask",
        "do not request",
        "do not provide",
        "never share",
        "verify identity",
        "escalate if",
        "critical"
    ]
    
    safety_notes = []
    lines = output.split("\n")
    
    for line in lines:
        if any(kw in line.lower() for kw in safety_keywords):
            safety_notes.append(line.strip())
    
    default_notes = [
        "Do not request passwords or MFA codes",
        "Verify user identity before escalation",
        "Document all troubleshooting steps"
    ]
    
    return safety_notes[:3] if safety_notes else default_notes


def determine_confidence(output: str) -> str:
    """Determine confidence level based on output quality."""
    high_confidence_indicators = ["verified", "confirmed", "clearly", "definitely", "high confidence"]
    medium_confidence_indicators = ["likely", "probable", "possibly", "may be"]
    
    output_lower = output.lower()
    
    if any(ind in output_lower for ind in high_confidence_indicators):
        return "HIGH"
    elif any(ind in output_lower for ind in medium_confidence_indicators):
        return "MEDIUM"
    else:
        return "LOW"


def format_json_response(parsed_output):
    """Convert parsed output to clean JSON string."""
    return json.dumps(parsed_output, indent=2)


def validate_output(parsed_output) -> bool:
    """Validate that all required fields are present."""
    required_fields = [
        "issue_type",
        "diagnosis_summary",
        "evidence_used",
        "recommended_steps",
        "escalation_required",
        "escalation_group",
        "safety_notes",
        "confidence"
    ]
    
    return all(field in parsed_output for field in required_fields)
