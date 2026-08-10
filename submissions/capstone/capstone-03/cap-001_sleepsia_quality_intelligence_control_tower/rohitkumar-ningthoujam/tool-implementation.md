# Tool Implementation

## Excel Tools

The solution uses Excel Online (Business) connector tools for operational quality data retrieval and CAPA updates.

Configured tools include:

- Get Batch Register
- Get Customer Complaints
- Get Owners - CAPA
- Get Returns - Customer Impact
- Get Product Master
- Get CAPA Register
- Get Returns
- Get Customer Complaints - Customer Impact
- Get Customer Complaints-supervisor
- Get Quality Incidents
- Get Customer Complaints - Safety
- get capa owner -supervisor
- Create CAPA Record

These tools support the specialist agents and Quality Supervisor with structured data retrieval and CAPA record creation/update.

## Word Tool

### Generate Quality Investigation Report

The Word connector tool is available to the Quality Supervisor.

Purpose:
- Generate the final Quality Investigation Report.
- Use consolidated investigation findings after the quality decision.
- Provide documented investigation results and recommended actions.

## Outlook Tool

### Send Quality Investigation Notification

The Outlook connector tool is available to the Quality Supervisor.

Inputs:
- To
- Subject
- Body

Purpose:
- Send the quality investigation outcome to the required recipient.
- Communicate the final decision and required follow-up actions.

## Microsoft Learn MCP

### Microsoft Learn MCP Server - M

The Microsoft Learn MCP tool is configured for the M365 Guidance Specialist.

Purpose:
- Retrieve Microsoft 365 and Copilot guidance.
- Support Microsoft 365-related implementation questions.

## Tool Configuration Evidence

The configured tools were created in Microsoft Copilot Studio under the Quality Supervisor and specialist agents.

The implementation uses:
- Excel Online (Business) for structured quality data.
- Word for investigation report generation.
- Outlook for quality investigation notifications.
- Microsoft Learn MCP for Microsoft 365 guidance.

All tools are enabled in the configured Copilot Studio environment.