# P2-002 Product Support and Warranty Assistant

## Project Information

| Field | Details |
|-------|---------|
| **Project ID** | P2-002 |
| **Project Title** | Product Support and Warranty Assistant |
| **Participant** | Vikash Kumar |
| **Chatbot Name** | NovaRetail Product Support & Warranty Assistant |
| **Platform** | Microsoft Copilot Studio |

---

# Objective

Develop an AI-powered Product Support and Warranty Assistant using Microsoft Copilot Studio that provides safe, knowledge-grounded troubleshooting and preliminary warranty guidance for supported Lenovo and HP products.

The assistant helps customers troubleshoot common issues, assess warranty eligibility, identify safety-critical situations, and prepare information for human support while remaining within defined safety and business boundaries.

---

# Supported Products

## Laptops

- Lenovo ThinkPad E14 Gen 5

## Printers

- HP LaserJet Pro MFP M428-M429

## Accessories

- Bundled Lenovo Charger
- Bundled Lenovo Power Cable

---

# Features

- Guided product troubleshooting
- Product model validation
- Safety assessment before troubleshooting
- Preliminary warranty eligibility assessment
- Human escalation guidance
- Support case summary generation
- Unsupported product handling
- Conversation cancellation and restart
- Optional repair escalation and appointment preparation
- Knowledge-grounded responses using official documentation

---

# Custom Topics

## Main Topics

1. Guided Product Troubleshooting and Safety Triage
2. Warranty Eligibility and Service Route Assessment
3. Repair Escalation and Appointment Preparation *(Optional Advanced Topic)*

---

## Reusable Topics

- Product Safety Assessment
- Support Case Summary

---

## Utility Topics

- Unsupported Product Handler
- Human Escalation
- Cancellation & Restart

---

# Knowledge Sources

## Markdown Documents

- NovaCare Limited Warranty Policy
- Product Support Scope
- Product Safety and Escalation Policy

## Product Documentation

- Lenovo ThinkPad E14 Gen 5 User Guide (PDF)
- HP LaserJet Pro MFP M428-M429 User Guide (PDF)

## Official Websites

- Lenovo Support
- HP Support

---

# Safety Controls

- Mandatory safety assessment before troubleshooting
- Detection of safety-critical conditions
- Immediate escalation for Level 4 safety issues
- No unsafe troubleshooting instructions
- No device dismantling guidance
- No remote access instructions
- No requests to reproduce hazardous conditions

---

# Decision Boundaries

The assistant does **not**:

- Approve or reject warranty claims
- Create support cases
- Book repair appointments
- Assign technicians
- Reserve replacement products
- Perform live inventory lookups
- Provide repair status updates
- Access customer account records
- Make final warranty decisions

All warranty decisions remain the responsibility of authorised NovaRetail representatives.

---

# Chatbot URL

The published chatbot URL is provided in:

**chatbot-url.md**

---

# Project Status

**Status:** Completed

The chatbot includes:

- Supported product validation
- Safety assessment
- Guided troubleshooting
- Warranty assessment
- Human escalation
- Reusable subtopics
- Knowledge-grounded responses

---

# Known Limitations

- Supports only the products defined in the project scope.
- Uses only configured knowledge sources.
- Does not integrate with live CRM, ERP, or ticketing systems.
- Cannot create appointments or service requests.
- Cannot provide repair tracking or inventory availability.
- Cannot make final warranty approval decisions.

Refer to **known-limitations.md** for complete details.

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
```

---

# Submission Checklist

- Microsoft Copilot Studio chatbot created
- Knowledge sources configured
- Required custom topics implemented
- Reusable subtopics implemented
- Test cases executed
- Chatbot published
- Documentation completed

---

# Author

Vikash Kumar