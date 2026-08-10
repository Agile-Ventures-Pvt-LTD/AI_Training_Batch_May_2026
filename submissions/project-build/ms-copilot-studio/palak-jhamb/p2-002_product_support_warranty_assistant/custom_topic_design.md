# Custom Topics

## 1. Guided Product Troubleshooting and Safety Triage

### Purpose
Provides safe, model-specific first-line troubleshooting for supported laptops and printers. It performs safety assessment before troubleshooting and escalates unresolved or unsafe cases.

### Triggers
Triggered by requests related to:
- General troubleshooting
- Power or charging problems
- Battery issues
- Display problems
- Wi-Fi/connectivity
- Printing or scanning
- Paper jams and print quality
- Error messages
- Overheating

### Inputs
- Product family and model
- Issue category and symptoms
- Power status
- Error code/message
- Issue start and frequency
- Previous troubleshooting
- Physical or liquid damage
- Safety indicators
- Customer willingness to continue

### Key Variables
`ProductFamily`, `ProductModel`, `IssueCategory`, `SymptomDescription`, `PowerStatus`, `ErrorCode`, `IssueStart`, `IssueFrequency`, `AttemptedSteps`, `PhysicalDamage`, `LiquidExposure`, `SafetyIndicator`, `SafetyLevel`, `TroubleshootingStepCount`, `TroubleshootingResolved`, `EscalationLevel`, `CaseSummaryConfirmed`.

### Entities
Uses multiple-choice entities for structured values such as product family, product model, issue category, safety responses, and Yes/No decisions.

### Validation & Conditions
- Validates supported product family and model.
- Prevents model-specific guidance when the model is unsupported or unknown.
- Checks safety before technical troubleshooting.
- Routes laptop queries to Lenovo knowledge and printer queries to HP knowledge.
- Checks resolution after troubleshooting steps.

### Loops
Troubleshooting continues only within a defined attempt limit. The loop stops when the issue is resolved, the customer cancels, a safety risk appears, or the maximum troubleshooting attempts are reached; completed steps should not be repeated.

### Redirects / Subtopics
**Product Safety Assessment** – Called before normal troubleshooting to classify the case as safe or safety-critical.

**Support Case Summary** – Produces a structured final case summary and allows customer confirmation or correction.

### Knowledge Sources
- Lenovo PDF User Guide
- Lenovo official website
- HP PDF User Guide
- HP official website
- NovaRetail Product Support Scope
- NovaRetail Product Safety and Escalation Policy

### Outcomes
- Resolved through self-service
- Human technical-support review required
- Warranty assessment recommended
- Unsupported product escalation
- Safety-critical escalation
- Cancelled by customer

### Escalation
- **Level 2:** Unresolved technical troubleshooting
- **Level 4:** Safety-critical condition requiring immediate safety guidance and urgent human support

### Cancellation
The customer may stop troubleshooting at any time. The flow stops safely without continuing technical steps.

### Limitations
No remote access, physical repair, dismantling instructions, unsafe procedures, unsupported model-specific guidance, claims of completed repair, or indefinite troubleshooting.

---

## 2. Warranty Eligibility and Service Route Assessment

### Purpose
Provides a structured preliminary assessment of whether an issue may fall within the NovaCare warranty policy and determines an appropriate service route. It does not make final warranty decisions.

### Triggers
Triggered by questions about:
- Warranty coverage and duration
- Repair or replacement eligibility
- Product damage
- Missing invoices
- Battery/accessory coverage
- Consumables
- Dead-on-arrival (DOA)
- Warranty exclusions

### Inputs
- Product family and model
- Item category
- Purchase and delivery dates
- NovaRetail purchase status
- Invoice and serial-number availability
- Issue category and operational status
- Damage indicators
- Unauthorised repair/modification
- Consumable involvement
- Seven-day reporting status
- Troubleshooting status
- Previous repairs
- Customer disagreement

### Key Variables
`WarrantyProductFamily`, `WarrantyProductModel`, `ItemCategory`, `PurchaseDate`, `DeliveryDate`, `PurchasedFromNovaRetail`, `InvoiceAvailable`, `SerialAvailable`, `ProductAgeInMonths`, `IssueCategory`, `ProductOperational`, `AccidentalDamage`, `LiquidDamage`, `ElectricalSurge`, `UnauthorizedRepair`, `UnauthorizedModification`, `ConsumableItem`, `ReportedWithinSevenDays`, `TroubleshootingCompleted`, `PreviousRepairCount`, `SafetyOverride`, `WarrantyClassification`, `ServiceRoute`, `CustomerDisputesResult`, `AssessmentConfirmed`.

### Entities
Uses structured multiple-choice/Yes-No entities for product family, item category, damage indicators, troubleshooting status, warranty classification, service route, and confirmation responses.

### Validation
- Purchase date cannot be in the future.
- Delivery date cannot precede purchase date.
- Product family/model is validated where possible.
- Item category must be valid.
- Required Yes/No information is captured.
- Product age is calculated consistently.
- Correct coverage period is selected.
- Missing information is identified before classification.
- Full serial numbers are not required in screenshots/documentation.

### Conditions

**Coverage:**
- Laptop/Printer → 12 months
- Bundled laptop battery → 6 months
- Bundled accessory → 6 months
- Toner/paper/consumables → Not covered under standard warranty

**DOA Assessment:**
Checks NovaRetail purchase, seven-day reporting period, product operation, damage indicators, proof of purchase, and safety override.

**Exclusions:**
Checks accidental/liquid/fire damage, electrical surge, misuse, unauthorised repair/modification, cosmetic damage, normal wear, software-only issues, malware, data loss, and consumables.

**Repeat Repair:**
Repeated same-issue repairs are routed for Level 3 human review without guaranteeing replacement.

### Loops / Corrections
If the customer identifies incorrect information, affected variables are updated and relevant validation, product-age calculation, coverage, exclusions, and classification logic are re-evaluated before generating an updated summary.

### Redirects
If approved troubleshooting is incomplete and the case is safe:

`Warranty Assessment → Guided Product Troubleshooting and Safety Triage → Receive Result → Resume Warranty Assessment`

Available product and issue information is passed where possible to avoid repeated questions. Safety-critical cases bypass normal troubleshooting.

### Knowledge Sources
- NovaCare Limited Warranty Policy
- NovaRetail Product Safety and Escalation Policy
- NovaRetail Product Support Scope
- Official Lenovo documentation
- Official HP documentation

### Outcomes / Classifications
- Potentially covered
- Potential dead-on-arrival assessment
- Potentially excluded
- Outside standard coverage
- Insufficient information
- Human review required
- Safety-critical escalation

### Escalation
- **Level 2:** Technical-support review where troubleshooting remains unresolved
- **Level 3:** Warranty ambiguity, exclusion, repeat repair, or unresolved customer dispute
- **Level 4:** Safety-critical condition requiring urgent escalation

### Cancellation
The customer may cancel the assessment. No final warranty decision or transaction is claimed when the flow is cancelled.

### Limitations
The topic cannot finally approve/reject warranty claims, guarantee repair/replacement, create cases, access a live warranty database, provide repair status, or make legal conclusions.

---
