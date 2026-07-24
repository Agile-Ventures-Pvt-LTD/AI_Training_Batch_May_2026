
# Knowledge Sources Documentation

# P2-002 Product Support and Warranty Assistant

---

# 1. Overview

The Product Support and Warranty Assistant uses grounded knowledge sources in Microsoft Copilot Studio to ensure responses are based on approved enterprise information.

Knowledge grounding helps the assistant provide:

- Accurate troubleshooting guidance
- Consistent warranty information
- Safe customer instructions
- Policy-compliant responses

The assistant does not rely only on general generative AI knowledge. Instead, it uses configured knowledge sources to retrieve relevant information before generating responses.

---

# 2. Knowledge Source Strategy

The knowledge architecture follows a policy-first approach.

```

```
             Customer Query

                   |

                   v

          Copilot Studio Agent

                   |

                   v

          Knowledge Retrieval

                   |

    --------------------------------

    |              |               |

    v              v               v
```

Warranty Policy   Product Support   Safety Policy

```
    |

    v
```

Grounded AI Response

```

---

# 3. Connected Knowledge Sources

The solution uses the following enterprise knowledge documents:

| Knowledge Source | Purpose |
|---|---|
| NovaCare Limited Warranty Policy | Warranty rules, coverage, exclusions |
| Product Support Scope | Supported products and troubleshooting scope |
| Product Safety and Escalation Policy | Safety checks and escalation rules |

---

# 4. Knowledge Source 1: NovaCare Limited Warranty Policy

## File

```

novacare-limited-warranty-policy.md

```

---

## Purpose

Defines warranty-related business rules and assessment guidelines.

---

## Covers

### Warranty Coverage

- Applicable warranty duration
- Product category coverage
- Coverage limitations

---

### Dead-on-Arrival Assessment

Defines:

- Eligibility conditions
- Seven-day reporting window
- Required information
- Assessment limitations

---

### Warranty Exclusions

Includes:

- Accidental damage
- Liquid damage
- Electrical surge
- Unauthorized repair
- Unauthorized modification
- Consumables
- Normal wear and tear

---

### Repeat Repair Handling

Defines:

- Previous repair scenarios
- Escalation requirements
- Review process

---

# 5. Knowledge Source 2: Product Support Scope

## File

```

product-support-scope.md

```

---

## Purpose

Defines supported products, models, and troubleshooting boundaries.

---

## Supported Laptop

Manufacturer:

Lenovo

Model:

Lenovo ThinkPad E14 Gen 5

Supported Issues:

- No Power
- Charging Failure
- Battery Drain
- Blank Display
- External Display
- Overheating
- Wi-Fi Problems
- Keyboard Problems
- Touchpad Problems

---

## Supported Printer

Manufacturer:

HP

Model:

HP LaserJet Pro MFP M428-M429

Supported Issues:

- Printer Offline
- Paper Jam
- Poor Print Quality
- Network Connectivity
- Scan Failure
- Toner Warning
- Error Messages
- No Power

---

## Purpose of Validation

The document helps the agent:

- Identify supported products
- Avoid unsupported model instructions
- Route unsupported cases correctly

---

# 6. Knowledge Source 3: Product Safety and Escalation Policy

## File

```

product-safety-and-escalation-policy.md

```

---

## Purpose

Defines safety detection rules and mandatory escalation behavior.

---

## Safety Indicators

The agent checks for:

- Smoke
- Sparks
- Burning smell
- Electric shock
- Excessive heat
- Liquid exposure
- Battery swelling

---

## Safety Classification

Cases are classified as:

### Safe to Continue

Normal troubleshooting can proceed.

---

### Safety Critical

Normal troubleshooting must stop.

The assistant must:

- Provide safety instructions
- Avoid asking the customer to reproduce the issue
- Assign required escalation level

---

# 7. Grounding Approach

The assistant follows this process:

## Step 1: User Input

Customer describes an issue.

Example:

"My laptop is not charging."

---

## Step 2: Context Identification

The agent identifies:

- Product type
- Issue category
- Required knowledge area

---

## Step 3: Knowledge Retrieval

Relevant information is retrieved from:

- Product support documents
- Safety policies
- Warranty policies

---

## Step 4: Response Generation

The assistant generates a response based on retrieved information.

---

# 8. Knowledge Usage by Topic

| Topic | Knowledge Used |
|---|---|
| Troubleshooting | Product Support Scope + Safety Policy |
| Safety Assessment | Safety and Escalation Policy |
| Warranty Assessment | Warranty Policy |
| Product Validation | Product Support Scope |
| Case Summary | All relevant sources |

---

# 9. Grounding Rules

The assistant must:

✔ Use approved knowledge sources

✔ Follow defined policies

✔ Avoid unsupported assumptions

✔ Provide preliminary assessments only

✔ Escalate when required

---

The assistant must not:

✘ Approve warranty claims

✘ Guarantee replacement

✘ Provide unsafe troubleshooting

✘ Override safety policies

✘ Provide unsupported product instructions

---

# 10. Knowledge Maintenance

Future updates should include:

- New supported products
- Updated warranty policies
- Updated safety procedures
- Additional troubleshooting guides

Knowledge files should be reviewed periodically to maintain response accuracy.

---

# 11. Conclusion

The knowledge source architecture ensures that the Product Support and Warranty Assistant provides safe, accurate, and policy-aligned customer support while maintaining enterprise control over generated responses.
```

---
