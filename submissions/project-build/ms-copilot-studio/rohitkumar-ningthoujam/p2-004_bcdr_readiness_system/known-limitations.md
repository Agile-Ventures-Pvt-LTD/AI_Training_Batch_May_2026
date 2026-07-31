# Known Limitations

## P2-004 Autonomous Multi-Agent BC/DR Readiness System

## Overview
This document lists the known limitations and constraints of the BC/DR multi-agent solution built using Microsoft Copilot Studio.

## Limitations

### 1. MCP Dependency
- Technical Recovery Specialist depends on Microsoft Learn MCP Server availability.
- If MCP fails, the system does not hallucinate technical guidance.
- Assessment continues with limited evidence and may require manual review.

### 2. Data Dependency
- Assessment accuracy depends on application inventory completeness.
- Missing RTO, RPO, backup, DR, or ownership information may result in insufficient evidence.

### 3. Specialist Agent Dependency
- Supervisor Agent depends on successful specialist responses.
- Missing or conflicting outputs require reassessment or escalation.

### 4. Synthetic Data
- The solution uses sample enterprise data for testing.
- Results are not based on real production environments.

### 5. Tool Availability
- Excel, Word, and Outlook actions depend on Microsoft 365 connector availability and permissions.

### 6. Human Validation
- High-risk cases, conflicts, and major recovery decisions require human review.

## Conclusion
The system provides safe autonomous BC/DR assessment while avoiding unsupported recommendations and handling failures through evidence validation and escalation.