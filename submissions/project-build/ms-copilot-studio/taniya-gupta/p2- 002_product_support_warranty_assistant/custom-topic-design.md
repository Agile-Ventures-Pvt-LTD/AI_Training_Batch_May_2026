# Custom Topic Design

## Overview
This document outlines the design of the two custom topics and two reusable subtopics in NovaCare Assist.

---

## 1. Guided Product Troubleshooting and Safety Triage (Custom Topic)

**Purpose:** Safe, model-specific troubleshooting for Lenovo ThinkPad E14 Gen 5 and HP LaserJet Pro M428-M429.
**Triggers:** Participant-authored phrases (e.g., "My laptop won't turn on", "Printer is offline").
**Inputs & Variables:**
- `ProductFamily` (Laptop/Printer), `ProductModel`, `IssueCategory`, `SymptomDescription`
- `TroubleshootingStepCount` (Number), `SafetyLevel` (Text from subtopic), `EscalationLevel` (Text)
**Entities Used:** Choice entities for `ProductFamily` and Yes/No booleans.
**Validation:** Checks if the entered `ProductModel` is supported.
**Conditions:** 
- Restricts knowledge source based on `ProductFamily` (Lenovo vs HP).
- Halts troubleshooting if `SafetyLevel = Level4`.
**Loops:** A troubleshooting loop runs a maximum of 3 times.
**Redirects:** Redirects to *Safety Assessment* (before troubleshooting) and *Case Summary* (at the end).
**Sources:** Generative answers use manufacturer PDFs and websites based on product.
**Outcomes & Escalation:**
- Resolved = Level 1 Escalation
- Unresolved (max 3 loops) = Level 2 Escalation
- Unsafe = Level 4 Escalation
**Cancellation:** Users can say "Cancel" to gracefully end the loop.
**Limitations:** Cannot perform remote diagnostics or access the device.

---

## 2. Warranty Eligibility and Service Route Assessment (Custom Topic)

**Purpose:** Evaluates warranty eligibility based on the NovaCare policy.
**Triggers:** Participant-authored phrases (e.g., "Is my product under warranty?", "I have a defect").
**Inputs & Variables:**
- `PurchaseDate`, `DeliveryDate`, `ItemCategory` (Laptop/Battery/Consumable)
- `DamageIndicators` (Accidental/Liquid), `PreviousRepairs` (Number), `ProductAgeInMonths`
**Validation:** Ensures dates are not in the future and delivery date is after purchase date.
**Conditions:**
- Checks if `ProductAgeInMonths` is within 12 months (devices) or 6 months (batteries).
- Checks DOA window (within 7 days of delivery).
- Checks exclusions (liquid damage, accidental damage = not covered).
**Redirects:** Redirects to *Troubleshooting* topic if technical steps are needed, passing context variables.
**Sources:** Strictly grounded in the `NovaCare Limited Warranty Policy`.
**Outcomes & Escalation:**
- Covered, Excluded, or DOA.
- Ambiguous cases or multiple previous repairs = Level 3 Escalation.
**Cancellation:** Users can cancel during date collection.
**Limitations:** Decisions are preliminary and require human validation.

---

## 3. Product Safety Assessment (Reusable Subtopic)

**Purpose:** Triage safety-critical situations before troubleshooting.
**Triggers:** Called via redirect only.
**Variables & Conditions:** Asks about smoke, fire, swelling, or electric shocks. 
**Outcomes:** Returns `Global.SafetyLevel` as "Safe" or "Level4".

---

## 4. Support Case Summary (Reusable Subtopic)

**Purpose:** Summarize the conversation and confirm details with the customer.
**Triggers:** Called via redirect only.
**Variables:** Reads global and topic variables (Issue, EscalationLevel).
**Outcomes:** Displays a structured Adaptive Card summary.
**Cancellation/Correction:** Allows the user to correct details if they disagree with the summary.
