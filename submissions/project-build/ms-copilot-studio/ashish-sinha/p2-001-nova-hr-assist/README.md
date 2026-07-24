# P2-001 | HR Employee Assistance RAG Chatbot

# NovaHR Assist

An AI-powered HR Employee Assistance chatbot developed using **Microsoft Copilot Studio**. NovaHR Assist provides employees with quick, consistent, and policy-compliant answers to HR-related questions by leveraging Retrieval-Augmented Generation (RAG) from organization-specific knowledge sources.

---

# Project Information

| Field | Details |![alt text](image.png)
|--------|---------|
| **Project ID** | P2-001 |
| **Participant Name** | Ashish Sinha |
| **Chatbot Name** | Ashish_NovaHR_Assist |
| **Platform** | Microsoft Copilot Studio |
| **Copilot Studio URL** | https://copilotstudio.preview.microsoft.com/environments/Default-1e1572ff-a54c-4cd7-b2a9-20091afa5359/bots/652c3540-1b87-f111-8076-000d3af21e08/overview |
| **Primary HR Document** | NovaWorks HR Policy Addendum.pdf |
| **URL Knowledge Source** |https://www.rochester.edu/human-resources/hr-policies/ |
| **Custom Topics Completed** | 1. Leave Request Advisor <br> 2. Workplace Concern and Escalation <br> 3. Immediate Safety Assistance |
| **Number of Test Cases Executed** | 15 |
| **Known Limitations** | No HRMS integration, cannot access employee-specific information, cannot approve leave requests, responses limited to configured knowledge sources |
| **AI Tools Used** | Microsoft Copilot Studio, ChatGPT (documentation, topic planning, testing support) |

---

# Project Deliverables

This repository contains all required deliverables for the **P2-001 HR Employee Assistance RAG Chatbot** project.

- README.md
- test_report.md
- screenshot.md
- ai_usage_declaration.md

---

# Project Overview

NovaHR Assist is an AI-powered HR chatbot that enables employees to quickly obtain HR policy information without contacting the HR team for routine queries.

The chatbot uses **Retrieval-Augmented Generation (RAG)** to retrieve information from approved HR knowledge sources while ensuring responses remain accurate, policy-compliant, and within the HR domain.

The chatbot also includes custom conversational topics for common HR scenarios such as leave requests, workplace concerns, and emergency assistance.

---

# Project Objectives

- Provide instant answers to HR policy questions.
- Improve employee self-service.
- Reduce repetitive HR support requests.
- Deliver policy-compliant responses using approved knowledge sources.
- Guide employees through leave request scenarios.
- Handle workplace concerns confidentially.
- Follow Responsible AI principles.

---

# Features

## Knowledge Retrieval

The chatbot retrieves HR information including:

- Working hours
- Casual leave
- Sick leave
- Earned leave
- Remote work policy
- Bereavement leave
- Leave policy
- HR procedures

---

## Custom Topics

### Leave Request Advisor

Guides employees through leave-related queries by collecting:

- Leave type
- Leave duration
- Start date
- Emergency status

The chatbot provides policy guidance only and never approves or rejects leave requests.

---

### Workplace Concern and Escalation

Supports employees reporting workplace issues by:

- Collecting concern details
- Respecting confidentiality
- Providing HR escalation guidance

---

### Immediate Safety Assistance

When an employee reports immediate physical danger, the chatbot:

- Prioritizes employee safety
- Advises contacting emergency services or workplace security
- Directs the employee to HR after the immediate risk is addressed

---

## Responsible AI Features

NovaHR Assist implements responsible AI practices by:

- Protecting confidential information
- Preventing prompt injection attacks
- Refusing out-of-scope requests
- Respecting employee privacy
- Avoiding unsupported or fabricated information
- Applying knowledge source precedence

---

# Technology Stack

| Component | Technology |
|-----------|------------|
| AI Platform | Microsoft Copilot Studio |
| Knowledge Retrieval | Retrieval-Augmented Generation (RAG) |
| Knowledge Sources | PDF Documents & Website |
| Topic Authoring | Copilot Studio Topics |
| NLP | Microsoft Copilot Studio |
| Testing | Manual Functional Testing |

---

# Solution Architecture

```text
                    Employee
                        │
                        ▼
          Microsoft Copilot Studio
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
 Knowledge Sources   Custom Topics   Safety Rules
        │
        ▼
  AI-Generated HR Response
```

---

# Knowledge Sources

NovaHR Assist uses three configured knowledge sources.

1. NovaWorks HR Policy Addendum
2. Primary HR Policy Manual
3. Public HR Handbook

---

# Knowledge Source Priority

When conflicting information exists, the chatbot follows the configured precedence:

1. NovaWorks HR Policy Addendum
2. Primary HR Policy Manual
3. Public HR Handbook

This ensures organization-specific policies always take precedence over public information.

---

# Conversation Flow

```text
Employee Query
        │
        ▼
Intent Recognition
        │
        ▼
Knowledge Source Search (RAG)
        │
        ▼
Custom Topic Trigger?
      │             │
     Yes            No
      │             │
      ▼             ▼
Topic Flow     Knowledge Response
      │             │
      └──────┬──────┘
             ▼
     Final HR Response
```

---

# PRD Compliance

This implementation satisfies the major requirements of the **P2-001 Project Requirements Document (PRD)**.

- Retrieval-Augmented Generation (RAG)
- Three Knowledge Sources
- Three Custom Topics
- Responsible AI implementation
- Prompt Injection Protection
- Privacy Protection
- Immediate Safety Handling
- Knowledge Source Precedence
- Functional Testing using 15 mandatory test cases
- Complete project documentation

---

# Testing

The chatbot was validated against the mandatory test cases defined in the **P2-001 Project Requirements Document (PRD)**.

Testing covered:

- Knowledge Retrieval
- Leave Request Advisor
- Workplace Concern
- Immediate Safety
- Conflicting Information
- Missing Information
- Prompt Injection
- Privacy Protection
- Out-of-Scope Requests
- Fallback Responses

A detailed testing report is available in:

```text
test_report.md
```

---

# Repository Structure

```text
NovaHR-Assist/
│
├── README.md
├── test_report.md
├── screenshot.md
├── ai_usage_declaration.md
```

---

# Assumptions

- The chatbot provides policy guidance only.
- Leave approval is outside the chatbot's scope.
- Personal employee records are unavailable.
- Responses are limited to configured knowledge sources.
- HR decisions remain the responsibility of authorized personnel.

---

# Known Limitations

- No HRMS integration
- No payroll integration
- No employee authentication
- Cannot access personal leave balance
- Cannot modify employee records
- Cannot approve leave requests
- Cannot answer questions outside the HR domain
- Dependent on the quality of configured knowledge sources

---

# Future Enhancements

- Microsoft Entra ID authentication
- HRMS integration
- Leave balance lookup
- Payroll integration
- Microsoft Teams deployment
- Adaptive Cards
- Live HR agent handoff
- Analytics dashboard
- Multilingual support
- Automatic knowledge synchronization

---

# Best Practices Implemented

- Responsible AI
- Policy-based responses
- Knowledge source prioritization
- Privacy protection
- Prompt injection prevention
- Secure fallback responses
- Confidential workplace escalation
- Immediate safety prioritization

---

# Test Coverage Summary

| Requirement | Status |
|------------|--------|
| Knowledge Retrieval | ✅ |
| Leave Request Advisor | ✅ |
| Workplace Concern | ✅ |
| Immediate Safety | ✅ |
| Conflicting Information | ✅ |
| Missing Information | ✅ |
| Prompt Injection | ✅ |
| Privacy Protection | ✅ |
| Out-of-Scope Requests | ✅ |
| Fallback Handling | ✅ |

---

# Author

**Participant Name:** Ashish Sinha

**Project ID:** P2-001

**Project:** HR Employee Assistance RAG Chatbot

**Platform:** Microsoft Copilot Studio
