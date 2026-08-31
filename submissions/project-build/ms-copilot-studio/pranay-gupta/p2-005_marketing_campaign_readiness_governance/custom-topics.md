# Custom Topics

## Topic 1 — Campaign Intake & Validation

### Purpose

Perform deterministic pre-assessment validation before child agents are invoked.

### Required Validations

1. Campaign ID exists.
2. Campaign ID is unique.
3. Campaign status is Pending.
4. Campaign name exists.
5. Product exists.
6. Launch date exists.
7. Launch date is not in the past.
8. Budget values exist.
9. Geography exists.
10. At least one channel exists.
11. Campaign owner exists.

### Required Variables

Equivalent variables:

- CampaignID
- CampaignName
- Product
- LaunchDate
- DaysToLaunch
- ProposedBudget
- ApprovedBudget
- BudgetVariance
- TargetCPL
- Geography
- Channels
- Sensitivity
- CampaignOwner
- ValidationStatus
- DuplicateDetected

### Duplicate Handling

If the same campaign is already:

- In Assessment
- Awaiting Remediation
- Awaiting Approval
- Completed

do not create a new assessment.

### Flow

```text
List Pending campaigns
→ Select oldest eligible campaign
→ Retrieve campaign
→ Validate required information
→ Check duplicate/current state
→ Set In Assessment
→ Invoke specialists
```

---

## Topic 2 — Remediation & Selective Reassessment

### Purpose

Coordinate remediation when one or more specialist assessments fail or produce blocking conditions.

### Required Logic

1. Receive failed specialist domains.
2. Create remediation actions.
3. Identify responsible owner.
4. Set `CampaignStatus = Awaiting Remediation`.
5. Preserve passed specialist results.
6. Detect corrected underlying data.
7. Identify stale specialist results.
8. Rerun only affected specialists.
9. Re-enter Supervisor consolidation.
10. Recalculate final readiness.

### Example

If only a missing landing page is corrected, reassess the relevant Channel/Asset domain rather than automatically rerunning Budget.

### Loop Control

Maximum automated reassessment cycles: **2**.

After two unsuccessful cycles:

```text
Manual Review
```

---

## Topic 3 — Approval & Finalisation

### Purpose

Handle campaigns requiring mandatory human approval.

### Required Conditions

Evaluate:

- Proposed budget > approved budget
- Proposed budget > INR 1,000,000
- Target CPL > INR 4,000
- High regulatory sensitivity
- Multi-market geography
- Restricted/quantified claims
- Urgent launch with unresolved approval

### Required Logic

1. Determine required approver.
2. Prevent Ready while approval is outstanding.
3. Record approval reason.
4. Set `CampaignStatus = Awaiting Approval`.
5. Allow reassessment when approval data changes.
6. Return approval evidence to Supervisor.
7. Never fabricate human approval.

---

## Topic Exit Principles

- Intake failure stops specialist processing.
- Remediation returns corrected information to reassessment.
- Approval returns explicit approval evidence to Supervisor.
- Final readiness is always assigned by Supervisor.
