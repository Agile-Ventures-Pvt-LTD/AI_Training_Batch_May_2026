# 🖥️ Product Support & Warranty Assistant (Laptop Support)

> An AI-powered customer support assistant built with **Microsoft Copilot Studio** to provide guided laptop troubleshooting, product safety assessment, and preliminary warranty eligibility evaluation for **Lenovo ThinkPad E14 Gen 5**.

---

# Project Information

| Item | Details |
|------|---------|
| **Project ID** | **P2-002** |
| **Participant Name** | Ashish Sinha |
| **GitHub Username** | *Ashish-Agile* |
| **Chatbot Name** | Ashish_product_support _warranty_assistant |
| **Microsoft Copilot Studio URL** | https://copilotstudio.preview.microsoft.com/environments/Default-1e1572ff-a54c-4cd7-b2a9-20091afa5359/bots/35aa5099-4a87-f111-8076-000d3af21e08/overview |
| **Sharing Method** | Public Web Link *(Update after publishing)* |
| **Authentication Required** | No (Development Environment) |
| **Supported Laptop Model** | Lenovo ThinkPad E14 Gen 5 |
| **Supported Printer Model** | Not Implemented (Current Scope: Laptop Only) |
| **Knowledge Sources Configured** | 4 |
| **Custom Topics Completed** | 2 |
| **Reusable Subtopics Completed** | 2 |
| **Number of Test Cases Executed** | 16 |
| **Number of Passed Test Cases** |10 |
| **Number of Failed Test Cases** | 6 |
| **Known Limitations** | No live warranty lookup, no service ticket creation, no repair status tracking, laptop support only, no final warranty decisions, no inventory visibility |
| **AI Tools Used** | Microsoft Copilot Studio, ChatGPT |
| **Submission Date** | 24 July 2026 |

# 📌 Project Overview

The **Product Support & Warranty Assistant** is an intelligent virtual assistant designed to improve customer support by providing safe, structured, and policy-compliant assistance before escalating issues to human support teams.

The assistant helps customers:

- Troubleshoot laptop issues safely
- Perform product safety assessment
- Conduct preliminary warranty eligibility assessment
- Determine the appropriate service route
- Generate structured support summaries
- Reduce unnecessary support tickets

The assistant **does not**:

- Approve warranty claims
- Reject warranty claims
- Promise repair or replacement
- Perform remote access
- Recommend unsafe troubleshooting
- Ask customers to dismantle hardware

---

# 🎯 Project Objectives

- Improve first-contact resolution
- Reduce support workload
- Standardize troubleshooting
- Ensure customer safety
- Provide policy-based warranty guidance
- Improve customer experience

---

# 🏢 Business Scenario

NovaRetail provides after-sales support for Lenovo laptops.

Customers frequently contact support regarding:

- Laptop not powering on
- Charging issues
- Battery draining rapidly
- Display issues
- Wi-Fi problems
- Keyboard issues
- Warranty eligibility
- Product safety concerns

This Copilot Assistant performs an initial assessment before escalating cases to technical support.

---

# 🛠 Technology Stack

| Technology | Purpose |
|------------|---------|
| Microsoft Copilot Studio | Conversational AI |
| Microsoft Power Platform | Automation |
| Generative AI | Knowledge-based Answers |
| Microsoft Dataverse | Data Storage (Optional) |
| Microsoft Learn Knowledge Sources | Lenovo Documentation |
| Adaptive Cards | Rich Responses (Optional) |

---

# 📂 Project Structure

```
Product-Support-Warranty-Assistant/
│
├── README.md
│
├── knowledge/
│   ├── KnowledgeDocument1.md
│   ├── KnowledgeDocument2.md
│   └── KnowledgeDocument3.md
│
│
├── documentation/
│
└── screenshots/
```

---

# 💻 Supported Product

Currently supported:

- Lenovo ThinkPad E14 Gen 5

Future versions can support:

- HP Printers
- Accessories
- Additional Lenovo Laptop Models

---

# 🚀 Features

## Product Validation

- Validate supported laptop model
- Prevent unsupported model troubleshooting
- Guide unsupported products appropriately

---

## Product Safety Assessment

- Detect safety hazards
- Identify smoke
- Detect sparks
- Detect burning smell
- Detect electric shock
- Detect overheating
- Stop unsafe troubleshooting
- Escalate safety-critical cases

---

## Guided Laptop Troubleshooting

Supports:

- No Power
- Charging Failure
- Battery Draining
- Blank Display
- External Display
- Wi-Fi Issues
- Keyboard Issues
- Overheating

---

## Warranty Eligibility Assessment

Collects:

- Purchase Date
- Invoice Availability
- Serial Number
- Product Age
- Damage Information
- Previous Repairs
- Warranty Classification

Provides only a **preliminary assessment**.

---

## Support Case Summary

Generates a structured summary including:

- Product
- Issue
- Troubleshooting
- Safety Status
- Warranty Classification
- Escalation Level
- Recommended Next Action

---

# 🔄 Conversation Flow

```
Customer
      │
      ▼
Welcome
      │
      ▼
Product Validation
      │
      ▼
Safety Assessment
      │
      ├──────── Safety Critical
      │               │
      │               ▼
      │         Escalation
      │
      ▼
Issue Collection
      │
      ▼
Laptop Troubleshooting
      │
      ▼
Issue Resolved?
      │
      ├──── Yes
      │        ▼
      │  Support Summary
      │
      └──── No
               ▼
Warranty Assessment
               │
               ▼
Service Route
               │
               ▼
Conversation Ends
```

---

# 📋 Topics Implemented

## Main Topics

- Guided Laptop Troubleshooting
- Warranty Eligibility Assessment

## Reusable Subtopics

- Product Safety Assessment
- Support Case Summary

---

# 📚 Knowledge Sources

The assistant uses Lenovo product documentation for:

- Troubleshooting
- Safe operating guidance
- Error handling
- Hardware recommendations

Generative AI responses are restricted to approved documentation.

---

# ⚠ Safety Principles

The assistant never:

- Recommends dangerous actions
- Requests hardware disassembly
- Continues after detecting safety risks
- Claims a repair is complete
- Guarantees warranty approval

---

# 🔐 Warranty Disclaimer

This assistant provides only a **preliminary warranty assessment**.

Final decisions are made by authorized warranty specialists after reviewing the product and supporting documents.

---

# 📈 Future Enhancements

- Multi-product support
- HP printer troubleshooting
- Automatic warranty lookup
- CRM integration
- Live service ticket creation
- Microsoft Teams integration
- Power Automate workflows
- Voice-enabled Copilot
- Customer sentiment analysis
- Predictive issue detection

---

# 👨‍💻 Author

**Ashish Sinha**


---

