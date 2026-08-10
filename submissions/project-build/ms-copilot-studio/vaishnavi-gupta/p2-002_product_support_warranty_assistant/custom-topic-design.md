# Custom Topic Design

## Project Information

| Field | Details |
|--------|----------|
| **Project ID** | P2-002 |
| **Project Name** | Product Support and Warranty Assistant |
| **Platform** | Microsoft Copilot Studio |
| **Version** | 1.0 |

---

# Overview

The chatbot implements two primary custom topics and two reusable subtopics to provide structured, safe, and policy-compliant customer support. Each topic follows a guided workflow with validation, branching, escalation, and completion logic.

---

# Topic 1 – Guided Product Troubleshooting and Safety Triage

## Purpose

Guide customers through safe, model-specific troubleshooting for supported Lenovo laptops and HP printers while ensuring that safety checks are completed before technical guidance.

---

## Trigger Categories

The topic is triggered for requests related to:

- Laptop not working
- Printer not working
- Device won't turn on
- Charging issues
- Battery problems
- Blank display
- Wi-Fi issues
- Keyboard or touchpad issues
- Printer offline
- Paper jam
- Poor print quality
- Scan failures
- Toner warnings
- Error messages
- Power issues
- Connectivity problems

---

## Variables

- ProductFamily
- ProductModel
- IssueCategory
- SymptomDescription
- PowerStatus
- ErrorCode
- IssueStart
- IssueFrequency
- AttemptedSteps
- PhysicalDamage
- LiquidExposure
- SafetyIndicator
- SafetyLevel
- TroubleshootingStepCount
- TroubleshootingResolved
- EscalationLevel
- CaseSummaryConfirmed

---

## Workflow

1. Identify product family.
2. Validate supported model.
3. Collect issue details.
4. Redirect to **Product Safety Assessment**.
5. If safe, continue troubleshooting.
6. Route to Laptop or Printer branch.
7. Generate grounded troubleshooting response.
8. Ask if the issue is resolved.
9. Repeat until resolved or maximum attempts reached.
10. Generate Support Case Summary.
11. Complete or escalate.

---

## Decision Logic

- Supported product → Continue.
- Unsupported product → Human support recommendation.
- Safety detected → Stop troubleshooting.
- Issue resolved → End conversation.
- Maximum attempts reached → Technical support escalation.

---

## Controlled Troubleshooting Loop

The workflow:

- Tracks completed steps.
- Prevents repeated instructions.
- Stops after three attempts.
- Stops when customer cancels.
- Stops immediately for safety-critical cases.
- Escalates unresolved cases.

---

## Outcomes

- Self-service resolution
- Human technical support
- Warranty assessment recommended
- Unsupported product escalation
- Safety-critical escalation
- Customer cancelled

---

# Topic 2 – Warranty Eligibility and Service Route Assessment

## Purpose

Provide a preliminary warranty assessment based on NovaCare policy and recommend the appropriate service route.

---

## Trigger Categories

- Warranty
- Coverage
- Warranty expired
- Repair eligibility
- Replacement
- Product damaged
- Battery warranty
- Accessory warranty
- Consumables
- Missing invoice
- Dead-on-arrival
- Warranty claim
- Warranty dispute

---

## Variables

- WarrantyProductFamily
- WarrantyProductModel
- ItemCategory
- PurchaseDate
- DeliveryDate
- PurchasedFromNovaRetail
- InvoiceAvailable
- SerialAvailable
- ProductAgeInMonths
- IssueCategory
- ProductOperational
- AccidentalDamage
- LiquidDamage
- ElectricalSurge
- UnauthorizedRepair
- UnauthorizedModification
- ConsumableItem
- ReportedWithinSevenDays
- TroubleshootingCompleted
- PreviousRepairCount
- SafetyOverride
- WarrantyClassification
- ServiceRoute
- CustomerDisputesResult
- AssessmentConfirmed

---

## Workflow

1. Collect warranty information.
2. Validate dates and required fields.
3. Calculate product age.
4. Apply warranty period.
5. Redirect to troubleshooting if required.
6. Evaluate exclusions.
7. Evaluate Dead-on-Arrival conditions.
8. Evaluate repeat repairs.
9. Determine preliminary classification.
10. Recommend service route.
11. Generate completion summary.
12. Customer confirmation.

---

## Warranty Classification

Possible classifications:

- Potentially Covered
- Potential Dead-on-Arrival Assessment
- Potentially Excluded
- Outside Standard Coverage
- Human Review Required
- Insufficient Information
- Safety-Critical Escalation

---

## Service Routes

- Self-Service Information
- Technical Support Review
- Warranty Specialist Review
- Repeat Repair Review
- Paid Support Review
- Safety-Critical Escalation
- Additional Information Required

---

## Decision Logic

- Valid warranty period → Potentially Covered.
- Exclusion detected → Potentially Excluded.
- DOA criteria satisfied → Potential DOA Assessment.
- Missing information → Insufficient Information.
- Repeat repair → Level 3 Escalation.
- Safety detected → Safety-Critical Escalation.

---

# Reusable Subtopic – Product Safety Assessment

## Purpose

Evaluate mandatory safety indicators before troubleshooting.

---

## Safety Checks

- Smoke
- Fire
- Sparks
- Burning smell
- Electric shock
- Swollen battery
- Excessive heat
- Liquid ingress
- Exposed wiring
- Melting components

---

## Outputs

- SafetyLevel
- EscalationLevel
- Continue / Stop Decision

---

## Behaviour

If a safety-critical condition is detected:

- Stop troubleshooting.
- Advise the customer to stop using the product.
- Recommend authorized support.
- Prevent further troubleshooting.

---

# Reusable Subtopic – Support Case Summary

## Purpose

Generate a structured summary before ending the conversation.

---

## Summary Includes

- Product family
- Product model
- Issue category
- Symptom
- Safety classification
- Troubleshooting performed
- Warranty classification
- Escalation level
- Recommended next action

---

## Customer Confirmation

Customers may:

- Confirm the summary.
- Correct incorrect information.
- Regenerate the summary.

---

# Cross-Topic Navigation

The chatbot supports topic redirection to avoid collecting duplicate information.

### Warranty → Troubleshooting

If troubleshooting has not been completed and no safety risk exists:

- Redirect to Guided Product Troubleshooting.
- Pass collected product and issue variables.
- Resume warranty assessment after troubleshooting.

### Troubleshooting → Warranty

If technical troubleshooting is complete but warranty guidance is requested:

- Redirect to Warranty Assessment.
- Reuse captured variables where applicable.

---

# Knowledge Sources Used

- Lenovo ThinkPad E14 Gen 5 User Guide
- Lenovo Support Website
- HP LaserJet Pro MFP M428-M429 User Guide
- HP Support Website
- NovaCare Limited Warranty Policy
- Product Support Scope
- Product Safety and Escalation Policy

---

# Escalation Strategy

Escalation occurs when:

- Safety-critical conditions are detected.
- Unsupported products are identified.
- Maximum troubleshooting attempts are reached.
- Repeat repair conditions exist.
- Customer disputes remain unresolved.
- Required information is missing.

---

# Cancellation Handling

The chatbot allows customers to cancel the conversation at any stage.

When cancelled:

- The workflow stops gracefully.
- No further troubleshooting is performed.
- The interaction is closed without additional actions.

---

# Design Principles

The custom topics were designed following these principles:

- Safety before troubleshooting
- Grounded responses using approved knowledge sources
- Reusable subtopics to reduce duplication
- Structured conversation flow
- Clear decision boundaries
- Minimal repeated questions
- Controlled troubleshooting loops
- Human escalation for complex scenarios
- Transparent warranty assessments

---

# Known Limitations

- Supports only configured Lenovo and HP models.
- No live warranty or CRM integration.
- Cannot create repair tickets.
- Cannot schedule technician visits.
- Cannot verify invoices or serial numbers.
- Does not approve or reject warranty claims.
- Does not provide legal or commercial decisions.

---

# Conclusion

The custom topic design provides a modular, maintainable, and enterprise-ready conversation architecture. By separating troubleshooting, warranty assessment, safety evaluation, and case summarization into reusable components, the chatbot delivers consistent, policy-compliant, and safe customer support while ensuring that final technical and warranty decisions remain with authorized human representatives.