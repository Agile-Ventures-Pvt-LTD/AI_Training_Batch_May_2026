# NovaCare Product Support and Warranty Assistant

## Project Information

| Field | Details |
|---|---|
| **Project Title** | NovaCare Product Support Assistant |
| **Project ID** | P2-002 |
| **Participant** | Palak |
| **Platform** | Microsoft Copilot Studio |
| **Status** | Completed / Published |
| **Published Agent URL** | https://copilotstudio.preview.microsoft.com/environments/Default-1e1572ff-a54c-4cd7-b2a9-20091afa5359/bots/3045ffcf-4887-f111-8076-000d3af21e08/overview |

---

## Objective

The **NovaCare Product Support and Warranty Assistant** is a customer-support agent built using Microsoft Copilot Studio.

The agent is designed to provide:

- Grounded product information
- Safe, model-specific first-line troubleshooting
- Product safety triage
- Warranty exclusion identification
- Appropriate support and escalation routes
- Structured support case summaries

All warranty assessments provided by the agent are **preliminary only**. Final warranty approval, rejection, repair, replacement, or commercial settlement requires validation by an authorised human representative.

---

## Supported Products

| Product Family | Supported Product / Item | Support Scope |
|---|---|---|
| **Laptop** | Lenovo ThinkPad E14 Gen 5 | Setup, power, charging, battery, display, keyboard, touchpad, Wi-Fi, ports, external display, and overheating |
| **Printer** | HP LaserJet Pro MFP M428-M429 | Setup, printing, scanning, connectivity, paper loading, paper jams, print quality, toner, maintenance, and error messages |
| **Laptop Accessory** | Bundled charger | Connection, power delivery, and visible-damage assessment |
| **Printer Accessory** | Bundled power cable | Connection and visible-damage assessment |

Unsupported or unidentified models are not given unsupported model-specific instructions. The agent instead communicates its limitation and provides an appropriate support or escalation route.

---

## Key Features

- Product and model identification before model-specific support
- Source-grounded responses using approved knowledge
- Lenovo-specific laptop troubleshooting
- HP-specific printer troubleshooting
- Safety assessment before technical troubleshooting
- Detection of safety-critical conditions
- Controlled troubleshooting with limited attempts
- Preliminary NovaCare warranty assessment
- 12-month standard laptop and printer warranty logic
- 6-month bundled laptop battery and accessory warranty logic
- Warranty exclusion handling
- Repeat-repair escalation
- Cross-topic redirection between warranty and troubleshooting
- Customer correction and reassessment support
- Human escalation based on case severity
- Structured support and warranty summaries
- Privacy and personal-data safeguards
- Prompt-injection and out-of-scope handling

---

## Custom Topics

### 1. Guided Product Troubleshooting and Safety Triage

Provides safe, model-specific troubleshooting for supported laptops and printers while checking for safety risks before providing technical steps. It tracks troubleshooting attempts, avoids repetition, and escalates unresolved or safety-critical issues appropriately.

### 2. Warranty Eligibility and Service Route Assessment

Provides a structured preliminary warranty assessment based on product details, coverage period, damage, exclusions, DOA conditions, and repair history. It determines the appropriate service route while ensuring final warranty decisions are validated by an authorised human representative.


---

## Knowledge Sources

### NovaRetail-Authored Knowledge

1. **NovaCare Limited Warranty Policy**
   - Warranty periods
   - Warranty eligibility
   - Exclusions
   - Dead-on-arrival rules
   - Documentation requirements
   - Warranty decision boundaries

2. **NovaRetail Product Support Scope**
   - Supported products and models
   - Supported issue categories
   - Product identification requirements
   - Unsupported-product handling

3. **NovaRetail Product Safety and Escalation Policy**
   - Safety-critical indicators
   - Mandatory safety behaviour
   - Escalation levels
   - Urgent escalation requirements

### Official Manufacturer Knowledge

4. **Lenovo ThinkPad E14 Gen 5 and ThinkPad E16 Gen 1 User Guide**
   - Official Lenovo PDF documentation used for laptop technical guidance.

5. **Lenovo ThinkPad E14 Gen 5 / E16 Gen 1 Online User Guide**
   - Official Lenovo web documentation used as a secondary laptop technical source.

6. **HP LaserJet Pro MFP M329, M428-M429 User Guide**
   - Official HP PDF documentation used for printer technical guidance.

7. **HP LaserJet Pro MFP M428-M429 Setup and User Guides**
   - Official HP support website used as a secondary printer source where indexing is available and reliable.

---

## Knowledge Source Precedence

### Product Operation and Troubleshooting

1. Official product-manual PDF
2. Official manufacturer support website
3. NovaRetail Product Support Scope
4. General model knowledge must not replace missing product information

### Warranty and Service Eligibility

1. NovaCare Limited Warranty Policy
2. Product Safety and Escalation Policy
3. Official manufacturer information where applicable
4. General knowledge must not replace missing NovaRetail policy information

### Safety

1. Product Safety and Escalation Policy
2. Official manufacturer safety instructions
3. Human escalation when information is uncertain

The agent does not silently combine conflicting warranty periods, exclusions, specifications, troubleshooting procedures, or safety instructions.

---

## Warranty Coverage Rules

| Item Category | Standard Coverage |
|---|---|
| Laptop | 12 months from original invoice date |
| Printer | 12 months from original invoice date |
| Bundled laptop battery | 6 months from original invoice date |
| Bundled accessory | 6 months from original invoice date |
| Printer toner, paper, or consumables | Not covered under standard warranty |

All results are preliminary and subject to human validation.

---

## Escalation Levels

| Level | Description | Route |
|---|---|---|
| **Level 1** | Routine information or successful first-line troubleshooting | Self-service |
| **Level 2** | Troubleshooting unsuccessful or repeated technical failure | Human technical-support review |
| **Level 3** | Warranty ambiguity, exclusions, repeat repair, or dispute | Warranty specialist / repeat-repair review |
| **Level 4** | Safety-critical condition | Immediate safety guidance and urgent escalation |

---

## Published Agent

**Agent URL:**  
(https://copilotstudio.preview.microsoft.com/environments/Default-1e1572ff-a54c-4cd7-b2a9-20091afa5359/bots/3045ffcf-4887-f111-8076-000d3af21e08/overview)

**Status:**  
Published / Ready for Evaluation

---

## Limitations

- The agent supports only the products and models defined in the configured Product Support Scope.
- Unsupported or unidentified models may require human support and are not given unsupported model-specific instructions.
- Warranty assessments are preliminary and do not constitute final claim approval or rejection.
- Final repair, replacement, warranty, or commercial decisions require an authorised human representative.
- The agent does not have access to a live warranty database unless an explicit integration is configured.
- The agent does not have access to live repair status, inventory, order history, or payment records unless explicitly integrated.
- The agent cannot submit a warranty claim, repair request, or replacement request unless an integrated system successfully performs that action.
- Exact product specifications, error codes, or procedures are not provided when they cannot be verified from configured knowledge.
- Full serial numbers and unnecessary sensitive personal information should not be stored in screenshots or project documentation.
- The HP support website may have indexing limitations because of dynamic web rendering. Where reliable website retrieval is unavailable, the official HP PDF manual is used as the authoritative printer technical source.
- Safety-critical cases are not handled through normal troubleshooting and require urgent escalation.
- The agent does not perform remote access, physical repair, product dismantling, or unsafe troubleshooting procedures.

---


## Important Disclaimer

The NovaCare Product Support and Warranty Assistant provides product-support guidance and **preliminary warranty assessments only**.

It does not make final warranty decisions or guarantee repair or replacement. Final warranty approval, rejection, repair, replacement, or commercial settlement must be validated by an authorised human representative.