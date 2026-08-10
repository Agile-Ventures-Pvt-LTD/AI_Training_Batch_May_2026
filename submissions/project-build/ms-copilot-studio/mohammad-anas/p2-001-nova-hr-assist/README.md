# P2-001: NovaHR Assist — Solution Summary & Submission

### Chatbot Shared with Ankur Sir


## Solution Summary

### Chatbot Name
**NovaHR Assist**

### Purpose
NovaHR Assist is an official self-service HR Employee Assistance RAG Chatbot built in Microsoft Copilot Studio. Its primary purpose is to reduce the administrative burden on the HR department by answering routine, repetitive policy questions through grounded Retrieval-Augmented Generation (RAG) and handling multi-step, deterministic employee inquiries via structured custom topics. 

**Core Operational Boundaries:**
* The chatbot provides **general policy guidance only**.
* It explicitly **lacks the authority** to approve leave, remote work, benefits, grievances, or any employee-specific requests.
* All final approvals and formal transactions remain strictly with the employee's manager and the HR department via the official HR portal.
* Live human HR support is available **Monday to Friday, 9:30 AM to 6:00 PM IST**.

### Knowledge Sources Used
The chatbot utilizes a tiered, priority-based RAG architecture to prevent hallucinations and resolve policy conflicts:
1. **Priority 1 (Supreme Authority): `NovaWorks_HR_Policy_Addendum_v1.0.pdf`**
   * Enforces company-specific rules effective July 1, 2026: 12 Casual Leave days, 10 Sick Leave days (medical certificate mandatory for >2 consecutive days), 18 Earned Leave days (5 days' notice required for >3 days), 2 days/week Remote Work (restricted during probation), 3 days Bereavement Leave, and standard working hours (9:30 AM – 6:30 PM IST with 10:00 AM – 4:00 PM core hours).
2. **Priority 2 (Primary Reference): `IIMA Human Resources Policy Manual 2023.pdf`**
   * Serves as the baseline manual for general administrative, behavioral, and procedural workflows not covered in the NovaWorks Addendum.
3. **Priority 3 (Supplementary Reference): `https://www.rochester.edu/human-resources/policies/`**
   * Configured public web URL utilized solely for general HR definitions and concepts if unaddressed by Priority 1 and 2 documents.

### Custom Topics Created
1. **Leave Request Advisor (Mandatory Topic 1)**
   * **Workflow:** Guides employees through leave categorization, validates request parameters against NovaWorks policy limits, and evaluates compliance.
   * **Key Logic:** Identifies that Remote Work is not leave and routes out of the calculation flow; checks Casual Leave duration (capped at 3 days) and notice periods (prompts for emergency exception if <2 days' notice); evaluates Sick Leave duration and enforces medical certificate requirements for >2 days; enforces 5-day advance notice for Earned Leave >3 days.
   * **Output:** Generates a structured summary card and requires user confirmation before closing with a mandatory disclaimer.
2. **Workplace Concern and Escalation (Mandatory Topic 2)**
   * **Workflow:** Empathetically handles workplace harassment, bullying, discrimination, and grievance reporting with strict privacy guardrails.
   * **Key Logic:** Implements an immediate safety check (`ImmediateDanger = true`) that halts routine HR questioning and provides emergency instructions (dial 112 / campus security); enforces a strict privacy guardrail advising users *not* to input sensitive personal data or descriptions of traumatic events; offers an anonymous reporting pathway; routes serious misconduct directly to the Internal Committee (IC/CMGI) without investigating or judging claims.

### Key Instructions Implemented
* **Zero Hallucination Directive:** Strict prompt enforcement prohibiting the language model from inventing or assuming policy values. If data is missing from configured sources, the bot issues a standardized fallback response directing the user to HR support during working hours.
* **Source Attribution:** Mandatory instruction to cite or mention the specific knowledge document utilized when generating policy answers.
* **Confidentiality & Data Protection:** Proactive restriction against requesting or storing passwords, bank details, Aadhaar numbers, or detailed evidence files.
* **Security & Scope Enforcement:** Prompt injection defense (refusing instructions to ignore system rules or reveal prompts) and out-of-scope refusal (declining coding requests, general trivia, or legal/medical advice).

### Participant 
Mohammad Anas
