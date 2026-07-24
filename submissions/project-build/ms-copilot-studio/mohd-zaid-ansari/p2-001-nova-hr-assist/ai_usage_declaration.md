# AI Usage Declaration

## AI Tools Used

- **Claude (Anthropic)** – Used only as a guide to understand how to build topics and configure the chatbot.
- **Microsoft Copilot Studio – "Add from description"** – Used once to create an initial draft of the Workplace Concern topic.

---

## How AI Was Used

AI was used only for guidance during development. It helped explain how to create topics, conditions, variables, and chatbot instructions. The chatbot, topics, and conversation flow were built and configured manually in Microsoft Copilot Studio.

---

## Manual Validation

The following were checked manually:

- Built and reviewed all topics and conversation flows in Copilot Studio.
- Tested all required test cases (TC-01 to TC-25).
- Verified that answers came from the correct knowledge source.
- Checked that company policy (NovaWorks Addendum) was used whenever there was a conflict.

---

## Changes Made

- Updated the leave topic by creating separate conditions for each leave type instead of using one combined condition.
- Reviewed and improved the Workplace Concern topic to ensure emergency situations are handled first.
- Improved the safety condition to recognize more danger-related words instead of matching only "yes".