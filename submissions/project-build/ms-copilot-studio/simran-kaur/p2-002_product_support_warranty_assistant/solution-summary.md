# Solution Summary

## Business Problem

Customers often require assistance with product troubleshooting, warranty-related queries, and safety concerns. Traditional support processes require customers to manually explain their issue, while support agents spend significant time collecting basic information before providing assistance. This can increase response times and lead to inconsistent customer experiences.

The NovaCare Product Support and Warranty Assistant addresses this problem by providing a structured conversational interface that guides customers through product support, performs a preliminary warranty assessment, identifies safety-critical situations, and recommends the appropriate service route using official documentation and company policies.

---

# Users

The primary users of this solution are:

* Customers seeking technical support for supported Lenovo laptops and HP printers.
* Customers requesting a preliminary warranty eligibility assessment.
* Customer support representatives who require a structured summary of customer interactions.
* Warranty specialists reviewing escalated cases.

---

# Product Portfolio

The chatbot currently supports the following products:

### Lenovo

* ThinkPad Laptop Series

### HP

* LaserJet Printer Series

If an unsupported product or model is provided, the assistant informs the customer that official guidance is unavailable and recommends contacting an authorized support representative.

---

# Scope

The chatbot is designed to provide an initial level of customer support by:

* Answering product-related questions using grounded knowledge.
* Guiding customers through approved troubleshooting procedures.
* Performing product safety assessments.
* Conducting a preliminary warranty eligibility assessment.
* Recommending an appropriate service route.
* Generating a structured support case summary.

The solution is intentionally limited to an initial assessment and does not replace authorized service engineers or warranty specialists.

---

# Capabilities

The assistant provides the following capabilities:

* Product information retrieval from official knowledge sources.
* Guided troubleshooting for supported products.
* Continuous safety assessment during troubleshooting.
* Preliminary warranty eligibility assessment.
* Warranty coverage evaluation.
* Warranty exclusion identification.
* Dead-on-arrival (DOA) assessment.
* Repeat repair assessment.
* Service route recommendation.
* Cross-topic navigation between troubleshooting and warranty assessment.
* Structured support case summary generation.
* Customer confirmation and correction workflow.

---

# Knowledge Architecture

The chatbot uses multiple grounded knowledge sources to ensure accurate and policy-compliant responses.

### Internal Knowledge Sources

* NovaCare Limited Warranty Policy
* Product Support Scope
* Product Safety and Escalation Policy

### Official Product Documentation

* Lenovo Laptop User Manual (PDF)
* HP Printer User Manual (PDF)

### Official Public Websites

* Lenovo Support
* HP Support

Knowledge precedence is implemented to ensure that:

1. Product Safety and Escalation Policy has the highest priority.
2. NovaCare Limited Warranty Policy governs warranty-related decisions.
3. Official product manuals provide technical guidance.
4. Official manufacturer websites supplement product information when required.

---

# Topics

The chatbot is organized into two primary topics and reusable subtopics.

### Topic 1 – Guided Product Troubleshooting and Safety Triage

This topic assists customers in diagnosing issues with supported products using approved troubleshooting procedures while continuously monitoring for safety-related conditions.

### Topic 2 – Preliminary Warranty Eligibility Assessment

This topic collects warranty-related information, validates customer inputs, evaluates warranty rules, determines a preliminary warranty classification, and recommends an appropriate service route.

### Reusable Subtopics

* Product Safety Assessment
* Support Case Summary

These subtopics are shared across multiple conversation flows to improve consistency and reduce duplication.

---

# Safety Controls

Customer safety is the highest priority throughout the conversation.

The chatbot continuously monitors for safety-critical conditions including:

* Smoke
* Fire
* Burning smell
* Swollen battery
* Electric shock
* Excessive heat
* Liquid damage
* Exposed wiring

If a hazardous condition is detected, the chatbot immediately stops routine troubleshooting, provides appropriate safety guidance, and recommends escalation to authorized service personnel.

---

# Decision Boundaries

The chatbot operates within clearly defined business boundaries.

It does not:

* Approve or reject warranty claims.
* Guarantee repairs or replacements.
* Create or update support cases.
* Access live warranty databases.
* Retrieve live repair status.
* Provide legal advice.
* Generate unsupported product information.

Whenever sufficient information is unavailable, the assistant requests additional details instead of making assumptions.

---

# Implementation Decisions

The solution was implemented using Microsoft Copilot Studio with a structured topic-based conversation design.

Key implementation decisions include:

* Using standard Copilot Studio conversation nodes instead of Adaptive Cards.
* Separating troubleshooting and warranty assessment into independent topics.
* Creating reusable subtopics for Product Safety Assessment and Support Case Summary.
* Implementing variable-driven conversation flow with nested conditional logic.
* Using cross-topic redirection to avoid collecting the same information multiple times.
* Applying knowledge precedence to ensure warranty decisions follow NovaCare policy while technical guidance comes from official manufacturer documentation.
* Using grounded knowledge sources to minimize hallucinations and improve response accuracy.
* Ensuring every warranty assessment remains preliminary and policy-compliant.
