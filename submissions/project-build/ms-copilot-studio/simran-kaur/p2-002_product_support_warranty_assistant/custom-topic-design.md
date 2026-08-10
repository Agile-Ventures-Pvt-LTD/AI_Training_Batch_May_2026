
# Custom Topic Design Document

## 1. Topic: Guided Product Troubleshooting and Safety Triage

### Purpose
Provides safe, model-specific troubleshooting support for NovaRetail laptops and printers. Identifies products, checks safety risks, provides approved guidance, and escalates unresolved cases.

### Triggers
- Laptop troubleshooting requests
- Printer issues
- Power, charging, battery, display problems
- Connectivity, printing, scanning issues
- Error messages

### Inputs
- Product family and model
- Issue category
- Symptoms
- Power status
- Error message/code
- Issue start date
- Previous troubleshooting steps
- Physical damage/liquid exposure
- Safety indicators

### Variables
- ProductFamily
- ProductModel
- IssueCategory
- SymptomDescription
- SafetyIndicator
- SafetyLevel
- TroubleshootingStepCount
- TroubleshootingResolved
- EscalationLevel
- CaseSummaryConfirmed

### Entities
- Product Family: Laptop, Printer, Accessory
- Issue Category
- Yes/No responses for validation

### Validation
- Confirm supported product model.
- Prevent model-specific guidance for unknown products.
- Check safety conditions before troubleshooting.

### Conditions
- Safety risk detected → Stop troubleshooting and escalate Level 4.
- Issue resolved → Generate case summary.
- Maximum attempts reached → Escalate technical support.

### Loop Handling
- Tracks completed troubleshooting steps.
- Prevents repeated instructions.
- Stops when resolved, cancelled, unsafe, or maximum attempts reached.

### Knowledge Sources
- Lenovo ThinkPad E14/E16 User Guide
- Lenovo Support Website
- HP LaserJet Pro M428-M429 User Guide
- HP Support Website

### Outcomes
- Self-service resolution
- Technical support escalation
- Warranty assessment recommended
- Safety escalation
- Unsupported product escalation

---

# 2. Topic: Warranty Eligibility and Service Route Assessment

### Purpose
Provides preliminary warranty assessment using NovaCare warranty rules. It identifies possible coverage and service routes without making final decisions.

### Triggers
- Warranty coverage questions
- Repair/replacement queries
- Damage assessment
- Battery/accessory coverage
- Invoice issues
- Dead-on-arrival queries

### Inputs
- Product/model
- Purchase date
- Delivery date
- Invoice availability
- Serial availability
- Issue category
- Damage indicators
- Previous repairs
- Troubleshooting status

### Variables
- WarrantyProductModel
- ItemCategory
- PurchaseDate
- ProductAgeInMonths
- AccidentalDamage
- LiquidDamage
- ConsumableItem
- WarrantyClassification
- ServiceRoute
- AssessmentConfirmed

### Validation
- Reject future purchase dates.
- Validate supported products.
- Calculate warranty period correctly.
- Identify missing information.

### Conditions

| Condition | Result |
|---|---|
| Within warranty + manufacturing issue | Potentially covered |
| Within 7 days + hardware failure | Potential DOA assessment |
| Damage/exclusion found | Potentially excluded |
| Outside coverage period | Outside standard coverage |
| Missing details | Insufficient information |

### Cross Topic Redirect
If troubleshooting is incomplete:

Warranty Topic → Troubleshooting Topic → Return assessment with captured information.

### Knowledge Sources
- NovaCare Limited Warranty Policy
- Product Safety and Escalation Policy
- Product Support Scope

### Outcomes
- Potentially covered
- Potential DOA assessment
- Potentially excluded
- Human review required
- Safety escalation

---

# 3. Reusable Subtopic: Product Safety Assessment

### Purpose
Checks safety conditions before troubleshooting.

### Inputs
- Smoke
- Fire
- Sparks
- Burning smell
- Electric shock
- Battery swelling
- Liquid exposure

### Logic
Safety risk detected:
→ Stop troubleshooting  
→ Provide safety guidance  
→ Assign Level 4 escalation

No safety risk:
→ Continue normal support flow

---

# 4. Reusable Subtopic: Support Case Summary

### Purpose
Creates structured information for human support escalation.

### Captures
- Product and model
- Issue details
- Safety status
- Troubleshooting performed
- Outcome
- Escalation level
- Recommended next action

---

# Limitations

- No live warranty lookup.
- No repair status tracking.
- No ticket creation.
- No final warranty approval/rejection.
- No technician scheduling.
- Supports only configured products.

