# AI Usage Declaration

## AI tools used
Chat GPT was used as a design and debugging assistant throughout the build of this Copilot Studio solution.

## Specific uses
- Interpreting the PRD's mandatory architecture and mapping it onto concrete Copilot Studio constructs (topics, child agents, tools, MCP, triggers).
- Drafting agent/topic instruction text and Description fields, subsequently reviewed and adapted by the participant.
- Designing the decision-precedence branch structure for Topic 2 (Quality Investigation Decision) based on the exact priority rules stated in the PRD.
- Designing the retry/fallback pattern (self-referential topic call with attempt counter) given the platform's lack of a native loop node in classic Topics.
- Debugging a Power Fx table-extraction issue (`First(...).Column` errors) — root-caused to output shape (`.value` nesting) but ultimately not resolved within the available time; the corresponding validation check was simplified to existence-of-row rather than abandoned silently (see known-limitations.md).
- Drafting this documentation set.

## Validation performed by participant
Manually tested every topic branch in the Test panel with real data from the supplied workbook before considering it complete.

## Explicit boundaries respected
No supplier/customer approval, test evidence, screenshots, or notification-sent claims were fabricated by the AI or the participant. All specific numeric values, thresholds, and table/column names used in agent instructions were taken directly from the supplied PRD and workbook, not invented. The participant remains responsible for understanding and being able to explain every orchestration pattern implemented.