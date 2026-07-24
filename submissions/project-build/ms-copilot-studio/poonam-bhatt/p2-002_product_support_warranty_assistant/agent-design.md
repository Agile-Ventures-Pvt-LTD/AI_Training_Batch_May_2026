Next file: **`agent-design.md`**

This is the most technical documentation file. It explains **how your Copilot Studio agent is designed internally** — topics, flow, variables, decision logic, reusable components, and architecture.

---

```markdown
# Agent Design Document

# P2-002 Product Support and Warranty Assistant

---

# 1. Agent Overview

The Product Support and Warranty Assistant is designed as a modular conversational AI agent using Microsoft Copilot Studio.

The agent combines:

- Custom conversation topics
- Reusable subtopics
- Knowledge grounding
- Conditional branching
- Variable-based decision making
- Generative AI responses
- Escalation workflows

The design focuses on providing safe customer assistance while maintaining controlled business logic.

---

# 2. Agent Architecture

## High-Level Architecture

```

```
                Customer
                   |
                   |
                   v

          Copilot Studio Agent

                   |
    --------------------------------
    |                              |
    v                              v
```

Product Support Flow          Warranty Assessment Flow

```
    |                              |
    v                              v
```

Safety Assessment              Warranty Validation

```
    |                              |
    v                              v
```

Troubleshooting                Coverage Assessment

```
    |                              |
    v                              v
```

Case Summary                   Service Route

```
    |
    v
```

Escalation / Resolution

```

---

# 3. Agent Components

The solution contains the following components:

| Component | Purpose |
|---|---|
| Main Topics | Customer-facing workflows |
| Reusable Topics | Common reusable processes |
| Knowledge Sources | Grounded information |
| Variables | Store conversation data |
| Conditions | Decision making |
| Generative Answers | Natural language responses |
| Escalation Paths | Human support routing |

---

# 4. Main Topics

The agent contains two mandatory custom topics.

---

# Topic 1: Guided Product Troubleshooting and Safety Triage

## Purpose

Guide customers through safe first-line troubleshooting for supported laptops and printers.

---

## Flow Design

```

Customer Issue

```
  |
```

Collect Product Information

```
  |
```

Safety Assessment

```
  |
```

Product Validation

```
  |
```

Issue Category Selection

```
  |
```

Troubleshooting Guidance

```
  |
```

Resolution Check

```
  |
```

Escalation / Summary



---

# Information Collection

The topic captures:

| Information | Purpose |
|-|-|
| Product Family | Identify laptop/printer |
| Product Model | Validate support scope |
| Issue Category | Select troubleshooting branch |
| Symptom Description | Understand issue |
| Power Status | Diagnose issue |
| Error Code | Identify errors |
| Issue Start | Determine timeline |
| Issue Frequency | Identify behaviour |
| Attempted Steps | Avoid repetition |
| Physical Damage | Safety assessment |
| Liquid Exposure | Safety assessment |
| Safety Indicators | Risk detection |

---

# Safety Assessment Design

Safety assessment is implemented as a reusable topic.

## Safety Checks

The agent checks:

- Smoke
- Sparks
- Burning smell
- Electric shock
- Excessive heat
- Liquid exposure
- Battery swelling

---

## Safety Decision

```

Safety Indicator Detected?

```
      |
 --------------

 Yes             No

 |               |
```

Level 4          Continue

Escalation       Troubleshooting

```

---

# Product Validation

The agent verifies:

## Laptop

Supported:

- Lenovo ThinkPad E14 Gen 5


## Printer

Supported:

- HP LaserJet Pro MFP M428-M429


Unsupported products:

- General guidance
- Human escalation

---

# Troubleshooting Branches

## Laptop Branch

Supported categories:

- No Power
- Charging Failure
- Battery Drain
- Blank Display
- External Display
- Overheating
- Wi-Fi
- Keyboard/Touchpad

---

## Printer Branch

Supported categories:

- Printer Offline
- Paper Jam
- Poor Print Quality
- Network Connectivity
- Scan Failure
- Toner Warning
- Error Message
- No Power

---

# Controlled Troubleshooting Loop

The agent maintains:

- Completed troubleshooting steps
- Attempt count
- Resolution status

The loop stops when:

- Issue is resolved
- Customer cancels
- Safety issue occurs
- Maximum attempts reached

---

# Topic 2: Warranty Eligibility and Service Route Assessment

## Purpose

Provide a structured preliminary warranty assessment.

The topic does not:

- Approve claims
- Reject claims
- Guarantee replacement
- Access live warranty databases

---

# Warranty Flow

```

Collect Warranty Information

```
      |
```

Validate Information

```
      |
```

Calculate Coverage

```
      |
```

Check DOA

```
      |
```

Check Exclusions

```
      |
```

Check Previous Repairs

```
      |
```

Generate Assessment

```
      |
```

Recommend Service Route

```

---

# Warranty Information Collection

Captured fields:

| Variable | Purpose |
|-|-|
| WarrantyProductFamily | Product identification |
| WarrantyProductModel | Model validation |
| ItemCategory | Coverage selection |
| PurchaseDate | Warranty calculation |
| DeliveryDate | Validation |
| InvoiceAvailable | Document status |
| SerialAvailable | Identification |
| IssueCategory | Problem type |
| ProductOperational | Product condition |
| Damage Indicators | Exclusions |
| PreviousRepairCount | Repeat repair handling |

---

# Warranty Decision Logic

## Coverage Rules

| Category | Period |
|---|---|
| Laptop | 12 months |
| Printer | 12 months |
| Battery | 6 months |
| Accessory | 6 months |
| Consumables | Not Covered |

---

# Warranty Classification

Possible outcomes:

- Potentially Covered
- Potential Dead-on-Arrival Assessment
- Potentially Excluded
- Outside Standard Coverage
- Insufficient Information
- Human Review Required
- Safety-Critical Escalation

---

# 5. Reusable Topics

## Product Safety Assessment

Purpose:

Perform mandatory safety checks before troubleshooting.

---

## Support Case Summary

Purpose:

Generate final customer-facing summary.

Contains:

- Product details
- Issue details
- Safety classification
- Troubleshooting performed
- Outcome
- Escalation level
- Next action

---

# 6. Variable Design

## Troubleshooting Variables

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

## Warranty Variables

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

# 7. Knowledge Grounding Strategy

The agent uses approved knowledge sources for:

- Warranty policies
- Safety rules
- Product scope
- Troubleshooting information

Generative responses are restricted to available knowledge.

---

# 8. Design Principles

## Safety First

Safety assessment occurs before troubleshooting.

## Modular Architecture

Reusable topics avoid duplicate logic.

## Controlled Automation

Business decisions use structured conditions.

## Human-in-the-loop

Complex cases are escalated.

## Transparency

The assistant clearly communicates limitations.

---

# 9. Future Improvements

Potential enhancements:

- CRM integration
- Automated ticket creation
- Real warranty database connection
- Serial number verification
- Image-based diagnosis
- Voice support
- Multi-language capability

```

---
