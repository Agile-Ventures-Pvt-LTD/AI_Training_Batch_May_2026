# Project Build 02 - HR Employee Assistance RAG Chatbot

## Project Title
**HR Employee Assistance RAG Chatbot**

---

## Project Overview

This chatbot will act as a self-service HR assistant for employees of a fictional company called NovaWorks Technologies Pvt. Ltd. Employees should be able to ask questions about:

- Leave and attendance
- Working hours
- Remote-working policies
- Employee benefits
- Code of conduct
- Performance management
- Grievances and workplace concerns
- Onboarding and separation
- HR contact and escalation procedures

The solution must use retrieval-augmented generation through Copilot Studio knowledge sources. It must also use custom topics for scenarios that require structured questioning, variables, validation, conditional branching, confirmation, escalation, or routing.

Copilot Studio supports documents and websites as knowledge sources, agent-level instructions, topic-level generative-answer sources, and authored topics with triggers, variables, questions, and conditions.

---

## Project Objective

Build an HR chatbot that demonstrates proficiency in:

- Writing effective agent instructions
- Configuring documents as knowledge sources
- Configuring a public website or URL as a knowledge source
- Generating grounded answers from HR documents
- Handling conflicting information across knowledge sources
- Creating custom topics with trigger phrases
- Capturing and using variables
- Applying conditional logic
- Validating user input
- Handling sensitive HR scenarios
- Testing conversational and RAG behaviour
- Publishing and sharing the chatbot

---

## ChatBot URL

[**NovaWorks HR Assistant**](https://copilotstudio.microsoft.com/environments/Default-1e1572ff-a54c-4cd7-b2a9-20091afa5359/bots/6df58da0-1a87-f111-8076-000d3af21e08/overview) The url of the HR Assistant.

---

## Solution Summary

### Purpose

**NovaHR Assist** is an AI-powered HR Employee Assistance chatbot developed using Microsoft Copilot Studio for NovaWorks Technologies Pvt. Ltd. It provides employees with accurate, policy-based HR guidance through Retrieval-Augmented Generation (RAG) using configured knowledge sources. The chatbot also supports structured HR workflows through custom topics, enabling employees to receive guidance on leave requests, workplace concerns, and employment verification requests while ensuring privacy, safety, and compliance with company policies

### Knowledge Sources Used

#### 1. NovaWorks HR Policy Addendum v1.0 (Primary Knowledge Source)
- Official company HR policy document.
- Highest-priority knowledge source.
- Used for company-specific policies related to working hours, leave, remote work, bereavement leave, workplace conduct, and HR support.
- Overrides conflicting information from other knowledge sources.

#### 2. Primary HR Policy Manual (Secondary Knowledge Source)
- Comprehensive HR handbook containing general HR policies and best practices.
- Used when information is not available in the NovaWorks HR Policy Addendum.
- Provides guidance on employee benefits, attendance, leave, performance management, onboarding, and workplace conduct.

#### 3. University of Rochester Human Resources Policies (Website Knowledge Source)
- Public HR website configured as a URL knowledge source.
- Used only when relevant information is unavailable in the higher-priority knowledge sources.
- Demonstrates URL-based Retrieval-Augmented Generation capabilities.

### Custom Topics Created

#### 1. Leave Request Advisor
- Collects leave request information through a conversational AI workflow.
- Determines the applicable leave category.
- Applies NovaWorks leave policy rules.
- Validates advance notice and medical certificate requirements.
- Generates a leave request summary for confirmation.
- Does not approve leave requests.

#### 2. Workplace Concern and Escalation
- Handles harassment, bullying, discrimination, retaliation, workplace conflicts, and safety concerns.
- Prioritises employee safety.
- Provides empathetic responses.
- Supports confidential reporting.
- Directs employees to authorised HR representatives or the Internal Committee.
- Does not investigate complaints or determine outcomes.

#### 3. Employment Verification Request (Optional Advanced Topic)
- Collects employment verification request details.
- Generates a request summary for user confirmation.
- Guides employees to the official HR process.
- Does not generate or authorise employment verification letters.

### Key Instructions Implemented

- Defined a professional HR assistant identity with clear scope and responsibilities.
- Restricted responses to HR-related topics only.
- Configured Retrieval-Augmented Generation using approved knowledge sources.
- Implemented knowledge-source precedence:
    - NovaWorks HR Policy Addendum
    - Primary HR Policy Manual
    - Public HR Website
- Prevented hallucinated or unsupported HR responses.
- Required source-grounded policy guidance.
- Protected employee privacy by refusing requests for confidential or personal information.
- Prevented disclosure of hidden prompts and internal instructions.
- Redirected employee-specific requests (leave balance, salary, attendance, etc.) to HR systems.
- Applied professional, respectful, and empathetic communication.
- Implemented prompt injection protection.
- Included confidential escalation guidance for sensitive workplace concerns.
- Ensured the chatbot provides policy guidance only and does not make HR decisions or approvals.

### Known Limitations

- The chatbot provides general HR policy guidance only and cannot approve leave, remote work, benefits, or other HR requests.
- Personal employee information such as leave balances, salary details, attendance records, and performance data cannot be accessed.
- The chatbot cannot investigate workplace complaints or determine whether misconduct has occurred.