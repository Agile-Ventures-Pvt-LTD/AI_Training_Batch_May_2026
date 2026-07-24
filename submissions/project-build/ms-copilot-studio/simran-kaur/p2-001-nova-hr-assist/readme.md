# P2-001 NovaHR Assist - HR Employee Assistance RAG Chatbot

## Participant Name
Simran Kaur

## Chatbot Name
NovaHR Assist

## Purpose

NovaHR Assist is an HR Employee Assistance chatbot built using Microsoft Copilot Studio.

The chatbot provides employees with policy-grounded HR guidance, structured workflows, and safe escalation support for workplace concerns.

The chatbot helps employees with:

- Leave and attendance queries
- Working hours and remote-work policies
- Employee benefits
- Workplace concerns and grievances
- HR escalation procedures

The chatbot provides general HR policy guidance only and does not make employee-specific decisions.

---

# Knowledge Sources Used

## 1. NovaWorks HR Policy Addendum v1.0

**Type:** Company-specific policy document

**Purpose:**
Provides NovaWorks-specific HR rules and policies.

**Priority:**
Highest priority source when conflicts occur.

---

## 2. Public HR Policy PDF

**Type:** External HR handbook / policy manual

**Purpose:**
Provides supplementary HR policy information.

---

## 3. Public HR Website

**Type:** URL Knowledge Source

**Purpose:**
Provides additional HR reference information.

---

# Custom Topics Created

## 1. Leave Request Advisor

Purpose:
Helps employees understand applicable leave policies.

Features implemented:

- Collects leave type
- Collects leave duration
- Checks probation status
- Checks advance notice
- Handles emergency cases
- Applies conditional policy rules
- Generates request summary
- Requests confirmation

Limitation:

The chatbot does not approve leave requests.

---

## 2. Workplace Concern Reporter

Purpose:
Handles sensitive workplace concerns safely and provides appropriate escalation guidance.

Features implemented:

- Empathetic acknowledgement
- Immediate safety check
- Harassment guidance
- Discrimination guidance
- Bullying guidance
- Safety issue handling
- Confidential HR escalation guidance
- Privacy protection

Limitation:

The chatbot does not investigate complaints or determine outcomes.

---

# Key Instructions Implemented

The chatbot follows these instructions:

- Use configured knowledge sources for HR answers.
- Prefer NovaWorks HR Policy Addendum over external sources.
- Avoid unsupported or hallucinated policy information.
- Provide source-grounded responses.
- Clearly explain limitations.
- Do not approve employee requests.
- Do not provide confidential employee information.
- Do not request sensitive personal information.
- Handle workplace concerns with empathy and safety-first escalation.

---

# Known Limitations

- Cannot access employee-specific HR records.
- Cannot check personal leave balances.
- Cannot approve leave or remote-work requests.
- Cannot investigate workplace complaints.
- Cannot replace HR representatives.
- Requires HR involvement for employee-specific decisions.