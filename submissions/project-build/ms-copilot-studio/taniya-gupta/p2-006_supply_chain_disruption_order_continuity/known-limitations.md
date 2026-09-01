# Known Limitations & Technical Constraints — P2-006

## Architectural & Platform Limitations

1. **Connector Throttling & Latency:**
   - Sequential sub-agent execution in generative orchestration incurs approximately 15-20 seconds per agent invocation due to LLM context parsing and tool calling overhead.
   - Excel Online (Business) API row update actions require explicit key column binding (`DisruptionID`) to prevent 404 row lookup errors.

2. **Single Pending Record Processing per Recurrence Tick:**
   - To prevent race conditions and lock contention in Excel, the Recurrence Trigger processes exactly **one Pending disruption per execution cycle**. Bulk processing of multiple pending records requires consecutive trigger cycles.

3. **Synthetic Data Bounds:**
   - The solution operates strictly on synthetic lab datasets provided in `P2-006_Supply_Chain_Continuity_Lab_Data.xlsx`. Live ERP/SAP integration requires custom Dataverse or REST connectors.

4. **Human Approval Boundaries:**
   - Autonomous execution is strictly halted when financial thresholds (>15% cost premium, >10% expedite premium) or unapproved supplier guardrails (`Approved = No`) are met. The system cannot autonomously override human approval rules.
