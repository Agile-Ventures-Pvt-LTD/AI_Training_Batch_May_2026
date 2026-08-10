# Solution Summary

## Business Problem

Customers often require assistance with troubleshooting product issues and understanding warranty coverage before contacting support. Traditional support processes can involve repetitive questioning, inconsistent guidance, and delays in identifying safety-critical situations or the correct service route.

The NovaRetail AI Support Agent addresses these challenges by providing structured, knowledge-grounded assistance while ensuring safety policies and warranty rules are consistently applied.

# Target Users

The solution is intended for:

- Customers seeking product support
- Customers performing basic troubleshooting
- Customers requesting warranty guidance
- Customer support representatives reviewing case summaries

# Product Portfolio

The chatbot currently supports:

- Laptops
- Printers

# Project Scope

### In Scope

- Product troubleshooting
- Safety assessment
- Safety-critical escalation
- Preliminary warranty assessment
- Dead-on-Arrival (DOA) assessment
- Service route recommendation
- Support case summary generation
- Knowledge-grounded responses

### Out of Scope

- Warranty approval or rejection
- Repair booking
- Replacement authorization
- Refund processing
- Order management
- Payment verification
- Inventory lookup
- Repair status tracking
- Live database access

# Solution Capabilities

The chatbot can:

- Guide users through structured troubleshooting
- Detect potential safety hazards
- Recommend immediate safety actions
- Perform a preliminary warranty assessment
- Check warranty coverage eligibility
- Identify common warranty exclusions
- Recommend the appropriate support route
- Generate a structured support case summary
- Provide knowledge-grounded answers using approved documentation

# Knowledge Architecture

The chatbot uses multiple knowledge sources:

## PDF Documents

- HP printer manual PDF
- Lenovo laptop manual PDF

## Websites

- Lenovo Support
- HP Support

## Markdown Knowledge Base

- novacare-limited-warranty-policy
- product-safety-and-escalation-policy
- product-support-scope

This architecture ensures responses are based only on approved support documentation.

# Custom Topics

## Guided Product Troubleshooting and Safety Triage

Responsible for:

- Product information collection
- Guided troubleshooting
- Safety detection
- Troubleshooting recommendations
- Escalation when required

## Warranty Eligibility and Service Route Assessment

Responsible for:

- Warranty information collection
- Coverage assessment
- Warranty exclusion checks
- DOA assessment
- Service route recommendation
- Warranty summary generation

# Safety Controls

The chatbot continuously checks for safety-critical conditions, including:

- Smoke
- Sparks
- Fire
- Burning smell
- Electric shock
- Excessive heat
- Swollen battery
- Damaged battery

When detected, troubleshooting stops immediately and the chatbot recommends disconnecting power (where safe) and contacting authorized support.

# Decision Boundaries

The chatbot provides guidance only within predefined boundaries.

It does **not**:

- Approve warranty claims
- Reject warranty claims
- Guarantee repair or replacement
- Submit warranty requests
- Access live repair systems
- Access order history
- Access payment records
- Access inventory databases
- Access warranty databases
- Create support tickets

All warranty decisions remain the responsibility of authorized NovaRetail representatives.

# Implementation Decisions

The solution was implemented using Microsoft Copilot Studio with a modular conversation design.

Key implementation decisions include:

- Two custom topics for troubleshooting and warranty assessment
- Two reusable subtopics for safety assessment and case summaries
- Variable-driven conversation flow
- Conditional branching using Power Fx
- Knowledge-grounded responses
- Reusable conversation components
- Safety-first conversation design
- Human escalation for unsupported or safety-critical scenarios

This modular architecture improves maintainability, consistency, and scalability while ensuring responses remain compliant with business policies.