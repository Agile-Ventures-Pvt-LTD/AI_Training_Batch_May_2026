# Solution Summary

## Project Overview

The **NovaRetail Product Support & Warranty Assistant** is an AI-powered customer support chatbot developed using **Microsoft Copilot Studio**. The solution combines Retrieval-Augmented Generation (RAG) with structured conversational topics to provide safe, accurate, and policy-compliant assistance for selected Lenovo laptops and HP printers.

The chatbot supports customers throughout the initial support journey by identifying supported products, guiding users through structured troubleshooting, providing preliminary warranty guidance based on NovaRetail policies, detecting safety-critical situations, and recommending the appropriate service route when human intervention is required.

---

# Business Problem

Customer support teams frequently receive repetitive requests related to product setup, troubleshooting, warranty coverage, and safety concerns. These requests increase support workload and often delay responses for customers requiring immediate assistance.

Additionally, inconsistent responses and the use of unofficial information can lead to incorrect troubleshooting steps or misunderstanding of warranty policies.

The chatbot addresses these challenges by providing a consistent, knowledge-grounded, and policy-driven self-service experience.

---

# Solution Objectives

The solution was designed to:

- Deliver accurate product support using official Lenovo and HP documentation.
- Guide customers through structured and safe troubleshooting workflows.
- Perform preliminary warranty eligibility assessments using NovaCare policies.
- Identify safety-critical situations before technical troubleshooting begins.
- Recommend the appropriate service route without making final warranty decisions.
- Reduce repetitive customer support requests through self-service.
- Ensure all responses follow responsible AI principles.

---

# Solution Scope

The chatbot currently supports the following products:

### Lenovo Laptops

- ThinkPad E14 Gen 5
- ThinkPad E16 Gen 1

### HP Printers

- HP LaserJet Pro MFP M428–M429 Series

Support is limited to these configured products and associated knowledge sources.

---

# Core Functionalities

The chatbot provides the following capabilities:

- Product identification and validation
- Guided product troubleshooting
- Product safety assessment
- Preliminary warranty eligibility assessment
- Service route recommendation
- Support case summary generation
- Human escalation guidance
- Grounded responses using configured knowledge sources

---

# Solution Architecture

```text
                    Customer
                        │
                        ▼
          Microsoft Copilot Studio
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
 Knowledge Sources   Custom Topics   Policy Rules
        │
        ▼
 Retrieval-Augmented Generation (RAG)
        │
        ▼
 Grounded Product & Warranty Response
```

---

# Knowledge Sources

The chatbot retrieves information from the following configured sources:

### NovaRetail Policies

- NovaCare Limited Warranty Policy
- Product Support Scope
- Product Safety and Escalation Policy

### Official Product Documentation

- Lenovo ThinkPad E14 Gen 5 & E16 Gen 1 User Guide (PDF)
- HP LaserJet Pro M428–M429 User Guide (PDF)

### Official Websites

- Lenovo Online User Guide
- HP Official Support Website

Responses are generated only from these approved knowledge sources.

---

# Custom Topics Implemented

## Guided Product Troubleshooting & Safety Triage

This topic guides customers through structured troubleshooting by:

- Validating supported products
- Collecting issue details
- Performing mandatory safety assessment
- Providing model-specific troubleshooting
- Tracking troubleshooting attempts
- Escalating unresolved or unsafe cases

---

## Warranty Eligibility & Service Route Assessment

This topic performs a preliminary warranty assessment by:

- Collecting purchase information
- Validating warranty inputs
- Applying NovaCare coverage rules
- Identifying exclusions
- Assessing potential dead-on-arrival (DOA) scenarios
- Recommending the appropriate service route

---

# Responsible AI Implementation

The chatbot follows responsible AI practices by:

- Restricting responses to approved knowledge sources
- Preventing unsupported or fabricated information
- Protecting customer privacy
- Detecting safety-critical situations
- Preventing unsafe troubleshooting
- Avoiding final warranty approval or rejection
- Recommending human review when required

---

# Expected Benefits

Implementation of the chatbot provides several benefits:

- Faster first-line customer support
- Consistent troubleshooting guidance
- Reduced workload for support teams
- Improved customer self-service
- Safer handling of hazardous situations
- Standardised preliminary warranty assessments
- Improved customer experience through structured conversations

---

# Current Limitations

The chatbot does not:

- Access live warranty databases
- Approve or reject warranty claims
- Create repair requests
- Track repair status
- Access customer accounts
- Support products outside the configured scope

These activities require authorised NovaRetail representatives.

---

# Conclusion

The NovaRetail Product Support & Warranty Assistant provides a structured, safe, and knowledge-driven customer support experience by combining Microsoft Copilot Studio, Retrieval-Augmented Generation (RAG), official product documentation, and NovaRetail policies. The solution improves self-service capabilities while ensuring that warranty decisions and complex cases remain under the responsibility of authorised human support teams.