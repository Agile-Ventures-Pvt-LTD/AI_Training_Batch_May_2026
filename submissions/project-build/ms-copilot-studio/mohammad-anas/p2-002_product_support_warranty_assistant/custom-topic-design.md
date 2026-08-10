# Custom Topic & Subtopic Design

## 1. Guided Product Troubleshooting and Safety Triage (Main Topic)
* **Purpose:** Identifies product, checks safety, runs technical troubleshooting loops, and routes to case summary.
* **Triggers:** `"troubleshoot my product"`, `"product isn't working"`, `"help with device issue"`, `"fix my appliance"`, `"my gadget is malfunctioning"`.
* **Inputs & Variables:** `ProductFamily`, `ProductModel`, `SymptomDescription`, `PowerStatus`, `ErrorCode`, `IssueStart`, `IssueFrequency`, `AttemptedSteps`, `TroubleshootingStepCount`, `TroubleshootingResolved`, `EscalationLevel`.
* **Conditions & Loops:** Branches between Laptop and Printer steps. Increments step counter from 1 to 2; if unresolved after 2 attempts, stops loop and escalates to Level 2 to avoid frustrating the user.
* **Redirects:** Calls `Product Safety Assessment` at the start and `Support Case Summary` at the end.

## 2. Warranty Eligibility and Service Route Assessment (Main Topic)
* **Purpose:** Checks preliminary warranty coverage and routes to the right service team.
* **Triggers:** `"check warranty eligibility"`, `"is my product under warranty?"`, `"repair or replacement eligibility"`, `"I lost my invoice can I claim warranty?"`.
* **Inputs & Variables:** `WarrantyProductFamily`, `WarrantyProductModel`, `ItemCategory`, `PurchaseDate`, `DeliveryDate`, `PurchasedFromNovaRetail`, `InvoiceAvailable`, `ProductAgeInMonths`, `AccidentalDamage`, `LiquidDamage`, `ElectricalSurge`, `UnauthorizedRepair`, `PreviousRepairCount`, `WarrantyClassification`, `ServiceRoute`.
* **Validation & Logic:** Calculates age in months using Power Fx `DateDiff`. Rejects future purchase dates. Applies 12-month limit for main units, 6-month limit for batteries/chargers, and flags consumables as not covered.
* **Special Branches:** Routes 7-day DOA claims and repeat repairs (>=2) to Level 3 Specialist Review. If basic troubleshooting wasn't done, redirects to Troubleshooting topic first.

## 3. Reusable Subtopics
* **Product Safety Assessment:** Takes symptom input, asks about smoke/heat/sparks. If `true`, sets Level 4 escalation, gives emergency advice, and ends dialog.
* **Support Case Summary:** Formats diagnostic data into an Adaptive Card. Adds preliminary disclaimer. If user confirms, outputs handover steps; if user disagrees, restarts topic to allow corrections.