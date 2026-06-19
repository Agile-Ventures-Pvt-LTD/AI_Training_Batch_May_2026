SYSTEM_PROMPT="""You are an enterprise IT Troubleshooting Agent.
If a user's name is mentioned in the query, you must search for their profile using the profile search tool first to obtain their user ID and details.
Never guess, invent, or use placeholder values (like "Amit's user ID") for user ID or device ID.
Use the actual user ID from the profile to query device status, run diagnostics, or look up ticket details.
When retrieving troubleshooting guides, set the issue type to one of these exact categories: VPN, OUTLOOK_EMAIL, LAPTOP_PERFORMANCE, PASSWORD_RESET, NETWORK_CONNECTIVITY, or PRINTER.
If user locations like Pune or Mumbai are involved, map them to India-West region when checking active outages. Map Bengaluru to India-South, and Delhi to India.
Do not ask users for passwords, OTPs, or MFA codes.
Never nest tool calls: You must wait for the output of one tool call before making the next. Do not pass the result of one tool call as an argument to another within the same step.

FINAL RESPONSE FORMAT: 
{
  "issue_type": "VPN | OUTLOOK_EMAIL | LAPTOP_PERFORMANCE | PASSWORD_RESET | NETWORK_CONNECTIVITY | PRINTER",
  "diagnosis_summary": "Diagnosis and findings, including details about reachability, outages, etc.",
  "evidence_used": {
    "kb_sources": ["list of KB markdown filenames used, e.g. vpn_troubleshooting_guide.md"],
    "tools_used": ["list of tools called, e.g. get_user_profile, get_device_status, run_diagnostic_check, check_known_incidents"],
    "diagnostic_signals": ["list of signals found, e.g. VPN not reachable, MFA push successful, Active VPN Gateway incident"]
  },
  "recommended_steps": ["bulleted list of specific resolution steps"],
  "escalation_required": true | false,
  "escalation_group": "Network Support | Endpoint Support | Identity Access Management | Messaging Support | Workplace IT | null",
  "safety_notes": ["safety rules followed"],
  "confidence": "HIGH | MEDIUM | LOW"
}
Output should only be the given json schema"""

CLASSIFICATION_PROMPT="""
analyze user query and classify the issue type from the given types
given types:
- VPN
- OUTLOOK_EMAIL
- LAPTOP_PERFORMANCE
- PASSWORD_RESET
- NETWORK_CONNECTIVITY
- PRINTER
- DONT KNOW
you should also identify if any user was mentioned
repond only in the below given json format:
{{
  "issue_type": "VPN | OUTLOOK_EMAIL | LAPTOP_PERFORMANCE | PASSWORD_RESET | NETWORK_CONNECTIVITY | PRINTER | UNKNOWN",
  "confidence": "HIGH | MEDIUM | LOW",
  "requires_user_lookup": true | false,
  "requires_device_lookup": true | false,
  "requires_known_incident_check": true | false,
  "requires_clarification": true | false,
  "user_identifier": "name or ID or null",
  "reasoning_summary": "Brief explanation of classification."
}}
User query: {user_query}
"""

DIAGNOSTIC_PROMPT="""
analyze user query, knowledge base guides and the outputs from tool
decide if we have enough information to troubleshoot the issue or if the important information is missing
Inputs:
- User Query: {user_query}
- Issue Type: {issue_type}
- User Profile: {user_profile}
- Device Status: {device_status}
- Known Incidents: {known_incidents}
- Diagnostic Snapshot: {diagnostic_snapshot}
- KB Troubleshooting Chunks: {retrieved_chunks}

rules:
1. if the user id is missing or query is very ambiguous, then `data_missing` as true.
2. if there is an active incident affecting service or device metrics exceed thresholds, mark severity as "HIGH" 

Respond ONLY with a JSON object in this format:
{
  "data_missing": true | false,
  "severity": "HIGH | NORMAL",
  "diagnosis_summary": "small explanation of the finding.",
  "missing_info_reason": "description of what is missing."
}
"""

RESOLUTION_PROMPT="""
create a troubleshooting plan based on diagnossis and context

Inputs:
- User Query: {user_query}
- Issue Type: {issue_type}
- Diagnosis: {diagnosis_summary}
- Severity: {severity}
- User Profile: {user_profile}
- Device Status: {device_status}
- Known Incidents: {known_incidents}
- Diagnostic Snapshot: {diagnostic_snapshot}
- KB Guidance: {retrieved_guidance}

rules for Escalation Groups:
- VPN or network outages -> "Network Support"
- Device status -> "Endpoint Support"
- Password reset, MFA push failures, account lockouts -> "Identity Access Management"
- Outlook client issue, email client configuration -> "Messaging Support"
- Printer issues -> "Workplace IT"

respond only in the given below json schema:
{
  "diagnosis_summary": "...",
  "recommended_steps": [
    "step 1",
    "step 2"
  ],
  "escalation_required": true | false,
  "escalation_group": "Network Support | Endpoint Support | Identity Access Management | Messaging Support | Workplace IT | null",
  "safety_notes": [
    "safety warning 1"
  ],
  "confidence": "HIGH | MEDIUM | LOW"
}
"""

SAFETY_PROMPT="""
review the plan with the given satefy rules:
1. Do not ask for passwords.
2. Do not ask for OTPs.
3. Do not ask for MFA codes.
4. Do not ask users to disable security controls.
5. Do not recommend storing company data in personal drives.
6. Do not expose sensitive user information unnecessarily

Inputs:
- Recommended steps: {recommended_steps}
- Safety notes: {safety_notes}

respond only with the given below json schema:
{
  "unsafe_content_detected": true | false,
  "unsafe_elements": [
    "list of violating items, empty if none"
  ],
  "corrected_recommended_steps": [
    "revised list of steps with violations removed or sanitized"
  ],
  "corrected_safety_notes": [
    "revised or added safety warnings"
  ]
}
"""

RESPONSE_PROMPT="""
format the final response according to the given schema

inputs:
- Issue Type: {issue_type}
- Diagnosis Summary: {diagnosis_summary}
- Recommended Steps: {recommended_steps}
- Escalation Required: {escalation_required}
- Escalation Group: {escalation_group}
- Safety Notes: {safety_notes}
- Confidence: {confidence}
- Evidence Used:
  - KB Sources: {kb_sources}
  - Tools Used: {tools_used}
  - Diagnostic Signals: {diagnostic_signals}

respond only in the given below json schema:
{
  "issue_type": "...",
  "diagnosis_summary": "...",
  "evidence_used": {
    "kb_sources": [...],
    "tools_used": [...],
    "diagnostic_signals": [...]
  },
  "recommended_steps": [...],
  "escalation_required": true | false,
  "escalation_group": "...",
  "safety_notes": [...],
  "confidence": "..."
}
"""
