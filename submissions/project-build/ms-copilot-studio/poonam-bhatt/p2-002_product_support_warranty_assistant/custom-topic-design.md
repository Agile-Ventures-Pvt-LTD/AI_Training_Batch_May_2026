# Custom Topic Design Document

# P2-002 Product Support and Warranty Assistant

---

# 1. Overview

The Product Support and Warranty Assistant contains two mandatory custom topics designed according to the P2-002 PRD.

The topics are:

1. Guided Product Troubleshooting and Safety Triage
2. Warranty Eligibility and Service Route Assessment

The solution also contains reusable subtopics:

- Product Safety Assessment
- Support Case Summary

The design follows a modular conversational architecture where reusable logic is separated from main business workflows.

---

# 2. Custom Topic Architecture

```

```
                     Customer

                        |

                        v

          Product Support Assistant


    ------------------------------------

    |                                  |

    v                                  v
```

Guided Product                    Warranty Eligibility

Troubleshooting                   Assessment

```
    |                                  |

    v                                  v
```

Safety Assessment                 Warranty Rules

```
    |                                  |

    v                                  v
```

Case Summary                      Service Route

```

---

# 3. Custom Topic 1

# Guided Product Troubleshooting and Safety Triage

---

# Purpose

The purpose of this topic is to guide customers through safe first-line troubleshooting for supported laptops and printers.

The topic ensures:

- Required information collection
- Safety validation before troubleshooting
- Supported product verification
- Controlled troubleshooting
- Proper escalation

---

# 3.1 Trigger Categories

The topic is triggered for:

## General Troubleshooting

Examples:

- My device is not working
- Need help fixing my product
- Troubleshooting required


## Laptop Issues

Examples:

- Laptop not turning on
- Laptop charging issue
- Battery problem
- Display problem


## Printer Issues

Examples:

- Printer not printing
- Printer offline
- Scan problem
- Printing error


## Power and Error Conditions

Examples:

- Device has no power
- Error code displayed
- Device overheating

---

# 3.2 Information Collection

The topic collects the following information.

| Information | Purpose |
|---|---|
| Product Family | Identify device category |
| Product Model | Validate support |
| Issue Category | Select troubleshooting path |
| Symptom Description | Understand problem |
| Power Status | Diagnose issue |
| Error Code | Identify failures |
| Issue Start | Determine timeline |
| Issue Frequency | Understand behaviour |
| Attempted Steps | Prevent repetition |
| Physical Damage | Safety evaluation |
| Liquid Exposure | Safety evaluation |
| Safety Indicators | Detect risk |
| Continue Confirmation | User control |

---

# 3.3 Required Variables

```

ProductFamily

ProductModel

IssueCategory

SymptomDescription

PowerStatus

ErrorCode

IssueStart

IssueFrequency

AttemptedSteps

PhysicalDamage

LiquidExposure

SafetyIndicator

SafetyLevel

TroubleshootingStepCount

TroubleshootingResolved

EscalationLevel

CaseSummaryConfirmed

```

---

# 3.4 Safety Assessment Subtopic

## Purpose

Reusable safety validation performed before technical troubleshooting.

---

# Safety Checks

The assistant checks:

- Smoke
- Sparks
- Burning smell
- Electric shock
- Excessive heat
- Liquid exposure
- Battery swelling

---

# Safety Logic

```

Safety Risk Detected?

```
    |
```

---

Yes          No

|             |

Safety          Continue

Critical        Troubleshooting

|

Level 4 Escalation

```

---

# Safety-Critical Behaviour

When safety risk is detected:

The assistant:

- Stops troubleshooting
- Provides safety instructions
- Assigns Level 4 escalation
- Does not ask customer to reproduce the issue
- Routes for human support

---

# 3.5 Product Validation Branch

The assistant validates:

## Laptop

Supported:

- Lenovo ThinkPad E14 Gen 5


## Printer

Supported:

- HP LaserJet Pro MFP M428-M429


If unsupported:

- Inform customer
- Avoid model-specific instructions
- Recommend escalation

---

# 3.6 Laptop Troubleshooting Branch

Supported categories:

## No Power

Flow:

- Collect power information
- Generate grounded troubleshooting response
- Provide safe steps
- Check resolution


---

## Charging Failure

Collect:

- Charger status
- Charging behaviour
- Power indicator


---

## Battery Drain

Collect:

- Battery behaviour
- Usage pattern
- Battery condition


---

## Blank Display

Collect:

- Power indicator
- Display behaviour


---

## Additional Supported Categories

- External Display
- Overheating
- Wi-Fi Problems
- Keyboard/Touchpad Issues

---

# 3.7 Printer Troubleshooting Branch

Supported categories:

## Printer Offline

Checks:

- Connection status
- Network availability


---

## Paper Jam

Checks:

- Error message
- Paper path condition


---

## Poor Print Quality

Checks:

- Print appearance
- Toner condition


---

## Scan Failure

Checks:

- Scanner connection
- Error messages


---

## Additional Categories

- Network Connectivity
- Toner Warning
- Error Message
- No Power

---

# 3.8 Controlled Troubleshooting Loop

The assistant maintains:

- TroubleshootingStepCount
- Completed steps
- Resolution status

The loop stops when:

## Resolved

Customer confirms issue fixed.

---

## Cancelled

Customer chooses not to continue.

---

## Safety Issue

Risk is detected.

---

## Maximum Attempts Reached

Escalation is required.

---

# 3.9 Support Case Summary Subtopic

## Purpose

Creates a structured summary after troubleshooting.

---

# Summary Contains

- Product family
- Product model
- Issue category
- Symptoms
- Safety classification
- Troubleshooting performed
- Outcome
- Escalation level
- Recommended next action
- Customer confirmation

---

---

# 4. Custom Topic 2

# Warranty Eligibility and Service Route Assessment

---

# Purpose

Provide a structured preliminary warranty assessment and recommend the appropriate service route.

The topic does not:

- Approve claims
- Reject claims
- Guarantee repairs
- Guarantee replacement
- Access live warranty systems

---

# 4.1 Information Collection

The topic collects:

| Information | Purpose |
|-|-|
| Product Family | Product validation |
| Product Model | Model identification |
| Item Category | Coverage selection |
| Purchase Date | Warranty calculation |
| Delivery Date | Date validation |
| NovaRetail Purchase | DOA validation |
| Invoice Availability | Document check |
| Serial Availability | Identification |
| Issue Category | Problem classification |
| Product Operation | Failure status |
| Damage Status | Exclusion check |
| Previous Repairs | Repeat repair assessment |

---

# 4.2 Required Variables

```

WarrantyProductFamily

WarrantyProductModel

ItemCategory

PurchaseDate

DeliveryDate

PurchasedFromNovaRetail

InvoiceAvailable

SerialAvailable

ProductAgeInMonths

IssueCategory

ProductOperational

AccidentalDamage

LiquidDamage

ElectricalSurge

UnauthorizedRepair

UnauthorizedModification

ConsumableItem

ReportedWithinSevenDays

TroubleshootingCompleted

PreviousRepairCount

SafetyOverride

WarrantyClassification

ServiceRoute

CustomerDisputesResult

AssessmentConfirmed

```

---

# 4.3 Warranty Validation

The assistant validates:

- Purchase date
- Delivery date
- Product support
- Product model
- Item category
- Required information completeness

---

# 4.4 Coverage Rules

| Category | Coverage |
|-|-|
| Laptop | 12 Months |
| Printer | 12 Months |
| Battery | 6 Months |
| Accessory | 6 Months |
| Consumables | Not Covered |

---

# 4.5 Dead-on-Arrival Assessment

Conditions:

- Purchased from NovaRetail
- Reported within seven days
- Product not operational
- No accidental damage
- No liquid damage

Outcome:

Potential Dead-on-Arrival Assessment

The assistant does not promise replacement.

---

# 4.6 Exclusion Assessment

Checks:

- Accidental Damage
- Liquid Damage
- Fire Damage
- Electrical Surge
- Unauthorized Repair
- Unauthorized Modification
- Cosmetic Damage
- Normal Wear
- Software Issues
- Malware
- Data Loss
- Consumables

Outcome:

Potentially Excluded

---

# 4.7 Repeat Repair Assessment

If:

Previous repair exists
AND
Same issue occurs again

Then:

- Assign Repeat Repair Review
- Escalate to Level 3 review
- Include repair history in summary

---

# 4.8 Warranty Classifications

Possible classifications:

- Potentially Covered
- Potential Dead-on-Arrival Assessment
- Potentially Excluded
- Outside Standard Coverage
- Insufficient Information
- Human Review Required
- Safety-Critical Escalation

---

# 4.9 Service Routes

Available routes:

- Self-Service Information
- Technical Support Review
- Warranty Specialist Review
- Repeat Repair Review
- Paid Support Review
- Safety-Critical Escalation
- Additional Information Required

---

# 4.10 Customer Disagreement Handling

If customer disagrees:

The assistant:

- Reconfirms information
- Allows corrections
- Updates variables
- Recalculates assessment
- Escalates unresolved disputes

---

# 5. Design Principles

## Safety First

Safety validation happens before troubleshooting.

---

## Reusable Logic

Common processes are separated into reusable topics.

---

## Controlled Automation

Important decisions follow defined rules.

---

## Transparency

The assistant provides preliminary assessments only.

---

## Human Escalation

Complex cases are routed appropriately.

---

# 6. Topic Outcomes

## Troubleshooting Outcomes

- Resolved through self-service
- Human technical-support review required
- Warranty assessment recommended
- Unsupported product escalation
- Safety-critical escalation
- Cancelled by customer


## Warranty Outcomes

- Potentially Covered
- Potential Dead-on-Arrival Assessment
- Potentially Excluded
- Outside Standard Coverage
- Insufficient Information
- Human Review Required
- Safety-Critical Escalation

```

---
