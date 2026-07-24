# IIMA HR Policy Assistant

An AI-powered HR Policy Assistant built using **Microsoft Copilot Studio** that helps employees quickly access HR policies, understand leave rules, and receive guidance on workplace-related queries through natural language conversations.


# Project Overview

The IIMA HR Policy Assistant is a conversational AI chatbot designed to answer employee HR-related questions using organizational policy documents and custom conversational topics.

The chatbot combines:

-  Retrieval-Augmented Generation (RAG)
-  Knowledge Sources
-  Custom Topics
-  Agent Instructions

to provide accurate, context-aware, and user-friendly responses.


#  Objectives

- Reduce HR workload by automating common employee queries.
- Provide instant and accurate answers based on official HR documents.
- Guide employees through leave-related scenarios.
- Deliver grounded responses using organizational knowledge sources.
- Demonstrate the capabilities of Microsoft Copilot Studio in enterprise HR automation.


# Technologies Used

| Technology | Purpose |
|------------|---------|
| Microsoft Copilot Studio | Conversational AI Development |
| Microsoft Power Platform | Agent Deployment |
| Retrieval-Augmented Generation (RAG) | Knowledge Retrieval |
| Knowledge Sources | HR Policies & Documents |
| Natural Language Understanding | User Intent Recognition |


#  Knowledge Sources

The chatbot retrieves information from the following sources:

- HR Policy Addendum
- IIMA HR Policy PDF
- University of Rochester HR Website (Reference Knowledge)

These documents enable the chatbot to provide grounded and accurate responses.


#  Agent Instructions

Custom agent instructions were configured to:

- Respond professionally.
- Answer only using available knowledge.
- Avoid generating unsupported information.
- Ask follow-up questions when additional clarification is required.
- Maintain a helpful HR assistant tone.

---

#  Custom Topics

##  Leave Request Advisor

This topic assists employees with:

- Leave eligibility
- Leave planning
- Leave recommendations
- Follow-up leave guidance

Status:

Implemented


##  Workplace Concern

This topic is intended to assist employees with workplace-related concerns and grievances.

Status:

 Implemented


#  Features

- HR Policy Question Answering
- Leave Policy Guidance
- Employee Benefits Information
- Working Hours Information
- Holiday Information
- Policy Clarification
- Context-Aware Responses
- Multi-document Knowledge Retrieval
- Conversational Leave Advisor
- Natural Language Interaction

---

# Test Coverage

| Category | Status |
|----------|--------|
| Knowledge Source Test Cases |  Completed |
| Leave Advisor Topic |  Completed |
| Workplace Concern Topic | Pending |


#  How It Works

1. User asks an HR-related question.
2. Copilot Studio analyzes the user's intent.
3. If a matching custom topic exists, the chatbot follows the predefined conversation flow.
4. Otherwise, it retrieves relevant information from the configured knowledge sources using RAG.
5. The chatbot generates a grounded response based on the retrieved content and agent instructions.

---

#  Example Questions

### Knowledge-Based Queries

- What is the leave policy?
- What are the working hours?
- How many casual leaves are allowed?
- What benefits are available for employees?
- Explain the HR attendance policy.

### Leave Advisor

- I want to apply for leave.
- Which leave should I take?
- I need leave for medical reasons.
- Can you help me choose the correct leave type?

---

# 🔍 Current Limitations

- Workplace Concern topic has not yet been implemented.
- Responses are limited to the configured knowledge sources.
- The chatbot cannot answer questions outside the provided HR documentation.


#  Future Enhancements

- Implement Workplace Concern Advisor.
- Integrate Microsoft Teams.
- Connect with HRMS for leave balance retrieval.
- Support multilingual conversations.
- Enable adaptive cards for leave requests.
- Add Power Automate workflows for leave approval.
- Integrate employee authentication.
- Provide analytics and conversation insights.


# Learning Outcomes

This project demonstrates practical experience with:

- Microsoft Copilot Studio
- Retrieval-Augmented Generation (RAG)
- Knowledge Source Configuration
- Conversational AI Design
- Topic-Based Conversation Flows
- Enterprise HR Automation
- AI Prompt Engineering
- Agent Instructions
- Conversational Testing


#  Author

**Nandani Bisht**
