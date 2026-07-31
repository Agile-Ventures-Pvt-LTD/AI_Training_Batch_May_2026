# Autonomous Trigger Design

# P2-004: Autonomous Multi-Agent BC/DR Readiness System

## 1. Trigger Concept & Objectives
To achieve true autonomy, the **P2-004 BC/DR Readiness System** must execute without requiring a user to start a conversational chat. In the Copilot Studio 2026 Modern Experience, this is configured using a native **When a file is modified (OneDrive for Business)** trigger directly within the agent orchestration framework.

The trigger acts as an event listener:
- **Trigger Event**: Fired whenever the consolidated workbook file `P2-004_BCDR_Lab_Data.xlsx` is saved or modified in OneDrive for Business.
- **Control Source**: `P2-004_BCDR_Lab_Data.xlsx` (sheet: `Application_Inventory`).
- **Execution Rule**: The trigger launches the Supervisor agent, which queries the inventory table and initiates assessments only for applications where `AssessmentStatus = "Pending"`.

---

## 2. Event Payload Context Mappings
When the OneDrive trigger fires, it causes the Supervisor to pull the pending rows using Excel Online integration. For each matching record, the Supervisor maps and passes the following payload fields as input parameters to the connected specialist agents:

```json
{
  "ApplicationData": {
    "ApplicationID": "APP-001",
    "ApplicationName": "Customer Commerce Portal",
    "BusinessFunction": "Digital Sales",
    "BusinessOwner": "priya-owner@novasphere.com",
    "TechnicalOwner": "arjun-admin@novasphere.com",
    "HostingPlatform": "Azure",
    "AzureService": "Azure App Service",
    "Environment": "Production",
    "UserCount": 4200,
    "CustomerFacing": true,
    "CurrentCriticality": "Mission Critical",
    "DataClassification": "Confidential",
    "RegulatoryImpact": "Medium",
    "RevenueImpact": "High",
    "OperatingHours": "24x7",
    "CurrentRTOHours": 8,
    "RequiredRTOHours": 2,
    "CurrentRPOHours": 4,
    "RequiredRPOHours": 1,
    "MaximumTolerableDowntimeHours": 4,
    "ManualWorkaround": "No",
    "BackupConfigured": true,
    "BackupFrequency": "Daily",
    "LastBackupTestDate": "2026-06-15",
    "DRConfigured": false,
    "DRRegion": null,
    "LastDRTestDate": "2025-10-10",
    "UpstreamDependencies": "Azure SQL Database",
    "DownstreamDependencies": "Payment Gateway; CRM",
    "RecoveryProcedureAvailable": true,
    "DocumentationLastReviewed": "2026-02-12",
    "AssessmentStatus": "Pending"
  }
}
```

---

## 3. Configuration Steps in Microsoft Copilot Studio
To set up the file modification automation:

1. Open the **BC/DR Supervisor Agent** in Copilot Studio.
2. Go to **Triggers** $\rightarrow$ Click **+ New Trigger** $\rightarrow$ Select **When a file is modified (OneDrive for Business)**.
3. Configure the trigger node:
   - **Unique Name**: `WorkbookModifiedTrigger`
   - **Folder**: Select the OneDrive folder path containing the Excel file.
   - **File**: Select `P2-004_BCDR_Lab_Data.xlsx`.
4. In the **Additional instructions to the agent when it's invoked by this trigger** field, paste the following exact orchestration logic:

```text
Every time this trigger runs, autonomously perform a BC/DR readiness assessment.

1. Read the Application_Inventory table in the BCDR Excel workbook using the configured Excel tools.
2. Filter the table to process only applications where AssessmentStatus = "Pending".
3. For each pending application:
   - Retrieve the full application record.
   - Delegate business impact analysis to the Application Criticality Specialist connected agent.
   - Delegate recovery objective audits to the Recovery Requirements Specialist connected agent.
   - Delegate technical configuration checks to the Technical Recovery Specialist connected agent (utilizing the Microsoft Learn MCP server tool).
   - Delegate gap consolidation and readiness scoring to the Risk & Recovery Gap Specialist connected agent.
   - Delegate action planning to the Remediation Planning Specialist connected agent.
   - Delegate documentation outputs to the Reporting & Communication Specialist connected agent.
4. Consolidate the findings and assign the final Overall Readiness status.
5. Update the Assessment_Register sheet by writing a new assessment record row.
6. Update the Application_Inventory sheet by setting AssessmentStatus = "Completed" for the evaluated ApplicationID.
7. Generate the final assessment report and trigger the corresponding Outlook notification.

If no applications require assessment (AssessmentStatus = "Completed" or empty), take no action and wait for the next file modification.
```

---

## 4. Platform Constraints (No Separate Power Automate Flow)
- **Direct Orchestration Integration**: The OneDrive file modification trigger and Excel connections are configured **entirely inside the Copilot Studio workspace**.
- **No External Clouds**: No separate Power Automate cloud flows or external schedulers are used to drive the orchestration. This avoids platform lag, keeps logic centralized, and complies with the P2-004 architectural boundary constraints.
