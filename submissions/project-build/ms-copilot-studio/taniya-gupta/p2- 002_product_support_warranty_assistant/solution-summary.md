# Solution Summary

- **Project ID:** P2-002
- **Agent Name:** NovaCare Assist
- **Participant:** Taniya Gupta
- **Date:** 24 July 2026

---

## Business Problem

NovaRetail Technologies Pvt. Ltd. receives a high volume of repetitive customer-support queries through email and messaging channels. Common issues include:

- Products that do not power on or charge
- Blank or flickering laptop displays and overheating
- Printer offline conditions, paper jams, and print-quality problems
- Questions about warranty duration, exclusions, and repair eligibility
- Customers unsure whether accidental damage, missing invoices, or old purchase dates affect warranty
- Product safety incidents (smoke, swollen battery, electric shock) requiring urgent guidance

The support team required a conversational assistant that could handle first-line product queries safely, assess warranty eligibility consistently, and escalate appropriately — while never making final decisions or claiming actions that have not occurred.

---

## Intended Users

- Customers of NovaRetail Technologies Pvt. Ltd.
- Owners of Lenovo ThinkPad E14 Gen 5 laptops and HP LaserJet Pro MFP M428-M429 printers purchased from NovaRetail

---

## Product Portfolio Supported

| Product | Model | Support Type |
|---|---|---|
| Laptop | Lenovo ThinkPad E14 Gen 5 | Setup, troubleshooting, accessory support |
| Printer | HP LaserJet Pro MFP M428-M429 | Setup, troubleshooting, accessory support |
| Laptop battery | Bundled with ThinkPad E14 Gen 5 | Warranty assessment (6-month coverage) |
| Laptop charger | Bundled with ThinkPad E14 Gen 5 | Connection and damage assessment |
| Printer power cable | Bundled with M428-M429 | Connection and damage assessment |

---

## Solution Scope

The NovaCare Assist chatbot provides:

1. **Product identification** before any model-specific guidance
2. **Safety triage** before any troubleshooting step — stops all guidance for safety-critical conditions
3. **First-line troubleshooting** using official Lenovo and HP documentation
4. **Controlled troubleshooting loops** — limited to a defined maximum, no repeated steps
5. **Preliminary warranty assessment** using NovaCare Limited Warranty Policy exclusively
6. **Coverage period calculation** by item category (12 months for laptop/printer; 6 months for battery/accessories)
7. **Dead-on-arrival assessment** for products reported within 7 days of delivery
8. **Exclusion identification** (accidental damage, liquid, unauthorised repair, etc.)
9. **Repeat-repair escalation** for products previously repaired multiple times
10. **Structured case summaries** with customer confirmation and correction capability
11. **Cross-topic redirection** from warranty assessment to troubleshooting with variable reuse
12. **Customer disagreement handling** — allows correction and recalculation
13. **Graceful cancellation** and restart at any point

---

## Knowledge Architecture

### Sources Configured

| Source | Type | Authority Area |
|---|---|---|
| NovaCare Limited Warranty Policy | Markdown (participant-created) | All warranty and coverage decisions |
| NovaRetail Product Support Scope | Markdown (participant-created) | Supported products and scope rules |
| Product Safety and Escalation Policy | Markdown (participant-created) | Safety-critical conditions and escalation levels |
| Lenovo ThinkPad E14 Gen 5 User Guide | Official PDF (downloaded from Lenovo) | Laptop-specific troubleshooting |
| HP LaserJet Pro MFP M428-M429 User Guide | Official PDF (downloaded from HP) | Printer-specific troubleshooting |
| Lenovo ThinkPad E14 Online User Guide | Public website URL (Lenovo) | Supplementary laptop documentation |
| HP LaserJet M428-M429 Setup and Support | Public website URL (HP) | Supplementary printer documentation |

### Source Precedence

| Decision Area | Precedence Order |
|---|---|
| Laptop troubleshooting | Lenovo PDF → Lenovo website → Product Support Scope |
| Printer troubleshooting | HP PDF → HP website → Product Support Scope |
| Warranty eligibility | NovaCare Warranty Policy → Safety Policy → Manufacturer warranty info |
| Safety | Safety Policy → Manufacturer safety instructions → Human escalation |

---

## Custom Topics

### Topic 1: Guided Product Troubleshooting and Safety Triage
- Collects product family, model, issue category, symptom, power status, error codes, damage history
- Redirects to Product Safety Assessment subtopic before any technical steps
- Provides model-specific guidance via generative-answer nodes restricted to the correct manufacturer source
- Controlled loop: tracks step count, prevents repetition, escalates at maximum
- Supports correction of product and symptom information at any point
- Redirects to Support Case Summary subtopic on completion

### Topic 2: Warranty Eligibility and Service Route Assessment
- Collects purchase date, delivery date, item category, damage indicators, repair history
- Applies coverage period by item category (12 months / 6 months / not covered)
- Dead-on-arrival branch for products within 7 days of delivery
- Exclusion branch for accidental damage, liquid, unauthorised repair, etc.
- Repeat-repair escalation for 2+ previous repairs
- Cross-topic redirection to troubleshooting if not yet completed, with variable reuse
- Customer disagreement branch with recalculation
- Generates structured preliminary assessment with disclaimer

### Subtopic: Product Safety Assessment (Reusable)
- Checks all safety-critical conditions
- Classifies as Safe or Level 4
- Returns result to calling topic
- Stops normal flow for safety-critical cases

### Subtopic: Support Case Summary (Reusable)
- Displays structured summary of all captured variables
- Shows escalation level and recommended next action
- Allows customer correction before closing

---

## Safety Controls

- Safety triage performed before every troubleshooting session
- Safety check also performed during warranty assessment
- Level 4 safety response stops all routine processing immediately
- No instructions to dismantle products or reproduce unsafe conditions
- Emergency services recommended for fire, electric shock, or immediate danger

---

## Decision Boundaries

The NovaCare Assist chatbot **does not**:
- Approve or reject warranty claims
- Submit repair or replacement requests
- Claim access to live warranty databases, repair status, or inventory
- Generate final legal conclusions about warranty coverage
- Perform remote access or diagnostics
- Provide emergency dispatch services
- Collect passwords, banking details, or full serial numbers

All final decisions, approvals, and actions are performed by authorised NovaRetail human representatives.

---

## Implementation Decisions

1. **Markdown knowledge documents** were created as participant-authored files matching exact PRD policy content, then uploaded to Copilot Studio as file-based knowledge sources.
2. **HP website URL** — if the page cannot be indexed due to dynamic rendering, the HP PDF serves as the authoritative fallback. This limitation is documented in known-limitations.md.
3. **Controlled troubleshooting loop** — implemented using a step counter variable with a maximum of 3 steps before Level 2 escalation.
4. **Cross-topic redirection** — the warranty topic redirects to troubleshooting and receives the completion result, resuming assessment without re-collecting product and model information.
