# Custom Topic and Subtopic Design

This document details the functional design of the custom topics and reusable subtopics implemented in Microsoft Copilot Studio.

---

## 1. Custom Topic 1: Guided Product Troubleshooting and Safety Triage

### 1.1 Purpose
Guide customers through model-specific, safe, first-line troubleshooting for supported laptops and printers. It prevents unsafe guidance, captures key details, uses a controlled loop, and creates a case summary.

### 1.2 Triggers
- **Trigger Phrases:** *"troubleshoot display"*, *"my laptop won't turn on"*, *"printer is offline"*, *"paper jam error"*, *"poor print quality"*, *"overheating issue"*, *"Wi-Fi connection failed"*.

### 1.3 Variables and Entities
| Variable Name | Type | Scope | Description / Captured Information |
| :--- | :--- | :--- | :--- |
| `ProductFamily` | Choice (Laptop/Printer) | Global | Identified product category |
| `ProductModel` | Choice | Global | Identified model (Lenovo ThinkPad E14 Gen 5 or HP LaserJet Pro MFP M428-M429) |
| `IssueCategory` | Choice | Topic | Category of the issue (e.g., No Power, Blank Display, Paper Jam, Print Quality) |
| `SymptomDescription`| Text | Topic | Description of how the issue behaves |
| `PowerStatus` | Choice (On/Off) | Topic | Is the device receiving power? |
| `ErrorCode` | Text | Topic | Error code or message shown on the screen |
| `IssueStart` | Text/Date | Topic | When the issue first occurred |
| `IssueFrequency` | Choice | Topic | Intermittent or Continuous |
| `AttemptedSteps` | Text | Topic | Troubleshooting steps already tried by the customer |
| `PhysicalDamage` | Boolean (Yes/No) | Global | Is there visible physical damage? |
| `LiquidExposure` | Boolean (Yes/No) | Global | Has the device been exposed to liquid? |
| `SafetyIndicator` | Boolean (Yes/No) | Topic | Does the user report smoke, sparks, burning smell, or excessive heat? |
| `SafetyLevel` | Number | Global | Calculated level of safety (1 to 4) |
| `TroubleshootingStepCount` | Number | Topic | Incremented step counter for the loop |
| `TroubleshootingResolved` | Boolean | Topic | Whether the issue was resolved by the troubleshooting |
| `EscalationLevel` | Choice | Global | Support level for routing (Level 1 to 4) |
| `CaseSummaryConfirmed` | Boolean | Topic | Customer confirmation of the case summary |

### 1.4 Logic Flow and Branching
1. **Triggering & Welcome:** User triggers the topic.
2. **Safety Triaging Redirect:** 
   - Immediately redirect to the **Product Safety Assessment** subtopic *before* collecting model details or running technical steps.
   - If a safety-critical issue is found, stop immediately, advice safety steps, set `SafetyLevel = 4`, and route to **Level 4 Urgent Escalation**.
3. **Product Validation Branch:**
   - Identify `ProductFamily` and `ProductModel`.
   - Validate model against supported scope.
   - If model is unsupported (e.g., Lenovo ThinkPad X1 or HP LaserJet Pro M15), present a limitation message and redirect to human support (Level 2).
   - Prevent model-specific instructions if the model is unknown.
4. **Troubleshooting Branching:**
   - **Laptop Branch (Lenovo ThinkPad E14 Gen 5):** Supports: *No power*, *Charging failure*, *Battery draining rapidly*, *Blank display*, *External-display problem*, *Overheating*, *Wi-Fi problem*, *Keyboard/touchpad problem*.
   - **Printer Branch (HP LaserJet Pro MFP M428-M429):** Supports: *Printer offline*, *Paper jam*, *Poor print quality*, *Network connectivity*, *Scan failure*, *Toner warning*, *Error message*, *No power*.
5. **Controlled Troubleshooting Loop:**
   - Initialize `TroubleshootingStepCount = 0`.
   - Retrieve step from the grounded manuals (restricted to Lenovo or HP sources respectively).
   - Show step to customer, and ask: *"Did this resolve the issue?"*
   - If yes: set `TroubleshootingResolved = True`, break loop, redirect to **Support Case Summary** subtopic.
   - If no: increment `TroubleshootingStepCount` by 1.
   - Loop exits if `TroubleshootingStepCount >= 3` (Maximum attempts reached) or if customer requests cancellation, or if a safety concern is raised during chat.
   - If loop exits unresolved: set `EscalationLevel = 2`, redirect to **Support Case Summary** and escalate.
6. **Correction Handling:**
   - At the summary step, if the customer indicates a correction is needed, allow them to modify `ProductFamily`, `ProductModel`, `IssueCategory`, or safety variables. Discard old classifications, recalculate variables, and regenerate the case summary.

---

## 2. Custom Topic 2: Warranty Eligibility and Service Route Assessment

### 2.1 Purpose
Provide a structured preliminary assessment of whether a reported issue falls within the NovaCare warranty policy and determine the appropriate service route. It calculates dates, applies exclusions, identifies missing invoice details, and routes cases.

### 2.2 Triggers
- **Trigger Phrases:** *"check warranty coverage"*, *"am I eligible for a repair?"*, *"how long is the warranty?"*, *"is my battery covered?"*, *"is accidental damage covered under warranty?"*, *"do I need an invoice for warranty?"*.

### 2.3 Variables
| Variable Name | Type | Scope | Description |
| :--- | :--- | :--- | :--- |
| `WarrantyProductFamily` | Choice | Topic | Category of the device under assessment |
| `WarrantyProductModel` | Choice | Topic | Product model |
| `ItemCategory` | Choice | Topic | Category (Laptop/Printer, Bundled Laptop Battery, Bundled Accessory, Consumable) |
| `PurchaseDate` | Date | Topic | Date of purchase from invoice |
| `DeliveryDate` | Date | Topic | Date of delivery (where available) |
| `PurchasedFromNovaRetail` | Boolean | Topic | Did they purchase from NovaRetail Technologies? |
| `InvoiceAvailable` | Boolean | Topic | Does the user have a valid invoice? |
| `SerialAvailable` | Boolean | Topic | Does the serial number match the invoice? |
| `ProductAgeInMonths` | Number | Topic | Calculated age since purchase date |
| `ProductOperational` | Boolean | Topic | Does the product work at all? |
| `AccidentalDamage` | Boolean | Topic | Is there accidental or liquid damage? |
| `LiquidDamage` | Boolean | Topic | Liquid damage indicators |
| `ElectricalSurge` | Boolean | Topic | Damage from external electrical surge |
| `UnauthorizedRepair` | Boolean | Topic | Has it been repaired by an unauthorized provider? |
| `UnauthorizedModification`| Boolean | Topic | Has the hardware been modified? |
| `ConsumableItem` | Boolean | Topic | Is the item a consumable (toner/paper)? |
| `ReportedWithinSevenDays` | Boolean | Topic | Was it reported within 7 calendar days of delivery? |
| `TroubleshootingCompleted` | Boolean | Topic | Has basic troubleshooting been completed? |
| `PreviousRepairCount` | Number | Topic | How many times has this issue been repaired? |
| `SafetyOverride` | Boolean | Topic | Did a safety-critical condition occur? |
| `WarrantyClassification` | Choice | Topic | Result (e.g., Potentially Covered, Potentially Excluded, Outside Standard Coverage, Insufficient Information) |
| `ServiceRoute` | Choice | Topic | Route (Self-service, Technical support, Warranty specialist, Repeat-repair, Paid-support) |
| `CustomerDisputesResult` | Boolean | Topic | Did the customer dispute the preliminary assessment? |
| `AssessmentConfirmed` | Boolean | Topic | Confirmation of warranty details |

### 2.4 Logic Flow and Branching
1. **Initialization and Safety Pre-Check:** Ensure no Level 4 safety indicators exist (using Safety Override).
2. **Inputs and Validation:**
   - Prompt for `ItemCategory` and `PurchaseDate`.
   - Validate `PurchaseDate` is not in the future.
   - If `DeliveryDate` is provided, validate it is not before `PurchaseDate`.
   - Calculate `ProductAgeInMonths` (Difference between current date 24 July 2026 and `PurchaseDate`).
3. **Cross-Topic Redirection:**
   - If `TroubleshootingCompleted = False`, offer redirection to **Guided Product Troubleshooting**.
   - If user accepts, redirect, pass product variables, receive the troubleshooting outcome, and resume the warranty assessment.
4. **Coverage Period Assessment:**
   - Match `ItemCategory` to policy duration:
     - *Laptop or Printer:* 12 months (`ProductAgeInMonths <= 12`).
     - *Bundled Laptop Battery:* 6 months (`ProductAgeInMonths <= 6`).
     - *Bundled Accessory:* 6 months (`ProductAgeInMonths <= 6`).
     - *Consumable:* Immediately classify as **Outside Standard Coverage** (Explain that toner, paper, and consumables are not covered).
5. **Dead-on-Arrival (DOA) Branch:**
   - If `ReportedWithinSevenDays = True`, `PurchasedFromNovaRetail = True`, `ProductOperational = False`, and there is no accidental/liquid damage:
     - Classify as **Potential Dead-on-Arrival Assessment** (Level 3 escalation).
     - Clarify that DOA requires technical verification and does not guarantee automatic replacement.
6. **Exclusion Branch:**
   - Check exclusions: `AccidentalDamage = True`, `LiquidDamage = True`, `ElectricalSurge = True`, `UnauthorizedRepair = True`, or `UnauthorizedModification = True`.
   - If any exclusion is met: Classify as **Potentially Excluded** (Explain which rule applies, without issuing a final absolute rejection, and route to Paid-Support or human review).
7. **Repeat-Repair Branch:**
   - Capture `PreviousRepairCount`. If `PreviousRepairCount >= 2` and the same issue returned, assign Level 3 **Repeat-Repair Review** escalation.
8. **Customer Disagreement Handling:**
   - If the user disagrees with the preliminary classification (e.g. they dispute an exclusion or age calculation), avoid arguing, allow them to correct facts, recalculate, and escalate unresolved disputes to a **Warranty Specialist** (Level 3).
9. **Assessment Summary:**
   - Display a structured summary of captured parameters, the preliminary classification, the applicable policy rule, required documents (invoice, serial number), and the assigned service route. Show the mandatory preliminary-assessment disclaimer.

---

## 3. Reusable Subtopics

### 3.1 Product Safety Assessment
- **Purpose:** Perform a rapid assessment of safety-critical indicators.
- **Inputs:** `SafetyIndicator`, `PhysicalDamage`, `LiquidExposure`.
- **Logic:** 
  - Loop through or ask about critical conditions (smoke, sparks, burning smell, excessive heat, swollen battery, exposed wires).
  - If any condition is positive, assign `SafetyLevel = 4`, return safety status to parent topic, stop normal troubleshooting, provide safety guidance, and route to Level 4 Escalation.
  - If negative, return `SafetyLevel = 1` and continue parent flow.

### 3.2 Support Case Summary
- **Purpose:** Create a structured text summary of the customer's case to prepare for human support handoff.
- **Inputs:** All captured variables from troubleshooting or warranty topic.
- **Outputs:** Formatted Case Summary block, including:
  - Product details (Family, Model, mask serial numbers if provided)
  - Issue category and symptoms
  - Troubleshooting performed and step count
  - Safety classification and Escalation Level
  - Recommended next action and service route
- **Customer Action:** Prompt user to confirm details or request a correction.
