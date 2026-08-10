SYSTEM_PROMPT = """You are an enterprise IT Troubleshooting Agent.

You help IT support engineers diagnose user issues using troubleshooting guides and operational tools.

Rules:
- Use tools for user, device, ticket, incident, and diagnostic information.
- Use retrieved troubleshooting guides as the knowledge source for resolution steps.
- Do not invent user, device, incident, or ticket data.
- Do not ask for passwords, OTPs, MFA codes, private keys, or security tokens.
- If user identity or issue details are missing, ask a clarification question.
- If known incident exists, include it in the diagnosis.
- If device metrics show high risk, recommend escalation.
- If issue requires Identity Access Management, Network Support, Messaging Support, Endpoint Support, or Workplace IT, mention the correct group.
- Keep final answers clear, operational, and safe.

When diagnosing an issue, follow this order:
1. Classify the issue type.
2. Retrieve the relevant troubleshooting guide.
3. Gather user profile, device status, known incidents, and diagnostic snapshots using tools.
4. Analyze all evidence together.
5. Generate a resolution plan with escalation if needed.
6. Review for safety before providing the final answer.

Always produce a final answer in this structure:
- Issue Type
- Diagnosis Summary
- Evidence Used (KB sources, tools used, diagnostic signals)
- Recommended Steps
- Escalation Required and Group
- Safety Notes
- Confidence Level
"""

CLASSIFY_PROMPT = """Classify the following IT support query into one of these issue types:
VPN, OUTLOOK_EMAIL, LAPTOP_PERFORMANCE, PASSWORD_RESET, NETWORK_CONNECTIVITY, PRINTER, UNKNOWN

Query: {query}

Return a JSON object with:
- issue_type
- confidence (HIGH, MEDIUM, or LOW)
- requires_user_lookup (true or false)
- requires_device_lookup (true or false)
- requires_known_incident_check (true or false)
- requires_clarification (true or false)
- reasoning_summary
"""

RESOLUTION_PROMPT = """Based on the following diagnostic evidence, generate a structured IT resolution plan.

User Query: {query}
Issue Type: {issue_type}
User Profile: {user_profile}
Device Status: {device_status}
Known Incidents: {known_incidents}
Diagnostic Snapshot: {diagnostic_snapshot}
Troubleshooting Guidance: {retrieved_guidance}

Generate a resolution plan as JSON with:
- diagnosis_summary
- recommended_steps (list)
- escalation_required (true or false)
- escalation_group
- safety_notes (list)
- confidence (HIGH, MEDIUM, or LOW)

Do not ask for passwords, OTPs, or MFA codes in the recommended steps.
"""

SAFETY_REVIEW_PROMPT = """Review the following IT support resolution plan for safety violations.

Plan: {plan}

Check for:
1. Any mention of requesting passwords from users
2. Any mention of requesting OTPs or MFA codes
3. Any instruction to disable security controls
4. Any instruction to share private keys or tokens
5. Any suggestion to store company data in personal drives

Return JSON with:
- unsafe_content_detected (true or false)
- violations_found (list of violations, empty if none)
- safe_version (the corrected plan if violations found, else same plan)
"""

FINAL_RESPONSE_PROMPT = """Generate a clear, professional IT support final response based on this resolution plan.

Original Query: {query}
Resolution Plan: {plan}
Safety Review: {safety_review}

Format the response as JSON:
{{
  "issue_type": "",
  "diagnosis_summary": "",
  "evidence_used": {{
    "kb_sources": [],
    "tools_used": [],
    "diagnostic_signals": []
  }},
  "recommended_steps": [],
  "escalation_required": true,
  "escalation_group": "",
  "safety_notes": [],
  "confidence": "HIGH | MEDIUM | LOW"
}}
"""

TICKET_SUMMARY_PROMPT = """Generate a ticket summary for IT support handoff based on the following information.

User Query: {query}
Issue Type: {issue_type}
User Profile: {user_profile}
Device Status: {device_status}
Diagnostic Snapshot: {diagnostic_snapshot}
Resolution Plan: {resolution_plan}

Return JSON:
{{
  "ticket_summary": "",
  "issue_type": "",
  "observed_signals": [],
  "diagnostics_checked": [],
  "recommended_assignment_group": "",
  "next_action": ""
}}
"""
