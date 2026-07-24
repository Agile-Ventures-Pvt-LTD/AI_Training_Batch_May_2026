# P2-002 | Product Support and Warranty Assistant


# Project Overview

The **Product Support and Warranty Assistant** is an AI-powered customer support chatbot developed using **Microsoft Copilot Studio** for **NovaRetail Technologies Pvt. Ltd.**

The chatbot serves as a first-line virtual support assistant that helps customers troubleshoot supported electronic products, obtain product information, understand warranty eligibility, receive safety guidance, and determine the appropriate support or escalation path.

The solution combines **Retrieval-Augmented Generation (RAG)** with structured conversational workflows to ensure responses are accurate, grounded, and based only on approved documentation and company policies.

---

# Business Problem

NovaRetail's customer support team receives a high volume of repetitive support requests related to:

- Laptop startup failures
- Charging problems
- Battery issues
- Blank displays
- Overheating
- Wi-Fi connectivity
- Printer offline problems
- Paper jams
- Printing issues
- Scanning failures
- Toner warnings
- Product setup
- Warranty questions
- Dead-on-arrival assessment
- Service eligibility
- Product safety incidents

Handling these repetitive requests manually increases support workload, response time, and operational costs.

This chatbot automates first-level customer support while ensuring that all safety and warranty decisions remain under human supervision.

---

# Project Objectives

The chatbot is designed to:

- Answer product questions using official documentation
- Guide users through safe troubleshooting
- Identify supported products before providing technical guidance
- Provide preliminary warranty assessment
- Detect safety-critical conditions
- Prevent unsafe troubleshooting
- Route customers to the correct support channel
- Generate structured case summaries
- Escalate high-risk cases to human support

---

# Supported Products

## Laptop

- Lenovo ThinkPad E14 Gen 5

Supported Issues

- Power problems
- Charging failures
- Battery issues
- Blank display
- External display
- Wi-Fi connectivity
- Keyboard
- Touchpad
- Overheating

---

## Printer

- HP LaserJet Pro MFP M428-M429

Supported Issues

- Printer offline
- Paper jam
- Poor print quality
- Network connectivity
- Scan failures
- Toner warnings
- Error messages
- No power

---

# Key Features

## Product Support

- Product setup guidance
- Product specifications
- Operating instructions
- Product feature explanation
- Troubleshooting assistance

---

## Guided Troubleshooting

The chatbot performs structured troubleshooting using official manufacturer documentation.

Features include:

- Product identification
- Model validation
- Safety assessment
- Category-specific troubleshooting
- Controlled troubleshooting loop
- Resolution confirmation
- Escalation after maximum attempts

---

## Warranty Assessment

Provides preliminary warranty guidance including:

- Warranty coverage period
- Product age calculation
- Dead-on-arrival assessment
- Warranty exclusions
- Consumable handling
- Battery coverage
- Accessory coverage
- Service routing

The chatbot never approves or rejects warranty claims.

---

## Safety Assessment

Before troubleshooting begins, the chatbot checks for safety-critical conditions such as:

- Smoke
- Fire
- Sparks
- Burning smell
- Electric shock
- Swollen battery
- Excessive heat
- Liquid entering electrical devices
- Exposed wiring
- Melting components

When any safety risk is detected, troubleshooting immediately stops and the customer is advised to seek urgent human assistance.

---

# AI Capabilities

The chatbot uses Retrieval-Augmented Generation (RAG) through Microsoft Copilot Studio.

The assistant retrieves answers only from configured knowledge sources instead of relying on general AI knowledge.

Benefits include:

- Accurate responses
- Reduced hallucinations
- Source-grounded answers
- Consistent troubleshooting
- Reliable warranty guidance

---

# Knowledge Sources

## Official Product Manuals

### Lenovo

ThinkPad E14 Gen 5 User Guide

Purpose

- Setup
- Power management
- Charging
- Display
- Battery
- Connectivity
- Diagnostics

---

### HP

HP LaserJet Pro MFP M428-M429 User Guide

Purpose

- Printer setup
- Printing
- Scanning
- Paper jams
- Print quality
- Maintenance
- Connectivity

---

## Public Websites

### Lenovo Support

Official Lenovo online documentation

---

### HP Support

Official HP setup and support documentation

---

## NovaRetail Knowledge Base

Three custom Markdown knowledge documents were created.

### NovaCare Limited Warranty Policy

Contains:

- Warranty periods
- Coverage
- Exclusions
- DOA policy
- Human approval requirements

---

### Product Support Scope

Defines:

- Supported products
- Supported models
- Supported troubleshooting
- Product boundaries

---

### Product Safety and Escalation Policy

Defines:

- Safety conditions
- Escalation levels
- Safety procedures
- Emergency guidance

---

# Knowledge Source Priority

## Product Information

1. Official Product Manual
2. Manufacturer Website
3. Product Support Scope

---

## Warranty Questions

1. NovaCare Warranty Policy
2. Product Safety Policy
3. Manufacturer Warranty Information

---

## Safety

1. Product Safety Policy
2. Manufacturer Safety Documentation

---

# Custom Topics

## Topic 1

### Guided Product Troubleshooting and Safety Triage

Functions

- Product identification
- Model validation
- Safety assessment
- Laptop troubleshooting
- Printer troubleshooting
- Controlled troubleshooting
- Resolution tracking
- Escalation
- Case summary

---

## Topic 2

### Warranty Eligibility and Service Route Assessment

Functions

- Warranty coverage calculation
- Product age calculation
- Coverage period validation
- Exclusion assessment
- DOA assessment
- Repeat repair handling
- Service route recommendation
- Preliminary warranty classification

---

# Reusable Subtopics

## Product Safety Assessment

Checks:

- Smoke
- Fire
- Sparks
- Burning smell
- Electric shock
- Swollen battery
- Excessive heat
- Liquid damage

Returns

- Safety Level
- Escalation Level

---

## Support Case Summary

Generates a structured summary including:

- Product
- Model
- Issue
- Safety status
- Troubleshooting performed
- Warranty classification
- Service route
- Recommended next action

---

# Variables

The chatbot captures multiple variables including:

- Product Family
- Product Model
- Issue Category
- Purchase Date
- Product Age
- Warranty Status
- Damage Indicators
- Safety Indicators
- Escalation Level
- Troubleshooting Status
- Previous Repair Count
- Service Route

---

# Conversation Flow

Customer Request

↓

Identify Product

↓

Validate Model

↓

Safety Assessment

↓

Supported Product?

↓

Technical Troubleshooting

↓

Issue Resolved?

↓

Yes → Complete

↓

No

↓

Warranty Assessment

↓

Coverage Evaluation

↓

Service Route

↓

Case Summary

↓

End Conversation

---

# Safety Controls

The chatbot immediately stops troubleshooting when:

- Smoke detected
- Fire detected
- Electric shock reported
- Swollen battery identified
- Excessive heat detected
- Burning smell reported

Customers are instructed to stop using the device and contact authorized human support.

---

# Privacy Controls

The chatbot never requests:

- Passwords
- PINs
- Banking details
- Payment card information
- Encryption keys
- Personal files
- Confidential customer information

---

# Security Features

- Prompt injection protection
- Grounded responses
- Hallucination prevention
- Source prioritization
- Unsupported model detection
- Escalation for uncertain cases

---

# Limitations

Current limitations include:

- No live warranty lookup
- No repair booking
- No case creation
- No inventory integration
- No repair status tracking
- No payment processing
- No customer account access
- No technician scheduling
- No real-time product availability
- Supports only configured products

---

# Testing

The chatbot was tested using scenarios covering:

- Product information
- Laptop troubleshooting
- Printer troubleshooting
- Warranty assessment
- Safety incidents
- Unsupported products
- Prompt injection
- Privacy
- Missing information
- Invalid inputs
- Customer corrections
- Cancellation
- Cross-topic navigation

---

# Technologies Used

- Microsoft Copilot Studio
- Retrieval-Augmented Generation (RAG)
- Microsoft Power Platform
- Generative Answers
- Microsoft Power Fx
- Markdown Knowledge Base

---

# AI Usage

AI tools were used to:

- Design conversation flows
- Generate documentation
- Improve chatbot instructions
- Assist with workflow design
- Draft Markdown documents

All AI-generated content was manually reviewed, validated against the PRD, and verified using official manufacturer documentation and NovaRetail policies.

---

# Future Improvements

Potential enhancements include:

- Live warranty verification
- CRM integration
- Case creation
- Appointment scheduling
- Repair tracking
- Inventory lookup
- Multi-language support
- Voice interaction
- Image upload for diagnostics
- OCR-based invoice verification

---

# Repository Structure

```
p2-002_product_support_warranty_assistant/
│
├── README.md
├── chatbot-url.md
├── solution-summary.md
├── agent-design.md
├── knowledge-sources.md
├── custom-topic-design.md
├── test-report.md
├── known-limitations.md
├── ai-usage-declaration.md
│
├── knowledge-base/
│   ├── novacare-limited-warranty-policy.md
│   ├── product-support-scope.md
│   └── product-safety-and-escalation-policy.md
│
└── screenshots/
```

---

# Project Status

**Status:** ✅ Completed

- Agent Created
- Knowledge Sources Configured
- Custom Topics Implemented
- Reusable Subtopics Created
- Safety Controls Implemented
- Warranty Assessment Implemented
- Testing Completed
- Published Successfully

---

## Author 
- Vaishnavi Gupta