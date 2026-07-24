# P2-002 | Product Support and Warranty Assistant

# NovaRetail Product Support & Warranty Assistant

An AI-powered **Product Support and Warranty Assistant** developed using **Microsoft Copilot Studio**. The chatbot helps customers troubleshoot supported Lenovo laptops and HP printers, provides grounded product guidance using official documentation, performs preliminary warranty assessments based on NovaCare policy, identifies safety-critical situations, and recommends the appropriate service route while maintaining responsible AI practices.

---

# Project Information

| Field | Details |
|--------|---------|
| **Project ID** | P2-002 |
| **Participant Name** | Pranay Gupta |
| **GitHub Username** | Pranaygupta-agileventures |
| **Chatbot Name** | NovaRetail Product Support & Warranty Assistant |
| **Platform** | Microsoft Copilot Studio |
| **Copilot Studio URL** | [Agent Link](https://copilotstudio.microsoft.com/environments/Default-1e1572ff-a54c-4cd7-b2a9-20091afa5359/bots/f9757893-4987-f111-8076-000d3af21e08/overview) |
| **Sharing Method** | Link |
| **Authentication Required** | Yes |
| **Supported Laptop Models** | Lenovo ThinkPad E14 Gen 5, Lenovo ThinkPad E16 Gen 1 |
| **Supported Printer Model** | HP LaserJet Pro MFP M428–M429 Series |
| **Knowledge Sources Configured** | NovaCare Limited Warranty Policy, Product Support Scope, Product Safety & Escalation Policy, Lenovo User Guide PDF, HP User Guide PDF, Lenovo Online User Guide, HP Support Website |
| **Custom Topics Completed** | 1. Guided Product Troubleshooting & Safety Triage <br> 2. Warranty Eligibility & Service Route Assessment |
| **Reusable Subtopics Completed** | 1. Product Safety Assessment <br> 2. Support Case Summary |
| **Number of Test Cases Executed** | 40 |
| **Passed Test Cases** | 30 |
| **Failed Test Cases** | 10 |
| **Known Limitations** | No live warranty lookup, repair booking, inventory visibility, repair status tracking, or final warranty approval |
| **AI Tools Used** | Microsoft Copilot Studio, ChatGPT (design, documentation, testing support) |
| **Submission Date** | 24/07/2026 |

---
# Project Overview

NovaRetail Product Support & Warranty Assistant is designed to provide first-line customer support for selected Lenovo laptops and HP printers. The chatbot combines Retrieval-Augmented Generation (RAG) with structured Copilot Studio topics to deliver accurate product guidance, perform safe troubleshooting, conduct preliminary warranty assessments, and recommend the appropriate support route.

The solution follows official Lenovo and HP documentation together with NovaRetail policies to ensure grounded, consistent, and policy-compliant responses.

---

# Project Objectives

- Provide accurate product support using official manufacturer documentation.
- Deliver safe and structured troubleshooting guidance.
- Perform preliminary warranty eligibility assessments.
- Identify safety-critical situations before troubleshooting.
- Route customers to the appropriate service path.
- Reduce routine support requests through self-service.
- Apply responsible AI and knowledge-source precedence.

---

# Features

## Product Support

Supports:

- Lenovo ThinkPad E14 Gen 5
- Lenovo ThinkPad E16 Gen 1
- HP LaserJet Pro MFP M428–M429 Series

Provides assistance with:

- Product setup
- Power and charging issues
- Battery guidance
- Display issues
- Connectivity problems
- Keyboard and touchpad issues
- Printer setup
- Printing and scanning
- Paper jams
- Print quality
- Toner guidance
- Network connectivity

---

## Responsible AI Features

The chatbot follows responsible AI principles by:

- Using only configured knowledge sources.
- Preventing unsupported or fabricated responses.
- Protecting customer privacy.
- Rejecting prompt injection attempts.
- Maintaining product and policy source precedence.
- Avoiding final warranty decisions.
- Escalating safety-critical scenarios.

---

# Technology Stack

| Component | Technology |
|-----------|------------|
| AI Platform | Microsoft Copilot Studio |
| Knowledge Retrieval | Retrieval-Augmented Generation (RAG) |
| Knowledge Sources | Markdown Policies, PDF Manuals & Official Websites |
| Topic Authoring | Microsoft Copilot Studio |
| Natural Language Processing | Microsoft Copilot Studio |
| Testing | Manual Functional Testing |

---

# Conversation Flow

```text
Customer Query
        │
        ▼
Identify Product
        │
        ▼
Knowledge Retrieval (RAG)
        │
        ▼
Custom Topic Trigger
      │             │
     Yes            No
      │             │
      ▼             ▼
Structured Topic   Grounded Response
      │             │
      └──────┬──────┘
             ▼
 Final Product Support Response
```

---

# Repository Structure

```text
p2-002_product_support_warranty_assistant/
│
├── README.md
├── chatbot-url.md
├── solution-summary.md
├── agent-design.md
├── knowledge-sources.md
├── custom-topic-design.md
├── test-report.md
├── known-limitations.md
├── ai-usage-declaration.md
│
├── knowledge-base/
│   ├── novacare-limited-warranty-policy.md
│   ├── product-support-scope.md
│   └── product-safety-and-escalation-policy.md
│
└── screenshots/
```

---

# Author

**Participant Name:** Pranay Gupta

**Project ID:** P2-002

**Project:** Product Support and Warranty Assistant

**Platform:** Microsoft Copilot Studio