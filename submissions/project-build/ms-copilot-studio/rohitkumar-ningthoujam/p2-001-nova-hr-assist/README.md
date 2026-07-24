
## Chatbot Name
NovaHR Assist


## Purpose
NovaHR Assist is an HR Employee Assistance chatbot built using Microsoft Copilot Studio.

The chatbot provides employees with:
- HR policy guidance
- Leave and attendance information
- Remote work policy information
- Workplace concern escalation support

The chatbot uses Retrieval-Augmented Generation (RAG) with configured knowledge sources and custom topics.

## Platform
Microsoft Copilot Studio

## Knowledge Sources

1. NovaWorks HR Policy Addendum v1.0
   - Company-specific HR rules
   - Highest priority source

2. Public HR Policy Handbook
   - General HR reference information

3. Public HR Website
   - Supplementary HR information

## Custom Topics Implemented

### 1. Leave Request Advisor
Purpose:
- Helps employees understand applicable leave policies.
- Collects leave type, duration, notice period and probation details.
- Provides policy guidance only.
- Does not approve leave.

### 2. Workplace Concern and Escalation
Purpose:
- Handles harassment, discrimination, bullying and grievance scenarios.
- Performs safety checks.
- Provides confidential HR escalation guidance.
- Does not investigate complaints.

## Agent Instructions Implemented

- Uses knowledge sources before answering.
- NovaWorks policy has highest priority.
- Avoids hallucinated HR information.
- Protects employee privacy.
- Handles sensitive workplace concerns safely.

## Known Limitations

- Does not approve employee requests.
- Does not access employee records.
- Does not investigate complaints.
- Provides general HR guidance only.
## agent URL:
```https://copilotstudio.microsoft.com/environments/Default-1e1572ff-a54c-4cd7-b2a9-20091afa5359/bots/af6f612c-1b87-f111-8076-000d3af21e08/overview
``