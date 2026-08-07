# Dataset Notes

## P2-006 Supply Chain Disruption & Order Continuity

### 1. Purpose

This document describes the datasets used by the P2-006 Supply Chain Disruption & Order Continuity solution.

The datasets provide the source evidence required by the Supervisor Agent and specialist agents to assess a supply disruption, evaluate recovery options, determine customer and commercial impact, and support the final continuity decision.

The solution uses structured business data rather than relying on assumptions or manually generated information.

---

# 2. Dataset Architecture

The solution uses data stored in the configured Excel Online (Business) source.

The data is logically organized around the following business areas:

```text
Disruption Request
       |
       v
Disruption / Intake Data
       |
       +----------------------+
       |                      |
       v                      v
   SKU Master              Inventory
       |                      |
       +----------+-----------+
                  |
                  v
           Purchase Orders
                  |
                  v
        Specialist Assessments
                  |
       +----------+----------+
       |          |          |
       v          v          v
   Supplier    Customer   Commercial
    Data        Orders      Data
       |          |          |
       +----------+----------+
                  |
                  v
          Supervisor Agent
                  |
                  v
          Recovery Decision

The exact tables and columns available to the solution depend on the supplied P2-006 dataset.

3. Primary Disruption Data

The disruption record is the starting point for the assessment workflow.

The Supervisor Agent uses the disruption record to identify the disruption and determine whether it is eligible for assessment.

The key fields used by the intake workflow include:

Field	Purpose
DisruptionID	Unique identifier for the disruption
SupplierID	Identifies the affected supplier
SKU	Identifies the affected product
DisruptionType	Identifies the type of supply disruption
ReportedDate	Date on which the disruption was reported
ExpectedRecoveryDate	Expected recovery date
AffectedPO	Purchase order affected by the disruption
AffectedQty	Quantity affected by the disruption
ReportedSeverity	Initial reported severity
Status	Current workflow status

The Supervisor validates these fields before starting the specialist assessment.

4. Intake Status

The Status field is important to the orchestration workflow.

The primary intake state is:

Pending

A valid pending disruption can move to:

In Assessment

Other workflow states used by the implemented solution include:

Insufficient Evidence
Awaiting Approval
Recovery Plan Proposed
Customer Action Required
Management Escalation
Manual Review
Completed

The status determines where the disruption is within the overall continuity workflow.

5. SKU Master Data

The SKU Master provides product-level information required for inventory and impact calculations.

The Inventory Impact Specialist may use SKU Master information to obtain information such as:

SKU identification
Product attributes
Daily consumption information
Safety stock
Criticality information
Unit cost

The SKU Master is used as an evidence source and is not treated as an authoritative source for fields that it does not contain.

If the requested SKU cannot be found, the specialist reports the missing evidence rather than creating a value.

6. Inventory Data

Inventory data supports the assessment of available supply and potential shortage.

The Inventory Impact Specialist may evaluate:

On-hand quantity
Reserved quantity
Quality-hold quantity
Inbound quantity
Available inventory
Other inventory attributes provided by the dataset

Where applicable, the specialist calculates Available to Promise (ATP) using the configured business logic.

The implemented inventory logic uses:

ATP = On Hand - Reserved + Inbound Within 7 Days - Quality Hold

The calculated value is then compared with demand during the expected recovery period.

If required inventory evidence is unavailable, the specialist reports:

Insufficient Evidence

instead of estimating or fabricating inventory values.

7. Purchase Order Data

Purchase Order data is used to validate the relationship between the disruption and the affected customer/order commitment.

Relevant information can include:

Purchase Order ID
SKU
Supplier
Order quantity
Due date
Customer/order information

The Inventory Impact Specialist can cross-check the Purchase Order against the disruption record.

For example:

Disruption
    |
    +-- SKU
    +-- Supplier
    +-- Affected PO
    |
    v
Purchase Order
    |
    +-- SKU
    +-- Supplier
    +-- Quantity
    +-- Due Date

A mismatch is treated as an evidence issue.

The solution does not automatically assume that the disruption record is correct when another authorized source conflicts with it.

8. Supplier / Alternate Supplier Data

Supplier information supports evaluation of alternate recovery options.

The Alternate Supplier Specialist evaluates whether:

An alternate supplier exists.
The alternate supplier is available.
The alternate supplier is approved.
The alternate supplier can support recovery requirements.

The strategy workflow distinguishes between:

Approved Alternate

and

Unapproved Alternate

An unapproved alternate supplier does not automatically become an autonomous recovery option.

Instead, the workflow can route the situation for manual qualification or approval.

9. Customer and Order Data

Customer and order information is used by the Customer & Order Impact Specialist.

The assessment considers information relevant to:

Customer orders
Strategic orders
SLA commitments
Orders at risk
Required customer actions
Potential prioritization

The resulting assessment is provided to the Supervisor Agent for consolidation with inventory, supplier, and commercial findings.

10. Commercial Data

Commercial information supports the Commercial Impact Specialist.

Relevant fields may include:

Cost premium
Expedite premium
Supplier-related cost impact
Recovery-related commercial impact

The Approval/Reassessment topic uses configured thresholds for approval evaluation.

The implemented rules include:

Cost Premium > 15%

and

Expedite Premium > 10%

When an applicable threshold is exceeded, the workflow can require human approval.

11. Data Validation Principles

The solution follows the following data-validation principles.

11.1 Required fields must exist

The intake workflow validates mandatory disruption fields before assessment begins.

11.2 Values must be usable

Numeric fields such as affected quantity must satisfy the configured validation rules.

For example:

AffectedQty > 0
11.3 Status must be valid

A new assessment is expected to start from:

Pending
11.4 Cross-record relationships are validated

The solution checks relationships between disruption, SKU, supplier, inventory, and purchase-order information where required.

11.5 Missing evidence is not invented

When source data is unavailable, the specialist reports the evidence limitation.

For example:

Inventory record not found

is not converted into:

Inventory = 0

unless the source data explicitly supports that value.

12. Evidence Conflict Handling

A key feature of the solution is the identification of conflicting records.

An example conflict can occur when:

Disruption SKU
       ≠
Purchase Order SKU

or:

Disruption Supplier
       ≠
Purchase Order Supplier

or:

Disruption Quantity
       ≠
Purchase Order Quantity

These conflicts are reported as evidence issues.

The specialist should not resolve the conflict by guessing which record is correct.

Instead, the result should identify:

The conflicting records.
The fields that differ.
The impact of the conflict.
The recommended corrective action.
13. Data Quality Outcomes

The solution can produce different evidence states depending on the quality of the source data.

Sufficient Evidence

The required information is available and consistent enough for assessment.

Insufficient Evidence

Required information is missing or cannot be reliably established.

Evidence Conflict

Two or more authorized sources contain conflicting information.

Manual Review

The automated reassessment process has reached its configured limit or requires human intervention.

These outcomes support safe orchestration and prevent unsupported recovery decisions.

14. Dataset Usage by Specialist
Specialist	Primary Data Used
Inventory Impact Specialist	Disruption, SKU Master, Inventory, Purchase Orders
Alternate Supplier Specialist	Disruption, Supplier / Alternate Supplier data
Customer & Order Impact Specialist	Disruption, Customer / Order data
Commercial Impact Specialist	Disruption, Commercial / cost data
Supervisor Agent	Specialist outputs + disruption status

The Supervisor Agent is responsible for consolidating the outputs rather than independently replacing the specialist assessments.

15. Dataset-to-Workflow Mapping
Disruption Data
      |
      v
Disruption Intake
      |
      v
Validation
      |
      v
In Assessment
      |
      +-------------------+
      |                   |
      v                   v
SKU / Inventory      Supplier Data
      |                   |
      v                   v
Inventory Specialist  Supplier Specialist
      |                   |
      +---------+---------+
                |
                v
        Customer / Order Data
                |
                v
        Customer Specialist
                |
                v
        Commercial Data
                |
                v
        Commercial Specialist
                |
                v
       Supervisor Consolidation
                |
                v
        Recovery Strategy
                |
                v
      Approval / Reassessment
                |
                v
         Final Assessment
16. Test Dataset

The primary end-to-end test record used during solution validation was:

DisruptionID: TEST-DIS-001
SupplierID: SUP-06
SKU: SKU-1009
DisruptionType: Supply Delay
AffectedPO: PO-5010
AffectedQty: 10
Status: Pending

This test record was useful for validating both the workflow and evidence-validation behavior.

During specialist assessment, the solution identified data conflicts involving the SKU, inventory, supplier, and purchase order information.

This demonstrated that the solution can identify insufficient or inconsistent evidence rather than automatically assuming missing information.

17. Data Integrity Expectations

For production use, disruption records should contain consistent references across the relevant source tables.

The expected relationship is:

DisruptionID
      |
      +-- SupplierID
      |
      +-- SKU
      |
      +-- AffectedPO
             |
             +-- Matching SKU
             +-- Matching Supplier
             +-- Valid Quantity
             +-- Valid Due Date

Maintaining these relationships improves assessment confidence and reduces the likelihood of an Insufficient Evidence outcome.

18. Date Handling

Date values are retrieved from the configured data source.

When Excel date serial values are returned by the connector, the agent may display the underlying serial value during processing.

For example:

46241

represents an Excel date value.

The assessment should interpret the date according to the source-system representation rather than treating the serial number itself as a business date.

Date validation is particularly important when calculating the recovery window.

For example:

Assessment Date
        |
        v
Expected Recovery Date
        |
        v
Demand Until Recovery

If the expected recovery date has already passed, the workflow should recognize that condition rather than treating the recovery period as a future period.

19. Data Security and Source Authority

The solution uses the configured business data sources available through the connected tools.

Specialist agents should use authorized source information when performing assessments.

The agents should not:

Invent missing source records.
Fabricate inventory quantities.
Fabricate supplier approval.
Fabricate customer commitments.
Fabricate human approval.
Treat unsupported assumptions as verified evidence.

Human approval remains a controlled business process.

20. Dataset Limitations

The quality of the final assessment depends on the quality and completeness of the underlying dataset.

Potential limitations include:

Missing SKU records.
Missing inventory records.
Missing supplier records.
Incorrect purchase-order references.
Conflicting quantities.
Incorrect dates.
Missing customer/order information.
Connector failures.
Temporary data-source availability issues.

When such limitations affect the assessment, the solution should surface the limitation and avoid presenting unsupported conclusions as verified facts.

21. Dataset Maintenance

The underlying dataset should be maintained so that:

Disruption IDs remain unique.
SKU references match the SKU Master.
Supplier references match supplier data.
Purchase orders reference valid SKUs and suppliers.
Inventory records are available for active SKUs.
Dates are stored in valid formats.
Quantities are valid numeric values.
Workflow status values use the configured status vocabulary.

Regular data-quality checks will improve the reliability of autonomous continuity assessments.

22. Summary

The P2-006 dataset provides the evidence foundation for the autonomous supply continuity workflow.

The Supervisor Agent uses disruption information to initiate the workflow and coordinate specialist assessments.

Specialists use the relevant source data to assess:

Inventory impact.
Alternate supplier availability.
Customer and order impact.
Commercial impact.

The Supervisor then consolidates these findings and applies the configured recovery, approval, and reassessment rules.

The solution is designed to favor evidence-based decisions. When data is missing or conflicting, the workflow identifies the issue and routes the disruption toward an appropriate evidence or manual-review outcome rather than fabricating information.

This dataset structure therefore supports the core objective of P2-006: autonomous but controlled supply disruption assessment and order continuity decision-making based on available business evidence.