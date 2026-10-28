# Autonomous trigger

## Overview

The Autonomous Marketing Campaign Launch Readiness & Governance System is initiated through a **Microsoft Copilot Studio Recurrence Trigger**. The trigger enables **fully autonomous event-driven execution**, allowing the system to continuously monitor the campaign pipeline and automatically begin governance assessments without human intervention.

The trigger is responsible for identifying pending campaigns, preventing duplicate processing, initializing campaign state, and invoking the **Campaign Readiness Supervisor**.

## Trigger architecture

The trigger acts as the entry point to the complete orchestration workflow.

```text
Recurrence Trigger
        |
        v
Read Pending Campaigns
        |
        v
Select Oldest Pending Campaign
        |
        v
Duplicate Validation
        |
        v
Update Campaign Status
        |
        v
Campaign Readiness Supervisor
```

## Trigger type

**Platform:** Microsoft Copilot Studio

**Trigger:** Recurrence

**Execution mode:** Autonomous

**Invocation:** Scheduled

## Trigger schedule

The trigger can be configured according to operational requirements.

### Development configuration

* Frequency: Every 5 minutes

### Production configuration

* Frequency: Every 30 minutes

The trigger should execute continuously during business operations.

## Trigger objective

On every execution cycle, the trigger performs the following actions:

1. Retrieve pending campaigns.
2. Select the next campaign to process.
3. Prevent duplicate assessment.
4. Mark the campaign as In Assessment.
5. Invoke the Supervisor.
6. Exit cleanly when no work exists.

## Campaign retrieval

The trigger reads **CampaignRequestsTable** from Excel Online (Business).

### Query

Retrieve rows where:

```text
CampaignStatus = Pending
```

The result set represents the operational assessment queue.

## Campaign selection strategy

When multiple pending campaigns exist, the trigger selects **one campaign only**.

Selection priority:

1. Earliest LaunchDate
2. Oldest submission
3. Lowest CampaignID (if required)

This deterministic ordering provides predictable assessment behavior.

### Example

| Campaign | Launch Date | Status  |
| -------- | ----------- | ------- |
| CMP-001  | Aug 10      | Pending |
| CMP-002  | Aug 08      | Pending |
| CMP-003  | Aug 12      | Pending |

Selected campaign:

**CMP-002**

## Single-campaign processing

Only one campaign is processed during each trigger execution.

### Rationale

This prevents:

* concurrent specialist conflicts,
* duplicate reassessment,
* Excel write collisions,
* inconsistent campaign state,
* overlapping notifications.

The next recurrence cycle processes the next pending campaign.

## Duplicate processing prevention

Before invoking the Supervisor, the trigger validates that the selected campaign is not already being processed.

### Protected states

The trigger will not start a new assessment when the campaign is already in:

* In Assessment
* Awaiting Remediation
* Awaiting Approval
* Completed

This ensures that a campaign cannot enter multiple assessment workflows simultaneously.

## State initialization

Immediately after selecting a campaign, the trigger updates the campaign state.

### Excel update

CampaignStatus:

```text
In Assessment
```

AssessmentStartTime:

Current timestamp

This reservation mechanism prevents another trigger execution from selecting the same campaign.

## Trigger workflow

```text
Recurrence Event
        |
        v
List Campaigns
        |
        v
Pending Campaigns?
      /      \
     No       Yes
     |         |
     |         v
     |    Sort by Launch Date
     |         |
     |         v
     |    Select One Campaign
     |         |
     |         v
     |    Duplicate Check
     |         |
     |         v
     |    Update In Assessment
     |         |
     |         v
     +---- Invoke Supervisor
```

## No-work behavior

When no pending campaigns exist:

* no Supervisor invocation,
* no Excel updates,
* no notifications,
* trigger exits successfully.

This allows continuous scheduling without unnecessary execution.

## Supervisor invocation

The trigger passes the following information to the Supervisor.

### Input variables

* CampaignID
* CampaignName
* LaunchDate
* CampaignOwner

The Supervisor retrieves the remaining campaign data during the intake stage.

## Idempotent execution

The trigger is designed to be **idempotent**.

Running the trigger multiple times should not create duplicate assessments.

### Protection mechanisms

* state reservation,
* duplicate validation,
* single-campaign processing,
* Supervisor state validation.

## Error handling

### Excel retrieval failure

Behavior:

* log retrieval failure,
* terminate current cycle,
* preserve existing campaign states.

### Excel update failure

Behavior:

* do not invoke Supervisor,
* preserve campaign status,
* retry during next recurrence.

### Supervisor invocation failure

Behavior:

* update campaign status back to Pending,
* record execution failure,
* allow future retry.

## Retry strategy

The trigger itself does not perform repeated retries.

Instead:

* failed campaigns return to Pending,
* future recurrence cycles reprocess them,
* reassessment limits are handled by the remediation workflow.

## Operational state transitions

### Successful initialization

```text
Pending
      |
      v
In Assessment
```

### Initialization failure

```text
Pending
      |
      v
Pending
```

### Duplicate detection

```text
In Assessment
      |
      v
In Assessment
```

No new assessment is created.

## Throughput characteristics

Assuming a 5-minute schedule:

* 12 campaigns/hour
* 96 campaigns/day (8-hour window)

Assuming a 30-minute schedule:

* 2 campaigns/hour
* 16 campaigns/day (8-hour window)

The architecture can be extended to multiple parallel Supervisors if higher throughput is required.

## Monitoring considerations

The trigger should record:

* execution time,
* selected campaign,
* initialization success,
* duplicate detections,
* Supervisor invocation status,
* processing failures.

These metrics support operational monitoring and troubleshooting.

## Security considerations

The trigger requires access only to:

* CampaignRequestsTable

It does not require:

* Word access,
* Outlook access,
* specialist knowledge,
* reporting permissions.

This follows the principle of least privilege.

## End-to-end execution sequence

```text
Scheduled Trigger
        |
        v
Retrieve Pending Campaigns
        |
        v
Select Highest-Priority Campaign
        |
        v
Reserve Campaign
        |
        v
Mark In Assessment
        |
        v
Invoke Campaign Readiness Supervisor
        |
        v
Supervisor Begins Autonomous Governance Workflow
```

## Conclusion

The recurrence trigger provides a deterministic and autonomous entry point for the complete campaign governance system. By combining scheduled execution, state reservation, duplicate prevention, and Supervisor invocation, the trigger enables reliable event-driven orchestration while maintaining operational consistency and preventing concurrent assessment conflicts.
