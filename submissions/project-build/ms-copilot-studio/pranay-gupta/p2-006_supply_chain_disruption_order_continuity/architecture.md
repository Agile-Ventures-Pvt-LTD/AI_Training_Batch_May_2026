# Architecture

```text
Autonomous Recurrence Trigger
        ↓
Supply Continuity Supervisor
        ↓
Disruption Intake & Validation
        ↓
Valid? ──No→ Hold / Review
   │
  Yes
   ↓
In Assessment
   ↓
┌──────────────┬────────────────┬────────────────────┐
↓              ↓                ↓
Inventory      Alternate        Customer & Order
Impact         Supplier         Impact
└──────────────┴────────────────┴────────────────────┘
                       ↓
              Commercial Impact
                       ↓
                     Fan-In
                       ↓
              Recovery Planning
                       ↓
          Recovery Strategy Resolution
                       ↓
              Supervisor Validation
                       ↓
       Approval / Exception / Reassessment
                       ↓
           Reporting & Communication
                       ↓
              Word + Excel + Outlook
```

## Supervisor
Owns orchestration, specialist selection, waiting for findings, consolidation, conflict resolution, final risk classification, recovery validation, approval routing, reassessment decisions and final communication authorization.

## Data
The supplied workbook contains Disruption_Requests, Suppliers, SKU_Master, Inventory, Purchase_Orders, Customer_Orders, Alternate_Suppliers, Recovery_Rules, Stakeholders and Test_Scenarios.
