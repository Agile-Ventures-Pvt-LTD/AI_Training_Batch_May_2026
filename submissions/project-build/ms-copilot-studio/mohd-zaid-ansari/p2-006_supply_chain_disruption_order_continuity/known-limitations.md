# Known Limitations

## Overview

This document describes the current limitations and boundaries of the NovaSphere Supply Chain Continuity Management System built using Microsoft Copilot Studio.

The solution is designed as an autonomous decision-support system. It recommends recovery actions but does not replace human approval or execute restricted business actions.

---

# 1. Human Approval Dependency

Some recovery actions require human approval.

Examples:

* High-cost alternate supplier selection
* Expedite decisions
* Strategic customer protection decisions

The system can identify approval requirements but cannot approve actions autonomously.

---

# 2. No Autonomous Procurement Actions

The system cannot:

* Create purchase orders.
* Confirm supplier commitments.
* Approve supplier onboarding.
* Negotiate supplier terms.

Procurement execution remains a human-controlled process.

---

# 3. No Customer Commitment Automation

The system cannot:

* Promise customer delivery dates.
* Modify customer commitments.
* Cancel customer orders.

Customer communication requires authorized business teams.

---

# 4. Synthetic Dataset Limitation

The solution uses the provided fictional NovaSphere dataset.

Limitations:

* Data volume is small.
* Data is not connected to live ERP systems.
* Results depend on dataset accuracy.

---

# 5. Excel Dependency

The solution relies on Excel Online (Business) as the operational data source.

Potential limitations:

* Incorrect spreadsheet values may affect recommendations.
* Workbook availability impacts execution.
* Large-scale enterprise data may require Dataverse or ERP integration.

---

# 6. AI Recommendation Limitations

Generative AI is used for orchestration and analysis support.

Limitations:

* AI cannot infer missing business information.
* AI cannot create unsupported evidence.
* AI recommendations depend on available data and rules.

Deterministic policy rules always override AI judgement.

---

# 7. Specialist Agent Limitations

Specialist agents operate only within their assigned domain.

Examples:

* Inventory agent does not evaluate customer risk.
* Commercial agent does not approve spending.
* Supplier agent does not approve suppliers.

Final decisions remain with the Supervisor.

---

# 8. Reassessment Limitations

Selective reassessment is supported but bounded.

Rules:

* Maximum automated reassessment cycles: 2
* Only stale specialist results are regenerated.

After the limit is reached:

```text
Manual Review
```

is required.

---

# 9. Integration Limitations

Current implementation does not include:

* ERP/SAP integration
* Real-time supplier APIs
* Power BI dashboards
* External logistics systems
* Live market intelligence

---

# 10. Notification Limitations

Outlook notifications are sent only after Supervisor validation.

Limitations:

* Failed email delivery requires exception handling.
* Recipient accuracy depends on StakeholdersTable data.

---

# 11. Reporting Limitations

Generated Word reports depend on available specialist outputs.

If required evidence is missing:

* Report must indicate limitations.
* System must not fill gaps with assumptions.

---

# 12. Scalability Limitations

The project is designed for a small controlled dataset.

Future enterprise deployment may require:

* Dataverse storage
* Enterprise identity management
* Advanced monitoring
* ERP integration
* Higher-volume orchestration design

---

# 13. Security and Data Limitations

The solution uses only supplied synthetic data.

It does not currently implement:

* Advanced data classification
* Custom security roles
* Enterprise compliance controls

---

# Conclusion

The solution demonstrates autonomous multi-agent orchestration for supply disruption response while maintaining strict business controls.

The limitations are intentional to ensure safe AI operation, explainability, and compliance with human approval boundaries.
