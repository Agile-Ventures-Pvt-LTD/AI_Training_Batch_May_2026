# P2-001 – NovaHR Assist

## Purpose

NovaHR Assist is an HR Employee Assistance chatbot developed using Microsoft Copilot Studio. The chatbot provides employees with HR policy guidance by grounding responses in approved organizational knowledge sources and includes guided workflows for common HR scenarios.

This project was developed as part of the Phase 2 Project Builds.

---

## Key instructions implemented

- HR policy question answering using Retrieval-Augmented Generation (RAG)
- Knowledge source as sole source of truth
- Leave Request Advisor Topic
- Workplace Concern & Escalation guidance
- Safe handling of out-of-scope requests
- Prompt injection resistance through agent instructions

---

## Knowledge Sources Used

The chatbot is configured with the following knowledge sources:

1. NovaWorks HR Policy Addendum v1.0
2. IIMA HR Policy Manual 2023
3. University of Rochester HR Policies

Knowledge precedence:

1. NovaWorks Addendum
2. IIMA HR Manual
3. University of Rochester HR Website

---

## Custom Topics Created

### Leave Request Advisor

Guides employees through leave-related queries by collecting required information and providing policy guidance without approving leave.

### Workplace Concern & Escalation

Provides confidential guidance for workplace concerns and routes employees to the appropriate reporting process while avoiding investigative actions.

---

## Technologies Used

- Microsoft Copilot Studio
- Generative AI
- Retrieval-Augmented Generation (RAG)
- Microsoft Knowledge Sources

---

## Project Structure

```
p2-001-nova-hr-assist
├── AI_USAGE_DECLARATION.md
├── Evaluate NovaHR Assist - Subhranshu Tests 260724_1507.csv
├── README.md
├── SCREENSHOTS.md
├── TEST_REPORT.md
├── agent overview.png
├── conditional (1).png
├── conditional (2).png
├── instructions (1).png
├── instructions (2).png
├── instructions (3).png
├── instructions (4).png
├── instructions (5).png
├── instructions (6).png
├── instructions (7).png
├── instructions (8).png
├── instructions (9).png
├── knowledge sources.png
├── knowledge-based answer.png
├── publish.png
├── sharing.png
└── topics.png
```

---

## Known limitations

- Edge case handling weak
- All Test cases not passed

---

## Author

Subhranshu Pattnayak