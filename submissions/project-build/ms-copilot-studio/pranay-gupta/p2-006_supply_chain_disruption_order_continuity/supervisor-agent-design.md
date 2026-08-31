# Supervisor Agent Design

## Agent
**Pranay NovaSphere Supply Supervisor**

## Responsibilities
- Receive recurrence trigger.
- Select oldest Pending disruption.
- Prevent duplicate processing.
- Invoke Disruption Intake & Validation.
- Mark valid case In Assessment.
- Identify affected SKU/PO/customer scope.
- Invoke four independent specialists.
- Wait for required findings.
- Retry missing specialist once.
- Consolidate findings.
- Apply deterministic precedence.
- Invoke Recovery Planning.
- Invoke Recovery Strategy Resolution.
- Route approvals/exceptions.
- Decide selective reassessment.
- Assign final risk.
- Validate final strategy.
- Authorize reporting and communication.
- Update disruption state.
- Complete only after required downstream actions succeed.

## Supervisor Tools
### Excel
`Disruption_Requests` for trigger selection and state management.

### Child Agents
Inventory Impact, Alternate Supplier, Customer & Order Impact, Commercial Impact, Recovery Planning, Reporting & Communication.

### Topics
Disruption Intake & Validation; Recovery Strategy Resolution; Approval, Exception & Selective Reassessment.

## Restrictions
Never fabricate approval, supplier approval or customer agreement. Never autonomously place POs, cancel orders, commit customer dates or authorize commercial expenditure.
