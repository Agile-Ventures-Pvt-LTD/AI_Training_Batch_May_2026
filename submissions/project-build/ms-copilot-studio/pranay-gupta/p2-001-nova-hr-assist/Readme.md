# NovaHR Assist – HR Employee Assistance Chatbot

## Project Overview

**Chatbot Name:** NovaHR Assist

NovaHR Assist is an AI-powered HR Employee Assistance chatbot developed using Microsoft Copilot Studio. It provides employees with accurate, policy-based guidance by retrieving information from approved organizational knowledge sources using Retrieval-Augmented Generation (RAG). The chatbot assists employees with HR-related queries while ensuring responses remain grounded in official company policies.

---

## Purpose

The primary objective of NovaHR Assist is to:

* Provide quick and reliable answers to HR policy-related questions.
* Help employees understand leave policies, workplace guidelines, and HR procedures.
* Support employees in identifying the appropriate HR processes without making HR decisions or approvals.
* Deliver consistent responses based on approved organizational knowledge sources.

---

## Knowledge Sources Used

The chatbot retrieves information from the following knowledge sources:

* NovaWorks HR Policy Addendum
* Great Lakes Employee Handbook (PDF)
* Official HR Policy Website

The chatbot follows a predefined source priority to ensure responses are based on the most authoritative policy available.

---

## Custom Topics Created

### 1. Leave Request Advisor

Provides guidance on different leave types, collects relevant information, evaluates policy conditions, and recommends the appropriate next steps without approving leave requests.

### 2. Workplace Concern & Escalation

Assists employees in reporting workplace concerns by classifying the issue, providing empathetic guidance, and recommending the appropriate HR grievance or escalation process.

---

## Key Instructions Implemented

* Respond only using the configured HR knowledge sources.
* Follow the defined knowledge source priority when multiple sources are available.
* Maintain a professional, respectful, and empathetic tone.
* Do not generate information that is not available in the knowledge base.
* Do not approve leave requests or make HR decisions.
* Protect confidential employee information.
* Recommend contacting HR when policy information is unavailable or employee-specific information is required.
* Provide policy-based guidance for workplace concerns and HR procedures.

---

## Known Limitations

* The chatbot cannot access employee-specific records such as leave balances, payroll, or personal HR information.
* It cannot approve leave requests or perform HR transactions.
* Responses are limited to the configured knowledge sources.
* Questions outside the HR domain are not supported.
* Final HR decisions remain with the Human Resources department and the employee's reporting manager.

## Chatbot Link

[NovaHR Assist URL](https://copilotstudio.microsoft.com/environments/Default-1e1572ff-a54c-4cd7-b2a9-20091afa5359/bots/30f98300-1d87-f111-8076-000d3af21e08/overview)