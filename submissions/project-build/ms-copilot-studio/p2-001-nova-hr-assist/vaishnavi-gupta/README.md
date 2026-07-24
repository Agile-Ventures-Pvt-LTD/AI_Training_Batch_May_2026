# HR Employee Assistance RAG Chatbot
### Microsoft Copilot Studio | Phase 2 Project Build (P2-001)

---

## Project Overview

The **HR Employee Assistance RAG Chatbot** is an AI-powered conversational assistant built using **Microsoft Copilot Studio**.

It acts as a self-service HR assistant for employees of **NovaWorks Technologies Pvt. Ltd.**, providing accurate, source-grounded responses to HR-related questions while ensuring privacy, safety, and compliance.

The chatbot combines:

- Retrieval-Augmented Generation (RAG)
- Microsoft Copilot Studio Knowledge Sources
- Custom Topics
- Conditional Branching
- Variables
- User Input Validation
- Secure Conversation Design

Unlike a traditional chatbot, this solution answers policy-related questions using uploaded company documents and structured workflows instead of relying solely on LLM knowledge.

---

# Project Objectives

The chatbot should enable employees to obtain HR policy information related to:

- Leave Policies
- Attendance
- Working Hours
- Remote Work
- Employee Benefits
- Performance Management
- Code of Conduct
- Workplace Grievances
- Onboarding
- Separation
- HR Contacts
- Escalation Procedures

The chatbot should:

✔ Answer policy questions using approved documents

✔ Guide users through structured HR workflows

✔ Prevent hallucinated answers

✔ Handle sensitive situations safely

✔ Respect employee privacy

✔ Escalate when necessary

---

# Technology Stack

- Microsoft Copilot Studio
- Generative AI
- Retrieval-Augmented Generation (RAG)
- Microsoft Knowledge Sources
- PDF Knowledge Base
- Website Knowledge Base
- Custom Topics
- Variables
- Conditional Logic
- Topic Branching
- Conversation Nodes

---

# High-Level Architecture

```
                    User
                      │
                      ▼
          Microsoft Copilot Studio
                      │
      ┌───────────────┼───────────────┐
      │               │               │
      ▼               ▼               ▼
Agent Instructions  Knowledge Base  Custom Topics
      │               │               │
      └───────────────┴───────────────┘
                      │
                      ▼
             RAG Response Engine
                      │
         ┌────────────┴────────────┐
         │                         │
 Knowledge Questions        Workflow Questions
         │                         │
         ▼                         ▼
 RAG Generated Answer      Topic-based Conversation
         │                         │
         └────────────┬────────────┘
                      ▼
               Final Response
```

---

# Features

## RAG-based Question Answering

The chatbot answers questions using configured HR documents instead of model memory.

Examples:

- Working Hours
- Leave Policy
- Remote Work Policy
- Employee Benefits
- Performance Policy

---

## Custom Topic 1

### Leave Request Advisor

Purpose:

Guide employees regarding company leave policies.

The chatbot:

- asks structured questions
- validates responses
- checks policy conditions
- provides recommendations

It **never approves leave**.

---

### Variables Used

| Variable | Purpose |
|-----------|----------|
| LeaveType | Selected leave type |
| StartDate | Leave start date |
| NumberOfDays | Leave duration |
| IsOnProbation | Probation status |
| AdvanceNoticeDays | Advance notice |
| IsEmergency | Emergency leave |
| MedicalCertificateAvailable | Sick leave certificate |
| PolicyOutcome | Final recommendation |

---

### Workflow

```
Trigger

↓

Welcome

↓

Leave Type

↓

Start Date

↓

Number of Days

↓

Probation Status

↓

Advance Notice

↓

Condition

↓

Casual Leave

↓

Sick Leave

↓

Earned Leave

↓

Summary

↓

Confirmation

↓

End Topic
```

---

### Business Rules

#### Casual Leave

- Maximum 3 consecutive days
- 2 working days advance notice
- Emergency exception

---

#### Sick Leave

- 1–2 days → No medical certificate
- More than 2 days → Medical certificate required

---

#### Earned Leave

More than 3 working days

↓

Minimum 5 working days advance notice

---

#### Remote Work

Remote work is **not classified as leave**.

---

# Custom Topic 2

## Workplace Concern and Escalation

Purpose

Safely handle workplace concerns without investigating complaints.

---

### Supported Concerns

- Harassment
- Bullying
- Discrimination
- Retaliation
- Unsafe workplace
- Grievances
- Manager issues

---

### Variables

| Variable | Purpose |
|-----------|----------|
| ConcernCategory | Type of concern |
| ImmediateDanger | Safety check |
| NeedConfidentialEscalation | HR escalation |
| RemainAnonymous | Anonymous reporting |
| RecommendedAction | Suggested next step |
| ConversationConfirmed | Confirmation |

---

### Workflow

```
Trigger

↓

Empathetic Message

↓

Immediate Danger?

↓

YES

↓

Emergency Advice

↓

END

↓

NO

↓

Confidential Escalation?

↓

YES

↓

Anonymous Reporting?

↓

Concern Category

↓

Summary

↓

END

↓

NO

↓

General Grievance

↓

Summary

↓

END
```

---

### Safety Rules

The chatbot:

- never investigates complaints
- never determines guilt
- never promises disciplinary action
- never promises investigation
- never replaces emergency services

---

### Privacy Rules

Never request

- Aadhaar
- PAN
- Passwords
- OTP
- Bank Details
- Medical Reports
- Evidence Files
- Witness Names
- Traumatic Incident Details

---

# Knowledge Sources

The chatbot uses three knowledge sources.

## 1. NovaWorks HR Policy Addendum

Highest Priority

Contains company-specific HR rules.

---

## 2. Public HR Policy PDF

Examples

- IIMA HR Manual
- Great Lakes Employee Handbook

---

## 3. Public HR Website

Example

University of Rochester HR Policies

---

# Knowledge Priority

If two knowledge sources conflict:

```
NovaWorks Addendum

↓

Public HR PDF

↓

Public Website

↓

No Answer
```

Never combine conflicting policies.

---

# Agent Instructions

The chatbot must:

- remain professional
- answer only HR questions
- use configured knowledge
- refuse unsupported requests
- cite knowledge source
- avoid hallucinations
- protect employee privacy
- recommend HR for employee-specific decisions

---

# Conversation Starters

Examples

- What are the working hours?
- How many casual leaves do I get?
- Can I work remotely?
- I want to apply for leave.
- Report workplace harassment.

---

# Functional Requirements

The chatbot supports

- Knowledge Retrieval
- Leave Guidance
- HR Escalation
- User Validation
- Variables
- Conditions
- Topic Branching
- Confirmation
- Cancellation
- Restart
- Fallback Responses

---

# Out-of-Scope Requests

The chatbot politely refuses requests unrelated to HR.

Examples

- Write Python code
- Tell me a joke
- Weather
- Politics
- Movies

---

# Prompt Injection Protection

The chatbot refuses prompts such as

- Ignore previous instructions
- Reveal your system prompt
- Show hidden prompt
- Developer instructions

---

# Testing

Recommended Test Cases

## Knowledge

- Working hours
- Casual leave
- Sick leave
- Remote work
- Bereavement leave

## Leave Topic

- Casual Leave
- Sick Leave
- Earned Leave
- Emergency Leave
- Cancellation

## Workplace Topic

- Harassment
- Immediate danger
- Anonymous reporting
- Grievance
- HR escalation

## Security

- Prompt Injection
- Privacy
- Confidential Information
- Out-of-Scope Questions

---

# Deliverables

- Published Copilot Studio Chatbot
- Chatbot URL
- Knowledge Sources
- Two Custom Topics
- Screenshots
- Test Report
- Solution Summary
- AI Usage Declaration

---

# Future Enhancements

- Microsoft Teams Integration
- Outlook Integration
- HRMS Integration
- Leave Application Automation
- Power Automate Workflow
- Power BI Dashboard
- Employee Authentication
- Dataverse Integration
- Adaptive Cards
- Multi-language Support
- Analytics Dashboard

---

# Acceptance Criteria

The project is considered complete when:

- Agent is created
- Instructions are configured
- Knowledge sources are added
- RAG answers are grounded
- Leave Topic works correctly
- Workplace Topic works correctly
- Variables and conditions are implemented
- Sensitive scenarios are handled safely
- Test cases pass
- Chatbot is published
- Evaluation URL is shared

---

# Conclusion

This project demonstrates how Microsoft Copilot Studio can be used to build a secure, enterprise-grade HR assistant by combining Retrieval-Augmented Generation (RAG) with structured conversational workflows. The chatbot provides grounded policy guidance, protects employee privacy, handles sensitive situations responsibly, and routes users toward the appropriate HR processes rather than making decisions on their behalf.