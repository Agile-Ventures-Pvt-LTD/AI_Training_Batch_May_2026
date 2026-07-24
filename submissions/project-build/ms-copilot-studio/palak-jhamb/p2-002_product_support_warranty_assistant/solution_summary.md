# Solution Summary

## 1. Business Problem

NovaRetail Technologies requires a reliable customer-support solution for customers who need help with laptop and printer issues, product safety concerns, and warranty-related questions.

Customers may struggle to identify the correct troubleshooting steps, understand warranty coverage, recognise safety-critical situations, or determine the appropriate support route. The **NovaCare Product Support and Warranty Assistant** addresses this by providing source-grounded product support, safe first-line troubleshooting, preliminary warranty assessments, and structured escalation while ensuring that final warranty decisions remain with authorised human representatives.

---

## 2. Users

The primary users of the solution are:

- NovaRetail customers seeking product support.
- Customers experiencing laptop or printer problems.
- Customers seeking warranty coverage information.
- Customers requiring guided first-line troubleshooting.
- Customers reporting damaged, unsafe, or potentially defective products.
- Customers who need technical, warranty, repeat-repair, or safety escalation.

The assistant is designed to provide clear, professional, concise, and safety-conscious guidance without requiring unnecessary sensitive information.

---

## 3. Product Portfolio

The assistant provides model-specific support for the following products:

| Product Family | Supported Product | Support Scope |
|---|---|---|
| Laptop | Lenovo ThinkPad E14 Gen 5 | Setup, power, charging, battery, display, keyboard, touchpad, Wi-Fi, ports, external display, and overheating |
| Printer | HP LaserJet Pro MFP M428-M429 | Setup, printing, scanning, connectivity, paper loading, paper jams, print quality, toner, maintenance, and error messages |
| Laptop Accessory | Bundled charger | Connection, power delivery, and visible-damage assessment |
| Printer Accessory | Bundled power cable | Connection and visible-damage assessment |

For unsupported or unidentified models, the assistant does not invent model-specific guidance. It communicates the limitation and provides an appropriate support or escalation route.

---

## 4. Solution Scope

The NovaCare Product Support and Warranty Assistant supports:

- Product identification and model validation.
- Product information for supported devices.
- Safe first-line troubleshooting.
- Laptop and printer issue diagnosis.
- Product safety assessment and triage.
- Preliminary warranty eligibility assessment.
- Warranty coverage-period evaluation.
- Dead-on-arrival (DOA) assessment guidance.
- Warranty exclusion identification.
- Repeat-repair identification and escalation.
- Cross-topic troubleshooting and warranty workflows.
- Structured support case summaries.
- Customer correction and reassessment.
- Appropriate human-support escalation.

The solution does not perform physical repairs, remote device access, final warranty decisions, claim submission, or unsupported product-specific diagnosis.

---

## 5. Core Capabilities

### Product Support

The assistant identifies the product family and model before providing model-specific guidance. Technical responses are grounded in the appropriate official Lenovo or HP documentation.

### Guided Troubleshooting

The assistant provides controlled, safe, first-line troubleshooting for supported laptop and printer issues.

It tracks troubleshooting attempts, avoids repeating completed steps, checks whether the issue has been resolved, and stops when:

- The issue is resolved.
- The customer cancels.
- A safety concern is detected.
- The maximum troubleshooting limit is reached.

Unresolved cases are escalated to human technical support.

### Safety Triage

Safety is evaluated before normal troubleshooting.

The assistant identifies conditions such as smoke, sparks, fire, burning smell, electric shock, excessive heat, swollen batteries, liquid exposure, exposed wiring, or melting components.

Safety-critical cases immediately stop normal troubleshooting and are assigned urgent Level 4 escalation.

### Preliminary Warranty Assessment

The assistant evaluates:

- Product and item category.
- Purchase and delivery dates.
- Product age.
- Purchase from NovaRetail.
- Invoice and serial-number availability.
- Applicable coverage period.
- Damage and exclusion indicators.
- Consumable involvement.
- DOA conditions.
- Troubleshooting status.
- Previous repair history.

Possible classifications include:

- Potentially covered.
- Potential dead-on-arrival assessment.
- Potentially excluded.
- Outside standard coverage.
- Insufficient information.
- Human review required.
- Safety-critical escalation.

All classifications are preliminary.

### Escalation

The solution supports structured escalation routes including:

- Self-service information.
- Technical-support review.
- Warranty specialist review.
- Repeat-repair review.
- Paid-support review.
- Safety-critical escalation.
- Additional information required.

---

## 6. Knowledge Architecture

The solution uses a controlled knowledge architecture combining NovaRetail-authored policies with official manufacturer documentation.

### NovaRetail Knowledge Sources

1. **NovaCare Limited Warranty Policy**
   - Warranty periods and eligibility.
   - Warranty exclusions.
   - DOA assessment rules.
   - Documentation requirements.
   - Warranty decision boundaries.

2. **NovaRetail Product Support Scope**
   - Supported products and models.
   - Supported troubleshooting categories.
   - Product identification requirements.
   - Unsupported-product handling.

3. **NovaRetail Product Safety and Escalation Policy**
   - Safety-critical indicators.
   - Mandatory safety behaviour.
   - Escalation levels.
   - Urgent escalation requirements.

### Manufacturer Knowledge Sources

4. **Lenovo ThinkPad E14 Gen 5 and ThinkPad E16 Gen 1 User Guide**
   - Primary technical source for supported laptop troubleshooting.

5. **Lenovo Official Online User Guide**
   - Secondary source for laptop setup, operation, and troubleshooting.

6. **HP LaserJet Pro MFP M329, M428-M429 User Guide**
   - Primary technical source for supported printer troubleshooting.

7. **HP Official Setup and User Guides**
   - Secondary printer source where reliable website indexing is available.

### Knowledge Precedence

For product troubleshooting:

**Official Product Manual PDF → Official Manufacturer Website → Product Support Scope**

For warranty decisions:

**NovaCare Limited Warranty Policy → Product Safety and Escalation Policy → Relevant Manufacturer Information**

For safety:

**Product Safety and Escalation Policy → Official Manufacturer Safety Guidance → Human Escalation**

The assistant does not invent missing specifications, error-code meanings, policy rules, or troubleshooting procedures.

---

## 7. Topics

### Guided Product Troubleshooting and Safety Triage

Provides safe, model-specific troubleshooting for supported laptops and printers while checking safety conditions before technical steps are provided.

The topic captures product and issue information, invokes safety assessment, selects product-specific knowledge, controls troubleshooting attempts, avoids repeated instructions, and escalates unresolved cases.

### Warranty Eligibility and Service Route Assessment

Provides a structured preliminary warranty assessment based on the NovaCare Limited Warranty Policy.

The topic evaluates product age, applicable coverage periods, proof-of-purchase information, damage and exclusions, DOA conditions, troubleshooting completion, safety, and previous repairs before assigning a preliminary classification and service route.

### Reusable Subtopics

#### Product Safety Assessment

Centralises safety logic so it can be reused across support workflows.

It classifies cases as safe to continue or safety-critical and assigns Level 4 escalation where required.

#### Support Case Summary

Creates a structured summary containing product details, issue information, safety classification, troubleshooting performed, outcome, escalation level, and recommended next action.

The customer can confirm or correct the captured information.

---

## 8. Safety Controls

Safety is treated as a higher priority than normal troubleshooting or warranty processing.

The solution:

- Performs safety assessment before technical troubleshooting.
- Detects smoke, sparks, fire, burning smell, electric shock, excessive heat, battery swelling, liquid exposure, exposed wiring, and similar hazards.
- Stops normal troubleshooting when a safety-critical condition is detected.
- Does not ask customers to reproduce unsafe conditions.
- Does not instruct customers to dismantle products.
- Does not recommend bypassing built-in product protections.
- Does not instruct customers to restart, charge, or continue using an unsafe product.
- Advises disconnection from power only when safe.
- Prioritises immediate safety guidance.
- Assigns Level 4 escalation to safety-critical cases.
- Directs customers to urgent human support when required.

Safety-critical classification overrides normal troubleshooting and warranty processing.

---

## 9. Decision Boundaries

The assistant operates within clearly defined decision boundaries.

### Warranty Decisions

All warranty assessments are **preliminary**.

The assistant must not:

- Finally approve a warranty claim.
- Finally reject a warranty claim.
- Guarantee repair.
- Guarantee replacement.
- Guarantee DOA replacement.
- Provide a legal conclusion.

Final warranty approval, rejection, repair, replacement, or commercial settlement requires validation by an authorised human representative.

### System and Transaction Boundaries

Unless an actual integration is configured, the assistant must not claim:

- A warranty claim has been submitted.
- A repair has been booked.
- A replacement has been approved.
- Access to a live warranty database.
- Access to repair status.
- Access to inventory.
- Access to customer order history.
- Access to payment records.

### Technical Boundaries

The assistant does not:

- Perform remote access.
- Perform physical repair.
- Request product dismantling.
- Recommend unauthorised procedures.
- Invent model-specific instructions.
- Interpret unsupported error codes.
- Continue troubleshooting indefinitely.

### Privacy Boundaries

The assistant does not request or disclose:

- Passwords.
- Banking information.
- Encryption keys.
- Full payment-card details.
- Real customer records.
- Unrelated personal files.
- Unnecessary sensitive information.

Only information required for support or preliminary warranty assessment should be collected.

---

## 10. Implementation Decisions

### Microsoft Copilot Studio

The solution is implemented using **Microsoft Copilot Studio**, using topics, variables, conditions, knowledge sources, generative answers, redirections, and escalation logic.

### Structured Topics Instead of Fully Generative Flows

Critical processes such as safety assessment and warranty classification use structured topic logic rather than relying entirely on generative responses.

This provides greater control over:

- Safety decisions.
- Coverage periods.
- Warranty classifications.
- Troubleshooting limits.
- Escalation routes.
- Customer correction flows.

### Product-Specific Grounding

Technical guidance is separated by product:

- Lenovo sources are used for Lenovo laptop troubleshooting.
- HP sources are used for HP printer troubleshooting.

This reduces the risk of cross-product retrieval and unsupported instructions.

### Reusable Safety Logic

The **Product Safety Assessment** is implemented as a reusable subtopic instead of duplicating complete safety logic across multiple topics.

This provides consistent safety classification and escalation behaviour.

### Controlled Troubleshooting

Troubleshooting uses a limited-attempt approach.

The implementation tracks completed steps and troubleshooting attempts to:

- Avoid repeating instructions.
- Stop when resolved.
- Stop when cancelled.
- Stop when unsafe.
- Escalate after the configured maximum.

### Cross-Topic Redirection

When warranty assessment identifies that approved troubleshooting has not been completed and the case is safe, the customer can be redirected to **Guided Product Troubleshooting and Safety Triage**.

Available product and issue information is reused where possible to avoid unnecessary repeated questions, after which the warranty assessment can continue.

### Deterministic Warranty Logic

Warranty periods are applied according to item category:

| Item Category | Coverage |
|---|---|
| Laptop | 12 months |
| Printer | 12 months |
| Bundled laptop battery | 6 months |
| Bundled accessory | 6 months |
| Printer toner, paper, or consumables | Not covered under standard warranty |

Purchase and delivery dates are validated before classification, and product age is calculated consistently.

### Safety Override

Safety-critical conditions override normal warranty and troubleshooting logic.

A safety-critical case is routed directly to immediate safety guidance and urgent escalation rather than continuing through routine technical or warranty assessment.


## Summary

The **NovaCare Product Support and Warranty Assistant** combines grounded knowledge retrieval, structured conversational workflows, safety-first controls, model-specific troubleshooting, and deterministic preliminary warranty logic.

The solution automates routine customer-support guidance while maintaining clear boundaries around safety, privacy, unsupported information, and final warranty decisions. Cases requiring judgement, specialist review, or urgent intervention are escalated to the appropriate human-support route.