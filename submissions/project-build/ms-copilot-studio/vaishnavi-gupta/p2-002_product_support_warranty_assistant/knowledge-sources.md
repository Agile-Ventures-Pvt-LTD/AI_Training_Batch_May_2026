# Knowledge Sources

## Project Information

| Field | Details |
|--------|----------|
| **Project ID** | P2-002 |
| **Project Name** | Product Support and Warranty Assistant |
| **Platform** | Microsoft Copilot Studio |
| **Version** | 1.0 |

---

# Purpose

This document describes all knowledge sources configured in the Product Support and Warranty Assistant.

The chatbot uses Retrieval-Augmented Generation (RAG) to answer customer questions. Instead of relying on general AI knowledge, it retrieves information only from approved and configured knowledge sources.

This approach improves:

- Accuracy
- Reliability
- Safety
- Transparency
- Hallucination prevention
- Policy compliance

---

# Knowledge Source Architecture

The chatbot uses two categories of knowledge sources:

## External Knowledge Sources

Official documentation provided by the product manufacturers.

- Lenovo Documentation
- HP Documentation

---

## Internal Knowledge Sources

Company-specific documentation created for NovaRetail.

- NovaCare Limited Warranty Policy
- Product Support Scope
- Product Safety and Escalation Policy

---

# Knowledge Source 1

## Lenovo ThinkPad E14 Gen 5 User Guide

### Source Type

PDF Document

### Provider

Lenovo

### Purpose

This document is used to answer questions related to the supported Lenovo laptop.

### Supported Topics

- Product overview
- Initial setup
- Charging
- Battery
- Keyboard
- Touchpad
- Display
- External monitor
- Wi-Fi connectivity
- BIOS information
- Hardware features
- Safe troubleshooting
- Maintenance
- Product specifications

### Used By

- Guided Product Troubleshooting Topic
- Generative Answer Nodes

### Restrictions

The chatbot only uses this document for technical guidance.

It is **not** used for:

- Warranty decisions
- Coverage determination
- Company policies

---

# Knowledge Source 2

## Lenovo Support Website

### Source Type

Official Website

### Provider

Lenovo

### Purpose

Provides additional product support information that may not be present in the PDF documentation.

### Supported Topics

- Driver information
- Software updates
- Troubleshooting
- Setup
- Connectivity
- Product documentation

### Used By

Generative Answer nodes when additional product information is required.

### Restrictions

Only official Lenovo documentation is considered valid.

---

# Knowledge Source 3

## HP LaserJet Pro MFP M428-M429 User Guide

### Source Type

PDF Document

### Provider

HP

### Purpose

Provides official printer documentation.

### Supported Topics

- Printer setup
- Printing
- Scanning
- Copying
- Wireless setup
- Paper handling
- Paper jams
- Print quality
- Error messages
- Toner replacement
- Maintenance

### Used By

Printer troubleshooting topic.

### Restrictions

Not used for warranty decisions.

---

# Knowledge Source 4

## HP Support Website

### Source Type

Official Website

### Provider

HP

### Purpose

Provides official online printer support information.

### Supported Topics

- Printer configuration
- Driver installation
- Firmware
- Troubleshooting
- Connectivity
- Product documentation

### Used By

Printer Generative Answer nodes.

### Restrictions

Only official HP documentation is considered authoritative.

---

# Knowledge Source 5

## NovaCare Limited Warranty Policy

### Source Type

Markdown Document

### Purpose

Defines the warranty rules followed by NovaRetail.

### Contains

- Warranty periods
- Coverage rules
- Exclusions
- Dead-on-arrival policy
- Repeat repair policy
- Human review requirements
- Warranty limitations
- Required documentation

### Used By

Warranty Eligibility and Service Route Assessment Topic.

### Priority

Highest priority for all warranty-related questions.

---

# Knowledge Source 6

## Product Support Scope

### Source Type

Markdown Document

### Purpose

Defines the products and models supported by the chatbot.

### Contains

- Supported laptops
- Supported printers
- Supported issue categories
- Product boundaries
- Unsupported products
- Escalation guidance

### Used By

Product validation and troubleshooting topics.

---

# Knowledge Source 7

## Product Safety and Escalation Policy

### Source Type

Markdown Document

### Purpose

Provides mandatory safety rules and escalation procedures.

### Contains

- Safety indicators
- Level 4 escalation criteria
- Emergency response guidance
- Safe troubleshooting rules
- Safety restrictions

### Used By

Product Safety Assessment subtopic.

### Priority

Highest priority for all safety-related conversations.

---

# Knowledge Source Priority

The chatbot follows a strict priority order to ensure consistent and reliable responses.

## Technical Questions

1. Lenovo User Guide
2. Lenovo Support Website
3. HP User Guide
4. HP Support Website

---

## Warranty Questions

1. NovaCare Limited Warranty Policy
2. Product Support Scope

---

## Safety Questions

1. Product Safety and Escalation Policy
2. Official Manufacturer Documentation

---

# Knowledge Source Selection

The chatbot automatically selects the correct source based on the customer's product and request.

### Laptop Queries

Sources Used

- Lenovo User Guide
- Lenovo Support Website

---

### Printer Queries

Sources Used

- HP User Guide
- HP Support Website

---

### Warranty Queries

Sources Used

- NovaCare Limited Warranty Policy

---

### Safety Queries

Sources Used

- Product Safety and Escalation Policy

---

# Retrieval Strategy

The chatbot uses Retrieval-Augmented Generation (RAG).

The retrieval process follows these steps:

1. Receive the customer's question.
2. Identify the product type and topic.
3. Select the appropriate knowledge source.
4. Retrieve relevant content from the configured documents.
5. Generate a grounded response based only on the retrieved information.
6. Return the response to the customer.

If relevant information cannot be retrieved, the chatbot informs the customer that the requested information is unavailable rather than generating unsupported content.

---

# Grounding Rules

To improve response quality, the chatbot follows these rules:

- Use only configured knowledge sources.
- Do not invent specifications.
- Do not invent warranty rules.
- Do not generate unsupported troubleshooting steps.
- Clearly indicate when information is unavailable.
- Keep technical guidance separate from warranty policy.
- Do not mix Lenovo and HP documentation.

---

# Source Restrictions

The chatbot does **not** use:

- Community forums
- Blogs
- Social media
- Third-party repair websites
- User-generated content
- Unofficial product manuals
- AI-generated technical articles
- Unverified documentation

Only official manufacturer documentation and approved NovaRetail policies are considered valid.

---

# Benefits of the Knowledge Architecture

The configured knowledge sources provide several advantages:

- Accurate product information
- Reliable troubleshooting
- Consistent warranty guidance
- Reduced hallucinations
- Source-grounded responses
- Improved customer trust
- Better maintainability
- Clear separation between technical and policy information

---

# Maintenance

Knowledge sources should be reviewed and updated whenever:

- A new supported product is added.
- Manufacturer documentation changes.
- NovaCare warranty policies are revised.
- Product safety procedures are updated.
- Product support scope changes.

Keeping the knowledge base current ensures that customers continue to receive accurate and policy-compliant responses.

---

# Conclusion

The Product Support and Warranty Assistant uses a structured Retrieval-Augmented Generation (RAG) architecture built on official manufacturer documentation and NovaRetail policy documents. By restricting responses to approved knowledge sources and enforcing clear source priorities, the chatbot delivers accurate, consistent, and safe customer support while minimizing the risk of hallucinations or unsupported recommendations.