# Product Support and Warranty Assistant

## Overview

The **Product Support and Warranty Assistant** is a Microsoft Copilot Studio chatbot developed as part of the **P2-002 Project Build**. The solution assists customers with guided troubleshooting for supported Lenovo laptops and HP printers and performs a **preliminary warranty eligibility assessment** based on the NovaCare warranty policy.

The assistant provides structured troubleshooting, safety guidance, warranty classification, and service routing while ensuring that it does **not** make final warranty decisions or claim access to live backend systems.

---

# Features

## Guided Product Troubleshooting

- Supports Lenovo laptops and HP printers
- Product identification and validation
- Safety assessment before troubleshooting
- Issue-specific troubleshooting workflows
- Resolution confirmation
- Automatic support case summary generation
- Safety-critical escalation

## Warranty Eligibility Assessment

- Collects warranty-related information
- Validates purchase and delivery dates
- Calculates product age
- Applies NovaCare coverage rules
- Performs preliminary warranty classification
- Determines appropriate service route
- Generates a structured assessment summary
- Supports cross-topic redirection to troubleshooting

---

## Submission Report

**Project ID:** P2-002

**Participant Name:** Aditya Sodani

**GitHub Username:** Aditya-Sodani

**Chatbot Name:** NovaRetail Support Assistant

**Copilot Studio URL:** https://copilotstudio.microsoft.com/environments/Default-1e1572ff-a54c-4cd7-b2a9-20091afa5359/bots/59655d90-4c87-f111-8076-000d3af21e08/overview

**Sharing Method:** Shared with Ankur Saxena via Microsoft Copilot Studio

**Authentication Required:** No

**Supported Laptop Model:** Lenovo Laptop

**Supported Printer Model:** HP Printer

**Knowledge Sources Configured:** Lenovo Product Manuals, HP Product Manuals , HP Online Support , Lenova Online Support 

**Custom Topics Completed:** Guided Product Troubleshooting, Warranty Eligibility and Service Route Assessment

**Reusable Subtopics Completed:** Safety Assessment, Support Case Summary, Warranty Summary, Escalation Flow

**Number of Test Cases Executed:** 30

**Number of Passed Test Cases:** 26

**Number of Failed Test Cases:** 4

**Known Limitations:** Supports only Lenovo laptops and HP printers; no live warranty database integration; no repair status tracking; warranty assessment is preliminary only; final decisions require human review.

**AI Tools Used:** Microsoft Copilot Studio, ChatGPT (OpenAI)

**Submission Date:** 24-07-2026


# Supported Products

| Product Family | Support |
|---------------|---------|
| Lenovo Laptop | ✅ |
| HP Printer | ✅ |

---

# Troubleshooting Topics

### Lenovo Laptop

- No Power
- Charging
- Battery
- Display
- Wi-Fi
- Keyboard
- Touchpad
- Overheating
- Performance
- Other

### HP Printer

- Paper Jam
- Print Quality
- Other

---

# Warranty Classifications

The assistant can generate the following preliminary classifications:

- Potentially Covered
- Potential Dead-on-Arrival Assessment
- Potentially Excluded
- Outside Standard Coverage
- Insufficient Information
- Human Review Required
- Safety-Critical Escalation

---

# Service Routes

- Self-Service Information
- Technical Support Review
- Warranty Specialist Review
- Repeat Repair Review
- Paid Support Review
- Safety-Critical Escalation
- Additional Information Required

---

# Safety Features

The assistant immediately stops troubleshooting and recommends escalation when users report:

- Smoke
- Burning smell
- Sparks
- Swollen battery
- Electric shock
- Excessive heat
- Liquid damage


---
