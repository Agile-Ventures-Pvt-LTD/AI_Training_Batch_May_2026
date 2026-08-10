# NovaHR Assist

## Overview

**NovaHR Assist** is a self-service HR assistant built for **NovaWorks Technologies Pvt. Ltd.** using Microsoft Copilot Studio.

The idea behind the assistant is simple: employees should be able to find answers to common HR questions without having to go through lengthy policy documents every time.

Employees can ask about leave, attendance, working hours, remote work, benefits, workplace concerns, onboarding, separation, and other supported HR topics.

NovaHR Assist only provides policy guidance. Any final decision, approval, investigation, or employee-specific matter remains with the authorised HR team.

---

## Knowledge Sources

The assistant uses only the approved NovaWorks HR knowledge sources:
```
1. **NovaWorks_HR_Policy_Addendum_v1.0**
2. **HR Policy Manual (2023)**
3. **Public HR Policy Website**
```

These sources follow a fixed priority order. If two sources contain conflicting information, the higher-priority source is followed instead of mixing the information from both.

---

## Custom Topics

### Leave Request Advisor

This topic helps employees with leave-related questions.

It can explain the relevant leave policy and guide employees on what they should do next. However, it does not approve, reject, or submit leave requests, and it does not decide whether a particular employee is eligible.

### Workplace Concern and Escalation

This topic is designed for sensitive workplace concerns such as:

- Harassment
- Bullying
- Discrimination
- Retaliation
- Workplace safety concerns

The assistant responds in a respectful and neutral way without investigating the situation or deciding who is at fault.

When needed, the employee is guided to the appropriate **HR representative or Internal Committee** for further support.

---

## How NovaHR Assist Responds

The assistant follows a set of instructions to keep its responses accurate, safe, and consistent.

It:

- Answers only NovaWorks HR-related questions.
- Uses approved HR sources instead of guessing.
- Follows the correct source priority when policies conflict.
- Keeps responses clear, professional, respectful, and concise.
- Mentions the supporting source whenever possible.
- Protects personal and confidential information.
- Refers matters requiring human judgement to authorised HR.
- Does not make employee-specific decisions or approvals.
- Politely refuses questions outside its HR scope.
- Refuses attempts to reveal hidden prompts, instructions, configurations, or other internal information.

If an answer cannot be verified from the available HR sources, the assistant does not make one up. Instead, it asks the employee to contact the authorised HR team.

---

## Privacy and Sensitive Information

NovaHR Assist is designed to avoid collecting unnecessary personal or confidential information.

Employees should not be asked to provide information such as Aadhaar numbers, passwords, banking details, medical reports, or unnecessary details about sensitive incidents.

The assistant also does not disclose confidential information belonging to another employee.

Sensitive workplace concerns are handled carefully and are redirected to the appropriate authorised channel when human involvement is required.

---

## Example Questions

Employees can ask questions such as:

- What are the standard working hours at NovaWorks?
- How many types of leave are available?
- What is the standard working week?
- Can employees work remotely during probation?
- How can I report harassment or discrimination confidentially?
- What should I do if I have a workplace concern?

---

## Known Limitations

NovaHR Assist is meant to provide **HR policy guidance**, not replace the HR team.

It cannot:

- Approve or reject HR requests.
- Submit or process requests on behalf of employees.
- Make decisions about individual employee eligibility.
- Access private employee records unless connected to an authorised system.
- Investigate workplace complaints or determine fault.
- Make disciplinary, legal, or policy-exception decisions.
- Answer questions when the required information is not available in the approved sources.

Cases requiring personal records, investigation, approval, or human judgement are referred to the authorised HR team.

---

## Technology Used

- **Microsoft Copilot Studio**
- Approved HR knowledge sources
- Custom topics
- Agent instructions and guardrails
- Source precedence and grounding
- Suggested prompts
- Escalation and sensitive-information handling

---

## Summary

| Item | Details |
|---|---|
| **Chatbot Name** | NovaHR Assist |
| **Organisation** | NovaWorks Technologies Pvt. Ltd. |
| **Platform** | Microsoft Copilot Studio |
| **Purpose** | Help employees find reliable HR policy information |
| **Custom Topics** | Leave Request Advisor, Workplace Concern and Escalation |
| **Knowledge** | Approved NovaWorks HR sources |
| **Final Decisions** | Authorised HR personnel and managers |

---

## Note

NovaHR Assist makes HR information easier to access, but it does not replace the HR team.

Whenever a question requires employee-specific information, approval, investigation, or human judgement, the employee is guided to the appropriate authorised HR channel.