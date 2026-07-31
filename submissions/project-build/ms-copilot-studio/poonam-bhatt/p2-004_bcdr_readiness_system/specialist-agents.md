# Specialist Agents Documentation

# P2-004: Autonomous Multi-Agent BC/DR Readiness System

This document outlines the detailed system design, input/output contracts, and instructional profiles for the six specialist connected agents coordinated by the central **BC/DR Supervisor Agent**.

---

## 1. Specialist Agent 1 - Application Criticality Specialist

### 1.1 Purpose
Evaluates the business context of a given application to categorize its importance to NovaSphere Technologies' operations and determine the appropriate recovery targets.

### 1.2 Required Input Variables
- `ApplicationID`, `ApplicationName`, `BusinessFunction`, `BusinessOwner`, `TechnicalOwner`, `UserCount`, `CustomerFacing`, `RevenueImpact`, `RegulatoryImpact`, `DataClassification`, `OperatingHours`, `UpstreamDependencies`, `DownstreamDependencies`.

### 1.3 Classification Logic
- **Mission Critical**: 24/7 service, >10,000 active users, customer-facing, high financial loss (>100k/hr) or major regulatory impact (GDPR/SOX compliance), or zero manual workarounds.
- **Business Critical**: High financial impact, medium user group (1,000 - 10,000), internal or customer-facing with a limited manual workaround.
- **Important**: Internal-only tool, low-to-medium user footprint, or manageable manual workarounds.
- **Standard**: Non-critical routine services, low users (<100), with simple backup/restore needs.

### 1.4 Expected Output Variables
- `BusinessCriticality` (String: Mission Critical, Business Critical, Important, Standard)
- `CriticalityRationale` (String)

---

## 2. Specialist Agent 2 - Recovery Requirements Specialist

### 2.1 Purpose
Audits the target recovery objectives (RTO/RPO) against the application's actual configuration, identifying gaps and structural dependency conflicts.

### 2.2 Required Input Variables
- `BusinessCriticality`, `CurrentRTOHours`, `CurrentRPOHours`, `RequiredRTOHours` (derived from policy), `RequiredRPOHours`, `MaximumTolerableDowntime`, `ManualWorkaround`, `UpstreamDependencies`, `DownstreamDependencies`.

### 2.3 Gap Detection Rules
- **Criticality Target Violations**: Flag if a *Mission Critical* application has an RTO goal greater than 1 hour or RPO goal greater than 4 hours.
- **Downtime Violations**: Flag if `CurrentRTOHours` > `MaximumTolerableDowntime`.
- **Dependency Inversion**: Flag if a critical application depends on an upstream service with a *slower* RTO/RPO target.
- **Manual Workaround Check**: Flag if a *Mission Critical* or *Business Critical* service has no manual workarounds recorded.

### 2.4 Expected Output Variables
- `RTO_Gap_Detected` (Boolean)
- `RPO_Gap_Detected` (Boolean)
- `InconsistentObjectives` (String: Description of mismatches)
- `RecoveryRequirementsConfidence` (Integer: 0-100)

---

## 3. Specialist Agent 3 - Technical Recovery Specialist (MCP Grounded)

### 3.1 Purpose
Reviews the hosting environment (Azure/M365) and compares current replication and backup settings against live Microsoft Learn documentation retrieved via the MCP server.

### 3.2 Required Input Variables
- `HostingPlatform`, `AzureService`, `BackupConfigured`, `BackupFrequency`, `LastBackupTestDate`, `DRConfigured`, `DRRegion`, `LastDRTestDate`.

### 3.3 Prompt Instructions & MCP Grounding Protocol
The Technical Recovery Specialist is manually configured with the following strict usage requirements:
1. Always use the **Microsoft Learn MCP** tool before making any technical assessment.
2. Identify the target Azure service or Microsoft technology (e.g. `"Azure SQL Database"` or `"Azure Virtual Machines"`).
3. Search and retrieve the most relevant Microsoft Learn documentation using the MCP tool.
4. Compare the application's recovery configuration against Microsoft guidance.
5. Base all recommendations on the retrieved documentation, providing URLs and quotes as evidence.
6. Clearly distinguish retrieved Microsoft documentation from your own reasoning.
7. **No Hallucination Fallback**: If the MCP server is unavailable or no documentation is found, do not fabricate Microsoft guidance. Return `"Technical Evidence Unavailable"` and recommend manual review.

### 3.4 Strict Output Format
The agent must return its findings using this exact layout:

```text
Technology Evaluated:
- <Technology>

Microsoft Documentation Retrieved:
- <Document 1>
- <Document 2>

Current Configuration:
- <Summary>

Technical Gaps:
- <Gap 1>
- <Gap 2>

Recommendations:
- <Recommendation 1>
- <Recommendation 2>

Evidence Status:
- Retrieved Successfully
or
- Technical Evidence Unavailable

Confidence Level:
- High / Medium / Low
```

> [!IMPORTANT]
> **Scope Restriction**:
> The Technical Recovery Specialist must return only factual technical findings and must **never** assign the overall BC/DR readiness classification (e.g., "Ready" or "High Risk"). That decision belongs exclusively to the **BC/DR Supervisor Agent**.

---

## 4. Specialist Agent 4 - Risk and Recovery Gap Specialist

### 4.1 Purpose
Consolidates business, recovery, and technical outputs to classify individual gaps and calculate the overall readiness rating.

### 4.2 Required Input Variables
- `BusinessCriticality`, `RTO_Gap_Detected`, `RPO_Gap_Detected`, `TechnicalRecoveryGap`, `BackupConfigured`, `DRConfigured`, `LastBackupTestDate`, `LastDRTestDate`, `RecoveryProcedureAvailable`.

### 4.3 Risk Classification Rules
Gaps are classified as **Critical, High, Medium, or Low**:
- **Critical Risk**: *Mission Critical* application with missing backup, zero DR setup, or RTO > 24 hours.
- **High Risk**: *Business Critical* application with backup but no tested DR procedure, or overdue DR test (>365 days).
- **Medium Risk**: *Important* application with outdated documentation or missing minor recovery scripts.
- **Low Risk**: *Standard* application with minor documentation review pending.

### 4.4 Expected Output Variables
- `CriticalGapCount` (Integer)
- `HighGapCount` (Integer)
- `MediumGapCount` (Integer)
- `LowGapCount` (Integer)
- `OverallReadiness` (String: Ready, Ready with Minor Gaps, Remediation Required, High Risk, Insufficient Evidence)

---

## 5. Specialist Agent 5 - Remediation Planning Specialist

### 5.1 Purpose
Converts identified risks and gaps into structured, actionable remediation cards with suggested owners and targets.

### 5.2 Required Input Variables
- `CriticalGapCount`, `HighGapCount`, `MediumGapCount`, `LowGapCount`, `OverallReadiness`, `TechnicalRecoveryGap`, `InconsistentObjectives`.

### 5.3 Remediation Actions Mapping
- If **Missing Backup** $\rightarrow$ Action: "Configure daily backup schedule with 30-day retention." Target Owner: Cloud Operations Team.
- If **Outdated DR Test** $\rightarrow$ Action: "Schedule and execute simulated disaster recovery switchover drill." Target Owner: Tech Lead.
- If **RTO Target Exceeded** $\rightarrow$ Action: "Implement Azure Traffic Manager and Multi-Region replica." Target Owner: Architect.

### 5.4 Expected Output Variables
- `RemediationTasksList` (JSON String array containing GapID, TaskDescription, TargetOwner, Priority, ExpectedOutcome)

---

## 6. Specialist Agent 6 - Reporting and Communication Specialist

### 6.1 Purpose
Generates final management outputs (Word Assessment Report, updates the Excel assessment register, and formats Outlook communications).

### 6.2 Required Input Variables
- All assessment metadata including `AssessmentID`, `ApplicationName`, `OverallReadiness`, `CriticalGapCount`, `HighGapCount`, `RemediationTasksList`.

### 6.3 Word Report & Outlook Escalation
- **Word Report**: Creates a detailed report under `reports/BCDR-Assessment-Report-[ID].docx` detailing the business profile, technical gaps, and remediation actions.
- **Outlook Notification Logic**:
  - **Ready / Ready with Minor Gaps**: Sends completion notification to the Application Owner.
  - **Remediation Required**: Sends remediation task schedule to the Technical Owner.
  - **High Risk / Insufficient Evidence**: Sends urgent escalation to Business Owner and Director of IT Operations.

### 6.4 Expected Output Variables
- `ReportGenerated` (Boolean)
- `NotificationSent` (Boolean)
