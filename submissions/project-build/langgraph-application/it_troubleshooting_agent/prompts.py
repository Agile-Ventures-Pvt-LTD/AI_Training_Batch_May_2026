CLASSIFIER_PROMPT = """
Classify the user query issue type into:
VPN
OUTLOOK_EMAIL
LAPTOP_PERFORMANCE
PASSWORD_RESET
NETWORK_CONNECTIVITY
PRINTER
UNKNOWN

Return JSON only:
{
 "issue_type": "",
 "confidence": "HIGH | MEDIUM | LOW",
 "requires_user_lookup": true,
 "requires_device_lookup": true,
 "requires_known_incident_check": true,
 "requires_clarification": false,
 "reasoning_summary": ""
}
"""

SYSTEM_PROMPT = """
You are an IT troubleshooting support assistant. Your goal is to help a user
resolve their workstation or network issue safely and efficiently.

- Ask for clarification only if the issue is unclear.
- Never expose raw SQL or database internals.
- Use knowledge base guidance and system diagnostics.
- Do not provide passwords or any sensitive authentication secrets.
- If the problem needs escalation, identify the correct team or next action.
"""

DEFAULT_SAMPLES = [
    "Amit says VPN times out after MFA approval. What should we check and what is the next action?",
    "Priya's laptop is very slow after startup. Diagnose the likely issue.",
    "David cannot login and password reset email is not received. What should be done?",
    "Sara's VPN disconnects frequently. What is the likely reason?",
    "Outlook is not syncing for Emily but webmail works. What is the next step?",
    "Which active known incidents may affect VPN users?",
    "Create a ticket summary for Rahul's laptop performance issue.",
    "My email is slow. Fix it.",
]

EVALUATION_SAMPLE_RUNS = [
    ("Amit says VPN times out after MFA approval. What should we check and what is the next action?", "USR-1001"),
    ("Priya's laptop is very slow after startup. Diagnose the likely issue.", "USR-1002"),
    ("David cannot login and password reset email is not received. What should be done?", "USR-1003"),
    ("Sara's VPN disconnects frequently. What is the likely reason?", "USR-1004"),
    ("Outlook is not syncing for Emily but webmail works. What is the next step?", "USR-1005"),
    ("Which active known incidents may affect VPN users?", None),
    ("Create a ticket summary for Rahul's laptop performance issue.", "USR-1006"),
    ("My email is slow. Fix it.", None),
]

QUERY_PROMPT = "Enter user query: "
EVALUATION_FILENAME = "evaluation_results.json"
