# P2-001 – NovaHR Assist

HR Employee Assistance RAG Chatbot built using **Microsoft Copilot Studio**

---

## Project Overview

NovaHR Assist is an HR support chatbot developed for the P2-001 project build using Microsoft Copilot Studio. The chatbot helps employees find answers to common HR questions by retrieving information from approved knowledge sources and guiding users through structured conversations for specific HR processes.

The objective of this project was to build a chatbot that provides accurate policy guidance while avoiding unsupported or fabricated responses. General HR questions are answered using Retrieval-Augmented Generation (RAG), whereas workflows such as leave requests and workplace concerns are handled through custom topics with guided questions and conditional logic.

The chatbot is designed for a fictional organization, **NovaWorks Technologies Pvt. Ltd.**

---

## Objectives

The chatbot was developed with the following goals:

- Reduce repetitive HR queries by providing self-service support.
- Answer HR questions using configured knowledge sources.
- Prevent unsupported responses by relying on document-based retrieval.
- Guide employees through common HR processes using structured conversations.
- Handle sensitive workplace concerns safely and direct employees to the appropriate HR channels.
- Demonstrate the use of Microsoft Copilot Studio features such as knowledge sources, topics, variables, and conditions.

---

## Features

NovaHR Assist can assist employees with questions related to:

- Working hours
- Leave policies
- Attendance
- Remote work
- Employee benefits
- Code of conduct
- Performance management
- Grievance procedures
- Onboarding
- Separation process
- HR support contacts

The chatbot only provides general HR policy guidance. It does not approve leave requests, modify employee information, or make HR decisions.

---

## Knowledge Sources

The chatbot uses three knowledge sources.

| Priority | Knowledge Source | Purpose |
|----------|------------------|---------|
| 1 | NovaWorks_HR_Policy_Addendum_v1.0 | Company-specific HR policies |
| 2 | IIMA Human Resources Policy Manual 2023  | Public HR reference |
| 3 | University of Rochester HR Policies  | Public HR website [https://www.rochester.edu/human-resources/hr-policies/] |

If multiple sources contain different information, the chatbot follows the priority listed above and does not combine conflicting policies.

---

## Custom Topics

### 1. Leave Request Advisor

This topic guides employees through a leave request by collecting the required information and checking it against the NovaWorks HR policy.

Information collected includes:

- Leave type
- Start date
- Number of working days
- Advance notice
- Emergency status
- Medical certificate requirement (where applicable)

The chatbot provides policy guidance only and reminds the employee that leave approval must be completed through the HR process.

---

### 2. Workplace Concern and Escalation

This topic is used for sensitive workplace issues such as harassment, bullying, discrimination, retaliation, or other grievances.

The conversation is designed to:

- Respond empathetically
- Avoid requesting unnecessary personal details
- Prioritize immediate safety where required
- Provide confidential HR escalation guidance
- Direct employees to the Internal Committee or an authorized HR representative

---

### 3. Employment Verification Request 

An additional topic was created to collect the information required for an employment verification request.

The chatbot collects:

- Employee name
- Employee ID
- Recipient organization
- Purpose
- Required date
- Salary inclusion preference

After collecting the information, it generates a request summary. It does not generate an official employment verification letter.

---

## Agent Configuration

The chatbot was configured with instructions to ensure consistent and safe responses.

Key behaviors include:

- Respond only to HR-related questions.
- Use configured knowledge sources instead of general AI knowledge.
- Follow the defined knowledge source precedence.
- Protect confidential employee information.
- Refuse out-of-scope requests.
- Resist prompt injection attempts.
- Direct employee-specific requests to HR.
- Handle workplace concerns using an empathetic and non-judgmental approach.
- Keep responses concise and easy to understand.

---

## Project Structure

```
p2-001-nova-hr-assist
│
├── README.md
├── TEST_REPORT.md
├── AI_USAGE_DECLARATION.md
├── screenshots.md
|---- assets

```

---

## Testing

The chatbot was tested using the scenarios provided in the project requirements.

The testing covered:

- Policy retrieval
- Leave policy validation
- Sick leave rules
- Remote work policy
- Knowledge source conflicts
- Employee privacy
- Prompt injection attempts
- Out-of-scope requests
- Workplace concern handling
- Immediate safety scenarios
- Topic cancellation
- Variable updates
- Fallback responses

A detailed record of all executed test cases is available in **test_report.md**.

---

## Known Limitations

The chatbot intentionally does not:

- Approve leave requests
- Access employee records
- View leave balances
- Modify HR information
- Retrieve payroll details
- Share confidential employee information
- Investigate workplace complaints
- Provide legal or medical advice
- Generate official employment verification letters

Requests requiring employee-specific information or approvals must be handled by the HR department.

---

## Technologies Used

- Microsoft Copilot Studio
- Retrieval-Augmented Generation (RAG)
- Microsoft Knowledge Sources
- Custom Topics
- Variables
- Conditional Branching

---

## How to Run

1. Open the published Copilot Studio chatbot.
2. Start a conversation using one of the suggested prompts or enter an HR-related question.
3. For structured requests such as leave applications or workplace concerns, follow the guided conversation.
4. Review the chatbot's recommendations and contact HR where approval or employee-specific action is required.

---

## Repository Contents

| File | Description |
|------|-------------|
| README.md | Project overview and implementation summary |
| test_report.md | Results of the required test cases |
| ai_usage_declaration.md | AI usage declaration for the project |
| screenshots.docx | Screenshots of the completed implementation |


---

# Chatbot Link:
```bash
https://copilotstudio.microsoft.com/environments/Default-1e1572ff-a54c-4cd7-b2a9-20091afa5359/bots/0ab12735-1787-f111-8076-000d3af21e08/overview
```
---

## Conclusion

This project demonstrates how Microsoft Copilot Studio can be used to build a practical HR support chatbot by combining knowledge-based responses with guided conversational workflows. The implementation focuses on accurate policy retrieval, user privacy, structured interactions, and safe handling of sensitive HR scenarios while remaining within the defined scope of the project.