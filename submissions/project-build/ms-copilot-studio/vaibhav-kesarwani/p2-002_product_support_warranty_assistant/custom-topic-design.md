# Custom Topic Design

This document describes the custom topics and reusable subtopics implemented in the **NovaRetail Product Support & Warranty Assistant**. It outlines the purpose, conversation flow, variables, validation logic, decision conditions, knowledge sources, escalation rules, and expected outcomes for each topic.

---

# Custom Topic 1: Guided Product Troubleshooting and Safety Triage

## Purpose

Guide customers through safe, structured, first-line troubleshooting for supported Lenovo laptops and HP printers. The topic ensures mandatory safety assessment before troubleshooting and provides model-specific guidance using approved knowledge sources.

---

## Trigger Intent

The topic is triggered by requests related to:

- General troubleshooting
- Laptop problems
- Printer problems
- No power
- Charging problems
- Battery issues
- Blank display and **more...**

---

## Validation

The topic validates:

- Supported product family
- Supported product model
- Mandatory issue information
- Safety status before troubleshooting
- Required troubleshooting information

Unsupported models follow the escalation path without providing model-specific guidance.

---

## Conditions

- Safety-critical vs safe condition
- Laptop vs printer
- Supported vs unsupported product
- Issue category selection
- Troubleshooting resolved vs unresolved
- Maximum troubleshooting attempts reached
- Customer correction
- Customer cancellation

---

## Troubleshooting Loop

The troubleshooting workflow:

- Tracks completed troubleshooting steps.
- Tracks the troubleshooting attempt count.
- Prevents repeated troubleshooting instructions.
- Stops immediately when:
  - The issue is resolved.
  - The customer cancels.
  - A safety issue is detected.
  - The maximum troubleshooting limit is reached.
- Escalates unresolved issues after the defined attempt limit.

---

## Redirects

The topic redirects to:

### Product Safety Assessment

Performs mandatory safety evaluation before troubleshooting.

### Support Case Summary

Generates the final troubleshooting summary and allows customer confirmation or correction.

---

## Knowledge Sources

Uses:

- Lenovo User Manuals
- HP User Manual
- Lenovo Online User Guides
- HP Online User Guides

Model-specific responses are restricted to the appropriate manufacturer documentation.

---

## Topic Outcomes

- Self-service resolution
- Technical support review
- Warranty assessment recommended
- Unsupported product escalation
- Safety-critical escalation
- Customer cancelled

---

## Escalation Rules

Escalate when:

- Safety-critical condition detected
- Unsupported product
- Maximum troubleshooting attempts reached
- Troubleshooting unsuccessful
- Customer requests escalation

---

## Cancellation

Customers may cancel troubleshooting at any time.

The topic terminates gracefully without continuing troubleshooting.
---

# Custom Topic 2: Warranty Eligibility and Service Route Assessment

## Purpose

Perform a structured preliminary warranty eligibility assessment using the NovaCare Limited Warranty Policy and recommend the appropriate service route.

The assessment is informational only and does not constitute final warranty approval.

---

## Trigger Intent

The topic is triggered by requests related to:

- Warranty coverage
- Warranty duration
- Warranty eligibility
- Repair eligibility
- Replacement eligibility and **more...**
---

## Validation

The topic validates:

- Purchase date
- Delivery date
- Supported product family
- Supported model
- Item category
- Warranty age calculation
- Coverage period
- Required Yes/No responses
- Missing mandatory information

Invalid information is requested again before continuing.

---

## Conditions

The topic evaluates:

- Coverage period
- Product age
- Dead-on-arrival eligibility
- Warranty exclusions
- Repeat repair
- Consumable coverage
- Customer disagreement
- Safety override
- Missing information

---

## Redirects

If approved troubleshooting has not been completed and the product is safe:

Redirect to:

**Guided Product Troubleshooting and Safety Triage**

Pass:

- Product Family
- Product Model
- Issue Category

Resume the warranty assessment after troubleshooting completes.

Previously collected information is reused.

---

## Knowledge Sources

Uses:

- NovaCare Limited Warranty Policy
- Product Support Scope
- Product Safety and Escalation Policy

Warranty decisions are based only on NovaRetail policy documents.

Technical information continues to use official Lenovo and HP documentation.
---

## Cancellation

Customers may cancel the warranty assessment at any point.

The conversation ends without generating a final assessment.

---

## Limitations

- Provides only preliminary warranty guidance.
- Does not approve or reject warranty claims.
- Does not guarantee repair or replacement.
- Does not submit warranty requests.
- Does not access live warranty databases.
- Does not access repair tracking systems.
- Uses only configured NovaRetail policy documents.

---

# Reusable Subtopic 1: Product Safety Assessment

## Purpose

Evaluate safety risks before troubleshooting and determine whether troubleshooting can continue safely.

---

## Inputs

- Product Family
- Safety Indicators
- Physical Damage
- Liquid Exposure

---

## Variables

- SafetyIndicator
- SafetyLevel
- EscalationLevel

---

## Validation

Checks all mandatory safety indicators.

---

## Conditions

- Safe to continue
- Safety-critical

---

## Outcomes

- Continue troubleshooting
- Immediate Level 4 escalation

---

## Knowledge Source

Product Safety and Escalation Policy

---

## Limitations

Stops troubleshooting immediately for safety-critical conditions.

---

# Reusable Subtopic 2: Support Case Summary

## Purpose

Generate a structured summary of troubleshooting or warranty assessment before ending the conversation.

---

## Inputs

- Product details
- Issue details
- Troubleshooting outcome
- Warranty assessment
- Escalation level

---

## Variables

Uses previously collected topic variables.

---

## Validation

Allows the customer to review and correct captured information.

---

## Outcomes

- Confirm summary
- Update information
- Regenerate summary
- Complete topic

---

## Knowledge Sources

Uses the information collected during the conversation and applicable policy documents.

---

## Limitations

Does not modify warranty decisions independently and cannot submit support requests.