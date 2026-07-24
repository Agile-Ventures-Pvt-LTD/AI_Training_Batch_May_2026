# P2-002 Product Support & Warranty Assistant

## Project Information

| Field | Details |
|--------|---------|
| **Project ID** | P2-002 |
| **Participant Name** | Vikash Kumar |
| **GitHub Username** | Vikash-agile |
| **Chatbot Name** | NovaRetail Product Support & Warranty Assistant |
| **Microsoft Copilot Studio URL** | *Refer to `chatbot-url.md`* |
| **Sharing Method** | Published through Microsoft Copilot Studio Demo Website and shared with the evaluator (Ankur Saxena). |
| **Authentication Required** | No (Public Demo Website) |

---

# Project Overview

The **NovaRetail Product Support & Warranty Assistant** is an AI-powered chatbot built using **Microsoft Copilot Studio**. It provides safe, knowledge-grounded troubleshooting, preliminary warranty eligibility assessment, and service route recommendations for supported Lenovo laptops and HP printers.

The chatbot uses Retrieval-Augmented Generation (RAG) with official knowledge sources and reusable conversational topics to deliver consistent and policy-compliant responses.

---

# Supported Products

## Supported Laptop Model

- Lenovo ThinkPad E14 Gen 5

## Supported Printer Model

- HP LaserJet Pro MFP M428-M429

## Supported Accessories

- Bundled Laptop Battery
- Bundled Charger
- Bundled Power Cable

---

# Knowledge Sources Configured

The chatbot is grounded using the following official knowledge sources:

### Markdown Documents

- NovaCare Limited Warranty Policy
- Product Support Scope
- Product Safety and Escalation Policy

### Product Documentation

- Lenovo ThinkPad E14 Gen 5 User Guide (PDF)
- HP LaserJet Pro MFP M428-M429 User Guide (PDF)

### Official Websites

- Lenovo Support
- HP Support

---

# Custom Topics Completed

- Guided Product Troubleshooting and Safety Triage
- Warranty Eligibility and Service Route Assessment
- Repair Escalation and Appointment Preparation *(Optional Advanced Topic)*

---

# Reusable Subtopics Completed

- Product Safety Assessment
- Support Case Summary

---

# Utility Topics

- Unsupported Product Handler
- Human Escalation
- Cancellation & Restart

---

# Testing Summary

| Metric | Value |
|--------|------:|
| **Number of Test Cases Executed** | 40 |
| **Passed Test Cases** | 23 |
| **Failed Test Cases** | 17 |
| **Errors** | 0 |

> *These values should match the latest evaluation results in Copilot Studio. Update them if you re-run the evaluation.*

---

# Known Limitations

- Supports only products defined in the project scope.
- Provides preliminary warranty assessment only.
- Does not approve or reject warranty claims.
- Does not create support tickets or repair appointments.
- Does not access live warranty databases or customer records.
- Does not integrate with CRM or ERP systems.
- Uses only configured knowledge sources.
- Requires human review for final warranty decisions.

Refer to **known-limitations.md** for complete details.

---

# AI Tools Used

The following AI tools were used during development:

- Microsoft Copilot Studio
- ChatGPT (OpenAI)

AI assistance was used for documentation, workflow planning, prompt refinement, and implementation guidance. All chatbot configuration, testing, validation, and final review were completed by the participant.

---

# Repository Contents

```text
README.md
chatbot-url.md
solution-summary.md
agent-design.md
knowledge-sources.md
custom-topic-design.md
test-report.md
known-limitations.md
ai-usage-declaration.md
screenshots.md
screenshots/
```

---

# Submission Checklist

- Repository path verified
-  Chatbot published
-  Chatbot URL shared with Ankur Saxena
-  Chatbot URL accessible with required permissions
-  Required Markdown files included
-  Official knowledge-source links documented
-  Required screenshots captured and readable
-  No confidential information committed
-  Repository structure follows project requirements

---

# Submission Date

**Date:** 24/07/2026

---

# Final Submission Condition

I confirm that:

- The repository path is correct.
- The chatbot URL has been shared with **Ankur Saxena**.
- The published chatbot is accessible with the documented permissions.
- All required Markdown documents are included.
- All screenshots are readable.
- Official knowledge-source links are recorded.
- No confidential or sensitive information has been committed.
- The solution is ready for evaluation according to the P2-002 project requirements.

# Author

Vikash Kumar