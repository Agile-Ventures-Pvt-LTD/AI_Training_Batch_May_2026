# Assignment A003 - Comparative Evaluation & Critical Analysis

## 5. Required Comparative Analysis Matrix

| Question | Baseline Evidence Quality | Improved Evidence Quality | Improvement Observed | Failure Mode |
| :--- | :--- | :--- | :--- | :--- |
| **HQ1** | Low | High | Standard keyword indexing mapped incorrectly to high-level PR statements. Hypothetical matching routed directly to deep legal disclosure items mapping factories and bottlenecks. | Risk of pulling secondary boilerplate risk texts if phrasing matches generic risk descriptions. |
| **HQ2** | Medium | High | Bypassed vocabulary bottlenecks. Standard search missed sections talking about "goodwill impairments" and "accrued expenses" but hypothetical indexes bridged these seamlessly. | Minor precision loss if multiple distinct product issues share similar legal liability paragraphs. |
| **HQ3** | Low | High | Found highly separated accounting statements scattered across tables that did not share overlapping terms with the executive's analytical wording. | Complex cross-referencing can sometimes make answers too verbose if context chunks contain heavy numbers. |
| **HQ4** | Low | High | Resolved the abstract lookup issue perfectly. Mapped queries asking about operational stability to clauses covering backend computational server space vulnerabilities. | Potential for low precision when general infrastructure failures overlap with security events. |

---

## 4.6 Analytical Core Evaluations

### 1. Which queries benefited most from hypothetical question retrieval?
Queries **HQ1** and **HQ4** demonstrated the highest performance lift. These queries are written using high-level corporate vocabulary ("What should a board member ask...", "Which disclosures help evaluate..."). Traditional text embedding structures fail here because 10-K documents are written in legal compliance terminology rather than managerial investigative prose. Generating hypothetical questions created an optimization bridge between these two distinct styles.

### 2. Which generated questions were too broad, too narrow, or misleading?
Questions built from boilerplate legal warnings (e.g., "Our business might face unforeseen external developments") resulted in overly broad hypothetical structures. Conversely, highly granular text rows holding single reporting balance sheets generated questions that were too narrow to catch fluid semantic lookups.

### 3. How did you prevent generated hypothetical questions from introducing unsupported facts?
We applied a multi-tier containment protocol:
1. Engineered strict, closed-loop instructions inside the system execution parameters explicitly denying creative liberties or factual extrapolation.
2. Set the model generation temperature configuration explicitly to `0` to enforce strict deterministic decoding patterns.
3. Designed the execution engine to fall back to a high-capacity parsing framework (`llama-3.3-70b-versatile`) if it caught structure corruption issues during operational loops.

### 4. Did the technique improve retrieval for abstract business questions?
Yes. Abstract corporate logic represents a major point of failure for standard keyword-bound RAG pipelines. By expanding individual text chunks into multiple distinct hypothetical questions representing analytical, risk-oriented, and factual inquiries, we created a rich semantic target space that accurately captures executive intent.

### 5. How would you update the hypothetical question index when new 10-K filings are added?
We would establish an isolated incremental ingestion script. New document arrivals would be passed to the chunk partition module independently. The system would generate hypothetical questions only for those newly minted blocks and append the results into the persistent storage engine using explicit collection parameters (e.g., `{'year': 2026}`). This eliminates the need to re-index the historical archive, cutting down on compute overhead and API costs.