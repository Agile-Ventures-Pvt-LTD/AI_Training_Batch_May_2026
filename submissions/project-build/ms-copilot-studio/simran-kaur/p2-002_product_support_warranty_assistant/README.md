# NovaCare Product Support and Warranty Assistant

## Project Information

**Project ID:** P2-002

**Project Name:** Product Support and Warranty Assistant

**Participant:** Simran Kaur

**Platform:** Microsoft Copilot Studio

---

# Project Overview

The **NovaCare Product Support and Warranty Assistant** is an AI-powered customer support chatbot developed using Microsoft Copilot Studio. It assists customers with product-related questions, guided troubleshooting, product safety checks, and preliminary warranty eligibility assessments for supported Lenovo laptops and HP printers.

The assistant uses official product documentation, NovaCare warranty policies, and company-defined support procedures to provide accurate and grounded responses. It is designed to improve the customer support experience while ensuring that all recommendations remain within defined business policies.

---

# Project Objective

The primary objective of this project is to develop a structured customer support assistant that can:

* Answer product-related questions using official documentation.
* Guide users through approved troubleshooting procedures.
* Detect and respond appropriately to safety-critical situations.
* Perform a preliminary warranty eligibility assessment.
* Recommend the appropriate service route based on the collected information.
* Maintain clear decision boundaries without making final warranty decisions.

---

# Supported Products

The chatbot currently supports the following product categories:

### Lenovo Laptop

* Lenovo ThinkPad Series

### HP Printer

* HP LaserJet Series

If a customer requests support for an unsupported product, the assistant informs them of the limitation and recommends contacting an authorized support representative.

---

# Key Features

The chatbot provides the following capabilities:

* Product information retrieval from official knowledge sources.
* Guided troubleshooting for supported devices.
* Product safety assessment and escalation.
* Preliminary warranty eligibility assessment.
* Warranty coverage and exclusion checks.
* Repeat repair assessment.
* Service route recommendation.
* Support case summary generation.
* Customer confirmation and correction workflow.
* Cross-topic navigation between troubleshooting and warranty assessment.
* Variable-based conversation flow with conditional branching.

---

# Custom Topics

### Topic 1 – Guided Product Troubleshooting and Safety Triage

This topic guides customers through approved troubleshooting steps for supported Lenovo laptops and HP printers. During the troubleshooting process, the assistant continuously checks for safety-related issues such as smoke, overheating, swollen batteries, electric shock, or liquid damage. If a safety-critical condition is identified, normal troubleshooting is stopped immediately and the appropriate escalation guidance is provided.

### Topic 2 – Preliminary Warranty Eligibility Assessment

This topic performs a structured preliminary warranty assessment based on the NovaCare warranty policy. It evaluates warranty coverage, applicable exclusions, dead-on-arrival conditions, repeat repairs, and required documentation before recommending an appropriate service route. The assistant does not approve or reject warranty claims; it only provides an initial assessment.

---

# Reusable Subtopics

## Product Safety Assessment

This reusable subtopic evaluates safety-related conditions reported by the customer. When a hazardous situation is detected, the assistant immediately stops routine troubleshooting and provides appropriate safety guidance.

## Support Case Summary

This reusable subtopic generates a structured summary of the interaction, including the customer's product details, issue description, troubleshooting progress, warranty assessment, service recommendation, and suggested next steps.

---

# Knowledge Sources

The assistant retrieves information from multiple trusted sources.

### Internal Knowledge Base

* NovaCare Limited Warranty Policy
* Product Support Scope
* Product Safety and Escalation Policy

### Official Product Documentation

* Lenovo laptop manual PDF
* HP printer user manual PDF

### Official Manufacturer Websites

* Lenovo Support
* HP Support

---

# Knowledge Priority

When multiple sources contain similar information, the assistant follows the following priority:

1. Product Safety and Escalation Policy
2. NovaCare Limited Warranty Policy
3. Official Product Manuals
4. Official Manufacturer Websites

This ensures that warranty decisions follow NovaCare policy while technical guidance comes from official manufacturer documentation.

---

# Safety and Decision Boundaries

The chatbot is designed to operate within clearly defined boundaries.

It does **not**:

* Approve warranty claims.
* Reject warranty claims.
* Guarantee repairs or replacements.
* Create support tickets.
* Access live warranty or repair systems.
* Provide legal advice.
* Invent unsupported product information.

Whenever sufficient information is unavailable, the assistant requests additional details instead of making assumptions.

---

# High-Level Workflow

Customer Request

↓

Identify Product

↓

Retrieve Product Information

↓

Guided Troubleshooting (if required)

↓

Safety Assessment

↓

Warranty Eligibility Assessment

↓

Service Route Recommendation

↓

Support Case Summary

↓

Customer Confirmation

---

# Technologies Used

* Microsoft Copilot Studio
* Markdown Knowledge Sources
* PDF Knowledge Sources
* Official Public Websites

---

# Current Limitations

The current implementation has the following limitations:

* Supports only selected Lenovo laptops and HP printers.
* Does not integrate with live warranty or repair management systems.
* Cannot create support cases automatically.
* Cannot track repair progress.
* Does not provide final warranty approval or rejection.

---

# Repository Structure

```text
submissions/
└── project-build/
    └── ms-copilot-studio/
        └── simran-kaur/
            └── p2-002_product_support_warranty_assistant/
```

---

# Project Status

The chatbot has been developed, tested, and published as part of the Phase 2 Project Build. It demonstrates the use of Microsoft Copilot Studio to build a structured enterprise support assistant with knowledge grounding, reusable subtopics, conditional conversation flows, safety controls, and policy-based warranty assessment.


# Project Information

| Field | Details |
|--------|---------|
| **Project ID** | P2-002 |
| **Participant Name** | Simran Kaur |
| **GitHub Username** | participant-simran-kaur |
| **Chatbot Name** | NovaCare Product Support and Warranty Assistant |
| **Copilot Studio URL** | https://copilotstudio.preview.microsoft.com/environments/Default-1e1572ff-a54c-4cd7-b2a9-20091afa5359/bots/6fcfdfd0-4c87-f111-8076-000d3af21e08/overview|
| **Sharing Method** | Copilot Studio Demo Website |
| **Authentication Required** | Yes (Microsoft Entra ID / Organization Account) |
| **Supported Laptop Model** | Lenovo ThinkPad E14 Gen 5 |
| **Supported Printer Model** | HP LaserJet Pro MFP M428-M429 |
| **Knowledge Sources Configured** | NovaCare Limited Warranty Policy, Product Support Scope, Product Safety and Escalation Policy, Lenovo PDF, Lenovo Support Website, HP PDF, HP Support Website |
| **Custom Topics Completed** | Guided Product Troubleshooting and Safety Triage, Warranty Eligibility and Service Route Assessment |
| **Reusable Subtopics Completed** | Product Safety Assessment, Support Case Summary |
| **Number of Test Cases Executed** | 25 |
| **Number of Passed Test Cases** | 25 |
| **Number of Failed Test Cases** | 0 |
| **Known Limitations** | No live warranty lookup, case creation, repair status, final warranty decisions, emergency integration, or inventory visibility |
| **AI Tools Used** | ChatGPT, Microsoft Copilot Studio AI capabilities |
| **Submission Date** | 24 July 2026 |
| **Final Submission Condition** | Chatbot published, URL shared with Ankur Saxena, all required artifacts committed to the mandatory GitHub repository path, required screenshots included, and no confidential information exposed. |