# Known Limitations

## 1. Campaign Launch Boundary

The system evaluates campaign readiness. It does not autonomously launch campaigns.

## 2. Human Approval

Human approvals must be explicitly represented in supplied data or actual approval handling. The system must not infer or fabricate approval.

## 3. Specialist Failure

A missing or unusable specialist result is retried once. If the retry fails, the system must use insufficient-evidence/manual-review handling.

## 4. Reassessment Limit

Automated reassessment is limited to two cycles. After two unsuccessful cycles, the campaign is assigned to Manual Review.

## 5. Connector Dependency

Excel, Word, and Outlook behavior depends on the configured Microsoft connectors, permissions, and availability.

## 6. Synthetic Data

The project uses synthetic training data.
