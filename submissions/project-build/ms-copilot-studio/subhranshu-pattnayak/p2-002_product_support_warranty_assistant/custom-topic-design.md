# Custom Topic Design

# Major Topics

## Guided Product Troubleshooting and Safety Triage

### Purpose

Provide structured troubleshooting using official documentation while ensuring customer safety.

### Triggers

> General
- Help me troubleshoot my device
- My laptop is not working
- My printer is not working
- Device problem
- Troubleshoot product
- Technical support
- Help me fix my laptop
- Help me fix my printer
- Device isn't working
- Need technical help

>  Laptop
- Laptop won't start
- Laptop won't turn on
- ThinkPad problem
- ThinkPad not working
- Laptop issue
- Laptop troubleshooting

> Printer
- Printer not printing
- Printer offline
- Printer issue
- Printer troubleshooting
- HP printer problem
- LaserJet issue

### Major Flow
```
Product Identification

↓

Safety Assessment

↓

Collect Issue

↓

Grounded Troubleshooting

↓

Resolution Check

↓

Support Summary

```

---

## Warranty Eligibility Assessment

### Purpose

Provide a preliminary warranty assessment according to NovaCare policy.

### Major Flow
```
Identify Product

↓

Collect Purchase Information

↓

Collect Warranty Details

↓

Grounded Policy Assessment

↓

Recommended Action

↓

Support Summary
```

### Triggers

> General

- Check warranty
- Warranty status
- Warranty eligibility
- Is my device under warranty
- Warranty support
- Can I claim warranty
- Warranty help
- Warranty information

> Laptop

- ThinkPad warranty
- Lenovo warranty
- Laptop warranty

> Printer

- HP warranty
- Printer warranty
- LaserJet warranty

---

# Reusable Subtopics

## Product Safety Assessment

Purpose:

Identify safety hazards before troubleshooting.

Outputs:

- SafeToContinue
- SafetyLevel
- SafetyIssue

---

## Support Case Summary

Purpose:

Provide a structured summary of the conversation.

Outputs:

- Product Name
- Recommended Action

---

# Variables

## Shared Variables

- ProductName
- ProductCategory
- IssueDescription
- PurchaseDate
- WarrantyStatus
- SafetyLevel
- SafetyIssue
- RecommendedAction

---

# Validation

- Supported product verification
- Purchase date validation
- Safety checks
- Warranty information completeness

---

# Conditions

- Supported vs unsupported product
- Safe vs unsafe condition
- Warranty eligible vs additional review
- Troubleshooting resolved vs escalation

---

# Knowledge Sources Used

Troubleshooting

- Lenovo Manual
- HP Manual

Warranty

- NovaCare Warranty Policy

Safety

- Product Safety Policy

---

# Outcomes

- Issue Resolved
- Human Technical Support
- Warranty Review
- Safety Escalation
- Unsupported Product
- Conversation Completed