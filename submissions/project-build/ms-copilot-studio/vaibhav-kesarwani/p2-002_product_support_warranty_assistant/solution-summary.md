# Solution Summary

## Business Problem

NovaRetail Technologies Pvt. Ltd. requires an AI-powered customer support assistant that provides accurate, consistent, and policy-compliant first-line support for supported Lenovo laptops and HP printers. Customers often require assistance with product setup, troubleshooting, warranty eligibility, and safety-related issues. The solution reduces repetitive support requests while ensuring that safety-critical cases and warranty decisions are appropriately escalated to human representatives.

---

## Target Users

The solution is designed for:

- Customers who purchased supported Lenovo laptops or HP printers from NovaRetail.
- Customer support representatives requiring standardized first-line guidance.
- Warranty specialists handling escalated warranty assessments.
- Technical support teams managing complex troubleshooting cases.

---

## Product Portfolio

The chatbot currently supports the following products:

### Laptops

- Lenovo ThinkPad E14 Gen 5
- Lenovo ThinkPad E16 Gen 1

### Printers

- HP LaserJet Pro MFP M428-M429

### Accessories

- Bundled laptop batteries
- Bundled laptop chargers and accessories
- Bundled printer power cables

---

## Project Scope

The chatbot provides:

- Product setup assistance
- Product feature guidance
- First-line troubleshooting
- Product safety assessment
- Preliminary warranty eligibility assessment
- Service route recommendation
- Support case summary generation

The chatbot does **not**:

- Approve or reject warranty claims.
- Submit repair or replacement requests.
- Access live warranty databases.
- Access live repair status.
- Perform remote access.
- Recommend unsafe repair procedures.
- Support products outside the configured product portfolio.

---

## Core Capabilities

The solution provides the following capabilities:

- Product identification and validation
- Model-specific troubleshooting
- Safety-first troubleshooting workflow
- Guided troubleshooting for laptops and printers
- Warranty eligibility assessment
- Dead-on-arrival (DOA) assessment
- Warranty exclusion identification
- Repeat repair assessment
- Escalation recommendations
- Structured support case summaries
- Customer correction handling
- Grounded responses using configured knowledge sources

---

## Knowledge Architecture

The chatbot uses multiple authoritative knowledge sources with defined priorities.

### Internal Knowledge Sources

- NovaCare Limited Warranty Policy
- Product Support Scope
- Product Safety and Escalation Policy

These documents provide the authoritative source for:

- Warranty rules
- Coverage periods
- Supported products
- Safety procedures
- Escalation policies
- Business rules

### Manufacturer Documentation

Official Lenovo and HP PDF manuals provide:

- Product setup
- Hardware features
- Troubleshooting
- Diagnostics
- Maintenance
- Connectivity guidance

### Manufacturer Websites

Official Lenovo and HP public support websites provide:

- Online documentation
- Installation guidance
- Troubleshooting articles
- Product documentation

### Optional Support References

Supplementary Lenovo and HP support portals are configured as the lowest-priority knowledge sources for additional documentation and reference material.

---

## Custom Topics

The solution includes the following primary custom topics:

### Guided Product Troubleshooting and Safety Triage

This topic:

- Identifies the product
- Performs mandatory safety assessment
- Routes to laptop or printer troubleshooting
- Tracks troubleshooting progress
- Prevents repeated troubleshooting steps
- Escalates unresolved issues
- Generates a support case summary

### Warranty Eligibility and Service Route Assessment

This topic:

- Collects warranty-related information
- Validates customer inputs
- Calculates warranty age
- Determines applicable coverage
- Identifies exclusions
- Performs dead-on-arrival assessment
- Determines service routes
- Generates a warranty assessment summary

---

## Reusable Subtopics

The chatbot includes reusable subtopics to improve maintainability and reduce duplicated logic.

### Product Safety Assessment

- Detects safety-critical conditions
- Classifies safety level
- Stops unsafe troubleshooting
- Initiates immediate escalation

### Support Case Summary

- Summarizes collected information
- Displays troubleshooting outcome
- Displays warranty assessment
- Allows customer confirmation or correction

---

## Safety Controls

Customer safety is the highest priority throughout every conversation.

The chatbot:

- Detects smoke, sparks, fire, burning smell, electric shock, excessive heat, liquid exposure, exposed wiring, and swollen batteries.
- Immediately stops troubleshooting for safety-critical cases.
- Advises customers to stop using unsafe products.
- Recommends disconnecting power only when safe.
- Never asks customers to reproduce dangerous conditions.
- Never instructs customers to dismantle products.
- Directs Level 4 safety incidents to urgent human support.

---

## Decision Boundaries

The chatbot operates within clearly defined decision boundaries.

The chatbot **can**:

- Provide product information.
- Explain supported features.
- Deliver first-line troubleshooting.
- Perform preliminary warranty assessments.
- Recommend service routes.
- Identify potential warranty exclusions.
- Generate support summaries.

The chatbot **cannot**:

- Approve warranty claims.
- Reject warranty claims.
- Approve repairs.
- Approve replacements.
- Submit support requests.
- Access live enterprise systems.
- Retrieve live warranty status.
- Retrieve live repair status.
- Invent product specifications.
- Answer questions outside the configured knowledge sources.

---

## Implementation Decisions

The solution was implemented using Microsoft Copilot Studio with a modular architecture.

Key implementation decisions include:

- Separate knowledge sources for policy documents and manufacturer documentation.
- Reusable subtopics for safety assessment and support case summaries.
- Variable-driven conversation flow to avoid repeated customer questions.
- Mandatory product validation before model-specific troubleshooting.
- Mandatory safety assessment before all troubleshooting.
- Cross-topic redirection between troubleshooting and warranty assessment.
- Grounded generative answers restricted to the appropriate Lenovo or HP knowledge sources.
- Controlled troubleshooting loops with escalation after the defined attempt limit.
- Structured summaries for customer confirmation before topic completion.
- Clear separation between manufacturer technical guidance and NovaRetail business policies to ensure accurate and policy-compliant responses.

