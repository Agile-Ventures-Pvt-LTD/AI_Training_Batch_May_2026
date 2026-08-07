# Orchestration Patterns

## 1. Sequential

### Where Used

The overall campaign lifecycle and post-fan-in stages.

### Flow

```text
Trigger
→ Intake
→ Validation
→ In Assessment
→ Four Specialist Assessments
→ Fan-In
→ Launch Risk
→ Supervisor Decision
→ Reporting
→ Communication
```

The Launch Risk Specialist runs after the first four specialist results.

The Reporting & Communication Specialist runs after Supervisor validation.

## 2. Parallel Fan-Out / Fan-In

### Where Used

The first four domain assessments.

```text
                    Supervisor
                        |
          +-------------+-------------+
          |             |             |
       Budget         Brand        Channel
          |             |             |
          +-------------+-------------+
                        |
                      Asset
                        |
                        v
                      Fan-In
```

The Supervisor waits for the required independent results before consolidation.

## 3. Hierarchical

### Where Used

Supervisor-to-child-agent orchestration.

```text
Supervisor
   |
   +-- Budget Specialist
   +-- Brand Specialist
   +-- Channel Specialist
   +-- Asset Specialist
   +-- Launch Risk Specialist
   +-- Reporting Specialist
```

Child agents return findings. The Supervisor owns final decisions.

## 4. Conditional Routing

Examples:

- Campaign is not Pending → do not start a new assessment.
- Duplicate/current assessment → stop duplicate processing.
- Budget above approved amount → approval route.
- Budget above INR 1,000,000 → VP Marketing approval.
- Target CPL above INR 4,000 → VP Marketing approval.
- Multi-market campaign → Regional Marketing Lead approval.
- High-sensitivity campaign → additional review.
- Missing blocking asset → remediation.
- Urgent unresolved blocking condition → Not Ready.

## 5. Loop / Selective Reassessment

When a blocking condition is corrected:

```text
Correction
→ Identify changed domain
→ Mark affected result stale
→ Rerun affected specialist
→ Preserve unaffected results
→ Fan-In / Risk reassessment
→ Supervisor recomputes outcome
```

Example:

If only a missing landing page is corrected, the system should reassess the relevant Channel/Asset domain rather than automatically rerunning Budget.

Maximum automated reassessment cycles: **2**.

After two unsuccessful cycles:

```text
Manual Review
```

## 6. Fallback

If a specialist produces no usable result:

```text
Specialist Failure
      |
      v
Retry Once
   /       Success    Failure
  |          |
Continue   Insufficient Evidence
              |
              v
         Manual Review
```

The system must not convert an unsupported result into Ready.

## 7. Conflict Handling

When specialist findings differ, the Supervisor applies the supplied governance-policy precedence.

The system must not average or dilute blocking findings.
