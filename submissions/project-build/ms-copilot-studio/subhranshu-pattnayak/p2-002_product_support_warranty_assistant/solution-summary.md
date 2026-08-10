# Solution Summary

## Business Problem

NovaRetail receives repetitive customer enquiries related to laptop and printer setup, troubleshooting, warranty coverage, and product safety. The objective of this project is to automate first-line support while ensuring safe, policy-compliant responses.

---

# Target Users

- Retail customers
- Product owners
- First-line support users

---

# Scope

Supported products:

- Lenovo ThinkPad E14 Gen 5
- HP LaserJet Pro MFP M428-M429

Unsupported products are identified early and redirected to human support.

---

# Capabilities

- Product identification
- Official manual retrieval
- Guided troubleshooting
- Warranty assessment
- Safety triage
- Human escalation
- Support summary generation

---

# Knowledge Architecture

The assistant uses Retrieval-Augmented Generation with the following precedence:

## Technical Questions

1. Lenovo/HP Official PDF
2. Lenovo/HP Official Website
3. Product Support Scope

## Warranty Questions

1. NovaCare Warranty Policy
2. Product Safety Policy

## Safety

1. Product Safety Policy
2. Manufacturer Safety Documentation

---

# Topic Architecture

## Main Topics

- Guided Product Troubleshooting and Safety Triage
- Warranty Eligibility Assessment

## Shared Topics

- Product Safety Assessment
- Support Case Summary

---

# Safety Controls

- Mandatory safety assessment
- Stops troubleshooting for critical hazards
- Immediate escalation for Level 4 incidents
- No unsafe repair guidance

---

# Decision Boundaries

The assistant:

- does not approve warranty claims
- does not create repair requests
- does not check live warranty databases
- does not fabricate product information
- escalates ambiguous cases to human support

---

# Implementation Decisions

- Global variables used for cross-topic data sharing
- Reusable subtopics reduce duplicated logic
- Multiple-choice product identification prevents unsupported retrieval
- Grounded AI responses restricted to configured knowledge sources