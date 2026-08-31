# Product Support & Warranty Assistant

## Platform

Microsoft Copilot Studio

## Current Scope

Lenovo ThinkPad E14 Gen 5 (Laptop Support Only)

---

# Topic Architecture

The assistant consists of two main topics and two reusable subtopics.

```
Main Topics
│
├── Guided Laptop Troubleshooting and Safety Triage
│
├── Warranty Eligibility and Service Route Assessment
│
Reusable Subtopics
│
├── Product Safety Assessment
│
└── Support Case Summary
```

---

# Main Topic 1

## Topic Name

Guided Laptop Troubleshooting and Safety Triage

### Purpose

Guide customers through safe, structured, model-specific troubleshooting for Lenovo ThinkPad E14 Gen 5 laptops while ensuring that safety risks are identified before technical guidance is provided.

---

## Trigger Phrases

Examples include:

- My laptop is not working
- Laptop won't turn on
- Charging problem
- Battery draining quickly
- Screen is blank
- Laptop overheating
- Wi-Fi not working
- Keyboard issue
- Touchpad problem
- Laptop troubleshooting
- Fix my laptop

---

## Required Inputs

- Product Family
- Product Model
- Issue Category
- Symptom Description
- Power Status
- Error Code
- Issue Start Time
- Issue Frequency
- Troubleshooting Already Attempted
- Customer Confirmation to Continue

---

## Variables

| Variable | Purpose |
|-----------|----------|
| ProductFamily | Store product type |
| ProductModel | Store laptop model |
| IssueCategory | Selected issue |
| SymptomDescription | User description |
| PowerStatus | Current power state |
| ErrorCode | Error message |
| IssueStart | Problem start time |
| IssueFrequency | Continuous or intermittent |
| AttemptedSteps | Previous troubleshooting |
| TroubleshootingStepCount | Loop counter |
| TroubleshootingResolved | Resolution status |
| EscalationLevel | Escalation priority |

---

## Entities

- Lenovo ThinkPad E14 Gen 5
- No Power
- Charging Failure
- Battery Issue
- Blank Display
- External Display
- Overheating
- Wi-Fi
- Keyboard
- Touchpad

---

## Validation Rules

- Product must be Lenovo ThinkPad E14 Gen 5.
- Issue category must be selected.
- Mandatory fields cannot be empty.
- Safety assessment must complete before troubleshooting.

---

## Decision Conditions

- Supported product?
- Safety critical?
- Issue category?
- Issue resolved?
- Maximum troubleshooting attempts reached?
- Customer wants to continue?

---

## Controlled Loop

The troubleshooting process repeats until one of the following occurs:

- Issue resolved
- Customer cancels
- Safety issue detected
- Maximum troubleshooting attempts reached

Maximum troubleshooting attempts:

3

---

## Redirects

Redirect to:

- Product Safety Assessment
- Support Case Summary
- Warranty Eligibility Assessment (if required)

---

## Knowledge Sources

- Lenovo Support Documentation
- Lenovo User Guide
- Lenovo Safety Documentation

---

## Possible Outcomes

- Resolved through self-service
- Technical support required
- Warranty assessment recommended
- Safety escalation
- Unsupported product
- Customer cancelled

---

## Escalation

Escalate when:

- Safety hazard detected
- Three troubleshooting attempts completed
- Unsupported issue
- Customer requests human support

---

## Cancellation

Conversation ends if the customer:

- Cancels troubleshooting
- Declines to continue
- Leaves the conversation

---

## Limitations

This topic:

- Supports only Lenovo ThinkPad E14 Gen 5.
- Does not provide printer troubleshooting.
- Does not perform remote support.
- Does not recommend hardware disassembly.

---

# Main Topic 2

## Topic Name

Warranty Eligibility and Service Route Assessment

### Purpose

Perform a preliminary warranty assessment and recommend an appropriate service route without making a final warranty decision.

---

## Trigger Phrases

Examples include:

- Check my warranty
- Is my laptop under warranty?
- Warranty claim
- Replacement eligibility
- Repair eligibility
- Warranty expired
- Battery warranty
- Accidental damage
- Invoice missing

---

## Required Inputs

- Product Model
- Purchase Date
- Delivery Date
- Invoice Available
- Serial Number Available
- Issue Category
- Product Operational Status
- Damage Information
- Previous Repairs
- Troubleshooting Status

---

## Variables

| Variable | Purpose |
|-----------|----------|
| PurchaseDate | Purchase date |
| DeliveryDate | Delivery date |
| InvoiceAvailable | Invoice status |
| SerialAvailable | Serial number availability |
| ProductAge | Warranty age |
| WarrantyClassification | Assessment result |
| ServiceRoute | Recommended route |
| PreviousRepairCount | Repair history |
| AssessmentConfirmed | Customer confirmation |

---

## Entities

- Warranty
- Invoice
- Serial Number
- Purchase Date
- Product Age
- Damage Type
- Service Route

---

## Validation Rules

- Purchase date cannot be in the future.
- Delivery date cannot precede purchase date.
- Supported product required.
- Mandatory Yes/No questions answered.
- Missing information identified before classification.

---

## Decision Conditions

- Within warranty period?
- Dead-on-arrival?
- Exclusion applies?
- Troubleshooting completed?
- Customer disputes assessment?

---

## Controlled Loop

If information changes:

- Recalculate assessment.
- Update service route.
- Regenerate summary.

---

## Redirects

Redirect to:

- Guided Laptop Troubleshooting (if troubleshooting not completed)
- Product Safety Assessment (if safety concern identified)
- Support Case Summary

---

## Knowledge Sources

- NovaCare Warranty Policy
- Lenovo Warranty Documentation
- Lenovo Support Documentation

---

## Possible Outcomes

- Potentially Covered
- Outside Standard Warranty
- Potential Dead-on-Arrival
- Potential Exclusion
- Human Review Required
- Safety Escalation

---

## Escalation

Escalate when:

- Safety issue detected
- Repeat repair identified
- Human warranty review required
- Customer disputes assessment after correction

---

## Cancellation

Conversation ends if the customer:

- Cancels the assessment
- Declines to continue

---

## Limitations

The assistant:

- Does not approve warranty claims.
- Does not reject warranty claims.
- Does not access live warranty systems.
- Does not promise repair or replacement.

---

# Reusable Subtopic 1

## Topic Name

Product Safety Assessment

### Purpose

Identify safety-critical situations before troubleshooting begins.

### Inputs

- Smoke
- Sparks
- Burning Smell
- Electric Shock
- Swollen Battery
- Liquid Exposure
- Excessive Heat

### Outputs

- Safe to Continue
- Safety Critical
- Escalation Level

### Outcome

If safety critical:

- Stop troubleshooting
- Display safety guidance
- Escalate immediately

---

# Reusable Subtopic 2

## Topic Name

Support Case Summary

### Purpose

Generate a structured summary of the customer interaction.

### Summary Includes

- Product Model
- Issue Category
- Troubleshooting Performed
- Safety Classification
- Warranty Classification
- Service Route
- Recommended Next Action

### Customer Actions

- Confirm Summary
- Correct Information

### Outputs

- Final Summary
- Updated Summary
- Conversation Completion

---

# Overall Conversation Flow

```
Customer

↓

Product Validation

↓

Product Safety Assessment

↓

Guided Laptop Troubleshooting

↓

Issue Resolved?

├── Yes → Support Case Summary → End

└── No

↓

Warranty Eligibility Assessment

↓

Service Route

↓

Support Case Summary

↓

End Conversation
```

---

# Current Implementation Limitations

- Supports only Lenovo ThinkPad E14 Gen 5.
- Printer support is not implemented.
- No CRM integration.
- No live warranty verification.
- No service ticket creation.
- No remote diagnostics.
- No voice interaction.
- No Power Automate integration.

---

**Document Version:** 1.0  
**Project:** Product Support & Warranty Assistant  
**Platform:** Microsoft Copilot Studio