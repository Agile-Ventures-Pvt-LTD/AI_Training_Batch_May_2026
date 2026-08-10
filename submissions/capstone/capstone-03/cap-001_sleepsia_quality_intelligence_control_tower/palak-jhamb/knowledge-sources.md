# Knowledge Sources

## Overview

The Sleepsia Quality & Customer Experience Intelligence Control Tower uses multiple knowledge sources to provide accurate, grounded, and evidence-based responses. The Quality Supervisor and specialist agents retrieve information only from approved enterprise documents and the official Sleepsia website.

---

# Knowledge Sources

## 1. Sleepsia Product Information

**Type:** Public Website

**Purpose:**

Provides official product information used by the Product & Batch Specialist and Customer Impact Specialist.

**URL**

https://sleepsia.com/

**Used For**

- Product specifications
- Mattress and pillow details
- Product features
- Warranty information
- Product categories

---

## 2. Sleepsia Help Center / Support

**Type:** Public Support Website

**Purpose**

Provides customer support policies and product guidance.

**URL**

https://sleepsia.com/pages/contact-us

**Used For**

- Customer support information
- Contact details
- Warranty assistance
- Customer service guidance

---

## 3. Internal Investigation Knowledge Base

**Type:** Uploaded Knowledge Documents

**Purpose**

Contains organization-specific quality investigation rules and documentation uploaded to Microsoft Copilot Studio.

**Includes**

- Product Quality Investigation Guidelines
- CAPA Process Documentation
- Quality Investigation SOPs
- Investigation Decision Rules
- Internal Process Documentation

**Used By**

- Quality Supervisor
- CAPA Specialist
- Safety Specialist
- Product & Batch Specialist

---

# Knowledge Source Precedence

When multiple sources contain relevant information, the following precedence is applied:

| Priority | Knowledge Source | Usage |
|----------|------------------|-------|
| 1 | Internal Investigation Knowledge Base | Investigation rules, CAPA, SOPs, quality decisions |
| 2 | Sleepsia Official Website | Product and warranty information |
| 3 | Sleepsia Support Pages | Customer support and contact information |

The supervisor always prefers internal enterprise documentation over public sources for investigation decisions.

---

# Retrieval Strategy

The agents use Retrieval-Augmented Generation (RAG) to answer questions.

Retrieval process:

1. Receive user request.
2. Search uploaded internal documents.
3. Retrieve relevant information from approved Sleepsia URLs if required.
4. Ground the response using retrieved content.
5. Generate an evidence-based answer.
6. If no relevant information is found, state that the information is unavailable instead of fabricating a response.

---

# Retrieval Test Cases

| Test ID | Query | Expected Result | Status |
|----------|-------|-----------------|--------|
| RT-01 | What is the warranty for Sleepsia products? | Retrieves warranty information from official Sleepsia website. | Passed |
| RT-02 | How is a CAPA created? | Retrieves CAPA workflow from internal knowledge documents. | Passed |
| RT-03 | What are the investigation classification rules? | Retrieves quality decision rules from uploaded investigation documents. | Passed |
| RT-04 | What product features does SLP-1002 have? | Retrieves product information from Sleepsia website. | Passed |
| RT-05 | How should a safety complaint be handled? | Retrieves investigation and safety guidance from internal SOP documents. | Passed |

---

# Knowledge Usage Rules

- Use only approved knowledge sources.
- Prefer internal investigation documents for quality decisions.
- Use official Sleepsia URLs only for public product and support information.
- Never fabricate product details, policies, or investigation outcomes.
- If information cannot be retrieved from an approved source, clearly state that it is unavailable.

---

# Summary

The project uses a hybrid knowledge retrieval approach combining:

- **Internal uploaded investigation documents** for quality processes, SOPs, and CAPA guidance.
- **Official Sleepsia website** for product and warranty information.
- **Official Sleepsia support pages** for customer support guidance.

This ensures all responses remain accurate, grounded, and aligned with enterprise quality investigation policies.