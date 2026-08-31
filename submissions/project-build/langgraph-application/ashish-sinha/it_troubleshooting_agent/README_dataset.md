# IT Troubleshooting Agent Dataset

Synthetic dataset for **IT Troubleshooting Agent with Tool-Using Workflow Using LangGraph**.

## Contents

```text
data/knowledge_base/
├── vpn_troubleshooting_guide.md
├── email_outlook_troubleshooting_guide.md
├── laptop_performance_guide.md
├── password_reset_guide.md
├── network_connectivity_guide.md
└── printer_troubleshooting_guide.md

data/database/
└── it_support.db
```

## Database Tables

```text
users
devices
tickets
known_incidents
diagnostic_snapshots
```

## Intended Agent Capabilities

The agent should classify issue type, retrieve troubleshooting guidance, inspect user/device/ticket/known incident data, run diagnostic checks using SQLite data, branch conditionally based on severity and missing information, generate a resolution plan, and avoid unsafe requests for passwords/OTP/MFA codes.

This is synthetic training data only.
