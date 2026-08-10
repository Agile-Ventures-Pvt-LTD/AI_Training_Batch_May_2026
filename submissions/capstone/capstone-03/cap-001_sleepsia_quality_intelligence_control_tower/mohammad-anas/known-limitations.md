# Known Limitations

## Platform constraints
- **No native parallel execution.** Copilot Studio's classic Topics run nodes sequentially; the five fan-out specialists are called one after another rather than truly simultaneously. This satisfies the PRD's explicit allowance for "logical fan-out/fan-in" but is not literal concurrent execution.
- **No native loop node.** Retry logic (specialist fallback) and the reassessment cycle counter are implemented via a topic calling itself with an incremented attempt/count variable, rather than a dedicated loop construct. Functionally equivalent, bounded correctly at the required limits (2 attempts, 2 reassessment cycles), but structurally a workaround.
- **No access to the newer Workflows canvas** (which natively supports parallel branches and loops) in this environment — build was constrained to Agent builder / classic Topics only.

## Implementation gaps
- One Power Fx table-extraction pattern (`First(TableVariable).ColumnName`) returned "invalid" in this environment during the BatchID-maps-to-SKU validation check in Topic 1. Root cause suspected to be output-shape nesting (`.value` wrapper) but not fully resolved within the project's time constraints. As a result, the affected validation check(s) in Topic 1 were narrowed to confirming the referenced record exists (row count check) rather than also cross-validating the specific mapped field value. 


## Tenant dependencies
- Teams and Microsoft 365 Copilot publishing availability depends on organisational sharing/app policy. It cannot be published because of Billing Issue.

## Data/testing scope
- All operational data is the supplied synthetic Sleepsia workbook; no real customer, medical, or payment data was used at any point.
