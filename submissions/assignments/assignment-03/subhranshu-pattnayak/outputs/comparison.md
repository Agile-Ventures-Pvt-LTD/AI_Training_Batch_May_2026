# Baseline vs HyDE Retrieval Comparison

This evaluation compares the standard vector retrieval baseline with HyDE retrieval across four hypothetical-question prompts. In `main.ipynb`, each method retrieves five document chunks, generates an answer, and stores the HyDE answer as the final answer.

Note: the notebook's `comparison_with_baseline` field says "chunks," but the recorded values are produced with `len()` on the joined context strings. They are therefore character counts, not the number of retrieved chunks.

## Summary

HyDE generally produced stronger answers for these broad, analyst-style questions because the generated hypothetical questions helped retrieve sections that matched the user's implied information need, not just the literal query terms. It was most useful for risk-factor synthesis, product-defect analysis, and cash-flow evidence. The baseline was competitive, and in HQ4 it was more focused on the formal cybersecurity disclosure because the user's wording already overlapped strongly with the target section.

Overall recommendation: use HyDE as the default final-answer retrieval path for this benchmark, but keep the baseline as a diagnostic comparator. For keyword-explicit questions like HQ4, baseline retrieval can be equally strong or more concise.

## Question-Level Results

| Question | Baseline context chars | HyDE context chars | Better answer | Rationale |
|---|---:|---:|---|---|
| HQ1 | 7,004 | 8,048 | HyDE | HyDE retrieved directly relevant risk-factor passages on production-ramp delays, supply chain disruption, legal/regulatory exposure, COVID-related disruptions, new-facility construction, delivery logistics, and service capacity. The baseline answer was directionally useful but included some less-targeted governance and credibility material. |
| HQ2 | 6,843 | 8,422 | HyDE | HyDE centered the answer on product defects, warranty/service costs, customer satisfaction, recalls, liability, and brand harm. The baseline focused heavily on warranty reserve audit procedures, which was useful for the warranty dimension but narrower than the full question. |
| HQ3 | 4,645 | 6,303 | HyDE | HyDE connected capex forecasts, actual investing cash outflows, working-capital management, and operating cash generation. The baseline gave the right evaluation framework but with fewer concrete data points. |
| HQ4 | 8,276 | 7,703 | Baseline slightly stronger | Both methods retrieved cybersecurity-relevant material. The baseline answer was more focused on Item 1A, Item 1C, governance, third-party risk, incident response, and ISO certification. HyDE added confidentiality and general investigation material, which broadened coverage but slightly diluted precision. |

## Method Observations

- HyDE improved semantic recall for broad questions where the user implied a category of evidence rather than naming the exact disclosure heading.
- Baseline retrieval performed best when the query terms already matched the document vocabulary, especially for explicit cybersecurity/data-risk language.
- HyDE answers tended to be longer and more structured; this helped in HQ1-HQ3, but in HQ4 the shorter baseline answer was more targeted.
- The generated hypothetical questions were useful because they mapped user intent to likely annual-report language such as "risk factors," "warranty claims," "cash flows from operating activities," and "cybersecurity risk management."

## Final Conclusion

HyDE should remain the primary answer path for this hypothetical-question evaluation because it wins on three of four questions and better handles indirect, conceptual prompts. The main exception is keyword-explicit retrieval, where baseline similarity search can retrieve the most direct disclosure with less noise.
