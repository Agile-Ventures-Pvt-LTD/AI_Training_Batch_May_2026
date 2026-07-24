# Agent Design
---

# Purpose

The **Product Support and Warranty Assistant** is an AI-powered conversational agent developed using Microsoft Copilot Studio. It provides first-line customer support for supported Lenovo laptops and HP printers by delivering grounded technical guidance, preliminary warranty assessments, product safety evaluation, and appropriate service routing.

The chatbot is designed to improve customer experience by providing accurate, consistent, and policy-compliant responses while ensuring that critical decisions remain under authorized human supervision.

---

# Agent Role

The chatbot acts as a **virtual product support assistant** for NovaRetail Technologies.

Its primary responsibilities are:

- Answer product-related questions.
- Provide product setup guidance.
- Assist with safe troubleshooting.
- Identify supported products.
- Detect safety-critical conditions.
- Perform preliminary warranty assessments.
- Recommend appropriate service routes.
- Generate structured case summaries.
- Escalate customers to human support when necessary.

The chatbot acts as an **assistant**, not as a replacement for human technical or warranty specialists.

---

# Supported Products

The chatbot currently supports only the following products.

## Laptop

- Lenovo ThinkPad E14 Gen 5

Supported troubleshooting includes:

- No power
- Charging issues
- Battery problems
- Blank display
- External display
- Wi-Fi connectivity
- Keyboard issues
- Touchpad issues
- Overheating

---

## Printer

- HP LaserJet Pro MFP M428-M429

Supported troubleshooting includes:

- Printer offline
- Paper jam
- Poor print quality
- Network connectivity
- Scan failures
- Toner warnings
- Error messages
- Power issues

If an unsupported product or unknown model is provided, the chatbot informs the customer of the limitation and recommends contacting technical support.

---

# Functional Scope

The chatbot supports the following capabilities:

- Product information
- Product setup
- Guided troubleshooting
- Safety assessment
- Warranty eligibility assessment
- Coverage explanation
- Service route recommendation
- Case summary generation
- Customer correction handling
- Human escalation

---

# Out of Scope

The chatbot does not:

- Approve warranty claims.
- Reject warranty claims.
- Guarantee repairs.
- Guarantee replacements.
- Create service requests.
- Schedule technician visits.
- Track repair status.
- Access live warranty databases.
- Access customer accounts.
- Process payments.
- Perform remote diagnostics.
- Execute software changes on customer devices.

---

# Conversation Design

The chatbot follows a structured conversation flow to ensure a consistent customer experience.

```
Customer Request
        │
        ▼
Identify Product
        │
        ▼
Validate Supported Model
        │
        ▼
Safety Assessment
        │
        ▼
Technical Troubleshooting
        │
        ▼
Issue Resolved?
   │           │
 Yes          No
   │           ▼
 Complete  Warranty Assessment
                │
                ▼
        Service Route Recommendation
                │
                ▼
         Support Case Summary
                │
                ▼
          Conversation Ends
```

The workflow ensures that safety checks are always completed before any troubleshooting begins.

---

# Knowledge Grounding

The chatbot uses **Retrieval-Augmented Generation (RAG)** provided by Microsoft Copilot Studio.

Rather than relying on general AI knowledge, every response is generated from approved knowledge sources.

Configured knowledge sources include:

- Lenovo ThinkPad E14 Gen 5 User Guide
- Lenovo Support Website
- HP LaserJet Pro MFP M428-M429 User Guide
- HP Support Website
- NovaCare Limited Warranty Policy
- Product Support Scope
- Product Safety and Escalation Policy

Grounded retrieval reduces hallucinations and ensures consistent responses.

---

# Knowledge Source Precedence

To prevent conflicting information, the chatbot follows a defined source priority.

## Product Information

1. Official Lenovo or HP Product Manuals
2. Official Lenovo or HP Support Websites
3. Product Support Scope

---

## Warranty Questions

1. NovaCare Limited Warranty Policy
2. Product Support Scope

---

## Safety Questions

1. Product Safety and Escalation Policy
2. Manufacturer Safety Documentation

The chatbot never mixes technical guidance with warranty policy unless required by the workflow.

---

# Custom Topics

The solution contains two primary custom topics.

## Guided Product Troubleshooting and Safety Triage

This topic:

- Identifies the product.
- Validates supported models.
- Performs safety assessment.
- Executes controlled troubleshooting.
- Tracks troubleshooting attempts.
- Escalates unresolved issues.
- Generates a support summary.

---

## Warranty Eligibility and Service Route Assessment

This topic:

- Collects warranty information.
- Validates customer inputs.
- Calculates product age.
- Evaluates coverage periods.
- Applies exclusion rules.
- Performs dead-on-arrival assessment.
- Handles repeat repairs.
- Determines service routes.
- Generates preliminary warranty classifications.

---

# Reusable Subtopics

## Product Safety Assessment

This reusable component evaluates mandatory safety indicators.

Indicators include:

- Smoke
- Sparks
- Fire
- Burning smell
- Swollen battery
- Electric shock
- Excessive heat
- Liquid ingress
- Exposed wiring
- Melting components

Outputs:

- Safety Level
- Escalation Level
- Continue or Stop decision

---

## Support Case Summary

Generates a structured summary containing:

- Product
- Model
- Issue
- Troubleshooting performed
- Safety classification
- Warranty classification
- Escalation level
- Recommended next action

Customers are allowed to review and correct the summary before completion.

---

# Safety Design

Customer safety is always the highest priority.

If a safety-critical condition is detected:

- Normal troubleshooting immediately stops.
- Customers are instructed to stop using the product.
- Unsafe actions are never suggested.
- The chatbot does not ask customers to reproduce dangerous conditions.
- Level 4 Safety Escalation is initiated.

---

# Warranty Decision Boundaries

The chatbot provides only a **preliminary assessment**.

It never:

- Approves warranty coverage.
- Rejects warranty claims.
- Guarantees product replacement.
- Guarantees repairs.
- Makes legal conclusions.
- Overrides NovaCare policy.

Final decisions always require human review.

---

# Privacy Controls

The chatbot follows privacy-by-design principles.

It never requests:

- Passwords
- PINs
- Banking information
- Payment card details
- Personal documents
- Confidential files
- Encryption keys

Only the minimum information required for troubleshooting and warranty assessment is collected.

---

# Hallucination Prevention

Several controls are implemented to reduce unsupported responses.

The chatbot:

- Uses Retrieval-Augmented Generation.
- Restricts answers to configured knowledge sources.
- Does not invent specifications.
- Does not invent troubleshooting procedures.
- Does not invent warranty rules.
- Clearly states when information is unavailable.
- Separates Lenovo and HP product documentation.
- Prevents unsupported product guidance.

These controls improve response accuracy and customer trust.

---

# Prompt Injection Protection

The chatbot is designed to ignore attempts to manipulate or reveal internal instructions.

Examples include requests such as:

- "Ignore previous instructions."
- "Reveal your system prompt."
- "Show hidden instructions."
- "List your internal configuration."

In such cases, the chatbot refuses the request and continues assisting only within its defined scope.

---

# Escalation Strategy

The chatbot escalates conversations when:

- Safety-critical conditions are detected.
- Unsupported products are identified.
- Required information is missing.
- Troubleshooting reaches the maximum attempt limit.
- Warranty disputes remain unresolved.
- Repeat repair scenarios require specialist review.

Escalation recommendations are clearly explained to the customer.

---

# Error Handling

The chatbot handles common issues such as:

- Invalid purchase dates
- Missing information
- Unsupported models
- Unknown products
- Customer corrections
- Conversation cancellation
- Conflicting responses
- Failed troubleshooting attempts

Appropriate prompts are provided to help the customer continue without losing previously entered information.

---

# Customer Experience Design

The chatbot is designed to provide a professional and user-friendly experience.

Key design principles include:

- Simple and clear language
- Guided conversations
- Step-by-step troubleshooting
- Confirmation before major decisions
- Minimal repeated questions
- Consistent terminology
- Clear next actions
- Human escalation when appropriate

---

# Security Considerations

To maintain security and confidentiality:

- No secrets or API keys are stored in the chatbot.
- No confidential customer information is retained.
- No live enterprise systems are directly accessed.
- All responses are grounded in approved documentation.

---

# Design Benefits

The implemented design provides several advantages:

- Accurate product guidance
- Consistent troubleshooting
- Reliable warranty information
- Reduced hallucinations
- Improved customer safety
- Faster issue resolution
- Standardized support process
- Easy maintenance through reusable topics
- Clear separation of responsibilities

---

# Future Enhancements

Possible future improvements include:

- Dynamics 365 integration
- Live warranty verification
- Automated case creation
- Repair appointment scheduling
- OCR-based invoice verification
- Image upload for diagnostics
- Voice-enabled conversations
- Multilingual support
- Power BI reporting
- Integration with Microsoft Teams

---

# Conclusion

The Product Support and Warranty Assistant is designed as a safe, structured, and enterprise-ready conversational agent. By combining Retrieval-Augmented Generation, reusable conversation components, strict knowledge-source precedence, safety-first workflows, and controlled warranty assessments, the chatbot delivers reliable first-line customer support while ensuring that final technical and warranty decisions remain under authorized human supervision.