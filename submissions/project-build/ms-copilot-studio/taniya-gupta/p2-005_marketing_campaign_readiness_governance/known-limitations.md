# Known Limitations & Future Enhancements

1. **Parallel Infrastructure Execution:** Copilot Studio executes child agent calls logically in parallel fan-out/fan-in sequence; infrastructure-level true concurrency depends on Copilot Studio runtime thread pool.
2. **Reassessment Triggering:** Requires updating underlying Excel row data before initiating selective reassessment cycle. (since it only triggers for pending status)
