# Custom Topic Design

## Overview

The NovaRetail Product Support & Warranty Assistant uses a modular topic architecture in Microsoft Copilot Studio. The design separates business workflows into main topics, reusable topics, and utility topics to improve maintainability, reusability, and consistency.

---

# Topic Architecture

```text
                    User
                      │
                      ▼
        ┌─────────────────────────────┐
        │      Main Topics            │
        └─────────────────────────────┘
          │                      │
          ▼                      ▼
Guided Product            Warranty Eligibility
Troubleshooting           & Service Route
& Safety Triage           Assessment
          │                      │
          └──────────┬───────────┘
                     ▼
         Product Safety Assessment
                     │
                     ▼
          Support Case Summary
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
 Human Escalation      Unsupported Product
                               │
                               ▼
                     Cancellation & Restart
```

---

# Topic Classification

| Category | Topic |
|----------|-------|
| Main Topic | Guided Product Troubleshooting and Safety Triage |
| Main Topic | Warranty Eligibility and Service Route Assessment |
| Main Topic *(Optional)* | Repair Escalation and Appointment Preparation |
| Reusable Topic | Product Safety Assessment |
| Reusable Topic | Support Case Summary |
| Utility Topic | Unsupported Product Handler |
| Utility Topic | Human Escalation |
| Utility Topic | Cancellation & Restart |

---

# Main Topic 1

## Guided Product Troubleshooting and Safety Triage

### Purpose

Provides guided troubleshooting for supported Lenovo laptops and HP printers while ensuring every interaction begins with a mandatory safety assessment.

### Trigger Examples

- My laptop won't turn on.
- My printer is offline.
- My laptop is overheating.
- My printer has a paper jam.
- Laptop battery issue.
- Printer printing blank pages.

### Inputs

- Product Family
- Product Model
- Issue Description

### Workflow

1. Collect product information.
2. Validate supported product.
3. Call **Product Safety Assessment**.
4. Stop workflow if safety issue detected.
5. Retrieve troubleshooting guidance.
6. Ask whether the issue is resolved.
7. Escalate if required.
8. Generate Support Case Summary.

### Outputs

- Troubleshooting guidance
- Safety status
- Escalation recommendation
- Case summary

---

# Main Topic 2

## Warranty Eligibility and Service Route Assessment

### Purpose

Performs a preliminary warranty assessment using the NovaCare Limited Warranty Policy.

### Trigger Examples

- Is my laptop under warranty?
- Can I claim warranty?
- My charger stopped working.
- My printer arrived damaged.

### Inputs

- Product Family
- Product Model
- Purchase Date
- Invoice Availability
- Issue Description

### Workflow

1. Validate supported product.
2. Call **Product Safety Assessment**.
3. Collect warranty information.
4. Check warranty policy.
5. Provide preliminary assessment.
6. Generate Support Case Summary.

### Outputs

- Preliminary warranty guidance
- Recommended next action
- Escalation recommendation

---

# Main Topic 3 (Optional)

## Repair Escalation and Appointment Preparation

### Purpose

Collects repair-related information and prepares a structured summary before the customer contacts human support.

### Inputs

- Product
- Issue Summary
- Previous Troubleshooting
- Safety Status
- Preferred Contact Method

### Outputs

- Appointment preparation summary
- Recommended escalation path

---

# Reusable Topic

## Product Safety Assessment

### Purpose

Checks for safety-critical conditions before troubleshooting or warranty assessment.

### Safety Checks

- Smoke
- Sparks
- Burning smell
- Electric shock
- Liquid exposure
- Excessive heat
- Swollen battery
- Physical damage

### Behaviour

If a safety issue is detected:

- Stop troubleshooting immediately.
- Advise the customer to stop using the device.
- Recommend contacting authorised support.
- Return the safety status to the calling topic.

---

# Reusable Topic

## Support Case Summary

### Purpose

Generates a structured summary of the interaction for customer confirmation and future reference.

### Summary Includes

- Product family
- Product model
- Issue description
- Safety assessment result
- Troubleshooting performed
- Warranty assessment
- Recommended next action

### Behaviour

- Display summary.
- Ask the customer to confirm.
- Return to the calling topic.

---

# Utility Topic

## Unsupported Product Handler

### Purpose

Handles products outside the supported scope.

### Behaviour

- Inform the customer that the product is unsupported.
- Offer an opportunity to re-enter the product model.
- Recommend contacting the manufacturer or authorised support.

---

# Utility Topic

## Human Escalation

### Purpose

Provides escalation guidance when automated support cannot resolve the issue.

### Escalation Conditions

- Safety-critical issue
- Unresolved troubleshooting
- Manual warranty review
- Customer requests human assistance
- Unsupported product

### Behaviour

- Explain why escalation is recommended.
- Provide next steps.
- Do not create support tickets or appointments.

---

# Utility Topic

## Cancellation & Restart

### Purpose

Allows customers to cancel, restart, or continue the conversation.

### Behaviour

- Confirm customer choice.
- Restart workflow if requested.
- End conversation if cancelled.
- Resume the current topic if continued.

---

# Variables Used

| Variable | Purpose |
|----------|---------|
| ProductFamily | Selected product category |
| ProductModel | Product model entered by customer |
| IssueDescription | Customer-reported issue |
| SafetyLevel | Safety assessment result |
| WarrantyStatus | Preliminary warranty outcome |
| TroubleshootingStatus | Whether the issue was resolved |
| RecommendedNextAction | Suggested next step |
| EscalationLevel | Escalation recommendation |
| SupportSummary | Final interaction summary |

---

# Design Principles

The topic architecture follows these principles:

- Modular conversation design.
- Reusable common workflows.
- Safety-first interaction.
- Knowledge-grounded responses.
- Clear separation of troubleshooting and warranty processes.
- Consistent escalation handling.
- No unsupported or fabricated guidance.

---

# Limitations

- Supports only products defined in the project scope.
- Does not integrate with CRM or ticketing systems.
- Does not create service requests.
- Does not schedule repair appointments.
- Does not make final warranty decisions.
- Relies entirely on configured knowledge sources for responses.