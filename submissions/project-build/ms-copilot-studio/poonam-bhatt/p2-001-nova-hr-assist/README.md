# NovaHR Assist

## Project Overview

NovaHR Assist is an AI-powered HR Employee Assistance chatbot built using Microsoft Copilot Studio. The chatbot helps employees quickly access HR policy information using Retrieval-Augmented Generation (RAG) with configured knowledge sources.

The chatbot provides grounded responses using official HR documents and prioritizes NovaWorks-specific policies over general HR guidance. It does not make HR decisions or approve employee requests.

## Features

- General HR policy guidance
- Grounded responses using configured knowledge sources
- Source-aware answers
- Leave Request Advisor custom topic
- Workplace Concern and Escalation custom topic
- Employee privacy and confidential information protection
- HR escalation guidance
- Safe handling of sensitive workplace scenarios

## Knowledge Sources

1. NovaWorks_HR_Policy_Addendum_v1.0.docx
2. HR-Policy-Manual-02.pdf
3. University of Rochester Human Resources Policies Website

## Custom Topics

### Leave Request Advisor
Guides employees through leave-related questions by collecting required information, evaluating the request against NovaWorks HR policy, and providing policy-based guidance. The chatbot does not approve leave requests.

### Workplace Concern and Escalation
Provides empathetic guidance for workplace concerns such as harassment, bullying, discrimination, retaliation, and safety issues. It prioritizes employee safety and recommends confidential HR escalation when appropriate.

## Limitations

- Cannot access employee records
- Cannot approve leave
- Cannot calculate leave balances
- Cannot provide legal or medical advice
- Answers only from configured knowledge sources
- Cannot add triggers inside the topic.

## Technologies

- Microsoft Copilot Studio
- Generative AI
- Retrieval-Augmented Generation (RAG)
- Knowledge Sources
- Custom Topics