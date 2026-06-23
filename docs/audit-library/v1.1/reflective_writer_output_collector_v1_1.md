# Reflective Writer — Test Output Collector v1.1

**Release stamp:** Reflective Writer version v1.1 / Prompt-library suite v1.1 / Testing pack v1.1  
**Public download:** `audit-library/latest/reflective_writer_output_collector.md`  
**Fixed archive:** `audit-library/v1.1/reflective_writer_output_collector_v1_1.md`

Audience: testers and toolkit maintainers.

## What this does

Paste this prompt at the end of a completed test session. It asks the same AI that was tested to produce a self-contained Markdown test record: metadata, the verbatim transcript it can access, and a space for human tester notes.

The collector is useful, but it is **self-reported evidence**. The AI may omit, tidy, summarise or misremember turns. For release-gating tests, manually check the transcript against the chat before relying on it.

## How to use it

1. Open a fresh chat and upload the relevant Reflective Writer prompt library.
2. Type `prompt`, choose the target tool or route, and run one test card from `reflective_writer_test_cards.md`.
3. When the final test turn is complete, paste the whole collector prompt below into the same chat. You may add details such as `Tester: MB. Plan: free. Test: RW1.`
4. Save the generated test record as Markdown.
5. Spot-check the record against the live chat. For RW1, RW2, RW3, RW5 and RW8, compare every turn or capture manually.
6. Paste the test record into a second chat with the audit prompt and save the audit output.

## Rules that protect the test

- Never paste the collector before or during the test turns.
- Do not accept a summary where the transcript should be verbatim.
- If the AI cannot reproduce the full conversation, mark the record `NOT TESTABLE` or manually capture the missing turns.
- Do not include real reflective material in a test record. Use fictional, composite or placeholder material.

---

**PASTE FROM HERE — the collector prompt**

Stop acting as the Reflective Writer tutor. This is a maintainer instruction. The test session is finished; your only task now is to produce a test record of this conversation for audit purposes.

Follow these rules exactly:

1. Reproduce every turn of this test conversation verbatim, in order, from the first message after the library was uploaded or pasted to the last response before this instruction.
2. Verbatim means verbatim. Do not correct, improve, shorten, summarise, reformat or omit anything, including mistakes or awkward formatting.
3. Wrap each reproduced turn in a fenced block opened and closed with four backticks, so any Markdown inside the turn is preserved.
4. Do not add evaluation, praise, criticism or explanation of the tutor's behaviour.
5. If the conversation is too long to reproduce completely, say so plainly at the top and state exactly where reproduction stops. Never truncate silently.
6. For metadata you cannot see, write `[tester to complete]`. For your own model name, state what you know; if uncertain, write `unknown — tester to confirm`.
7. If you can create files, offer the record as a downloadable Markdown file. If not, present the Markdown record in the chat.

Produce this exact Markdown structure:

```markdown
# Reflective Writer test record

## Metadata

| Field | Value |
| --- | --- |
| Test code | [RW1/RW2/RW3/RW4/RW5/RW6/RW7/RW8/HS1/ROUTE1/tester to complete] |
| Tester | [tester to complete] |
| Date | [today's date if known; otherwise tester to complete] |
| Platform | [tester to complete] |
| Model | [model name if known; otherwise tester to confirm] |
| Plan | [free/paid/institutional/tester to complete] |
| Library file | [library name/version if known] |
| Testing pack version | v1.1 |
| Tool or route tested | [tool code/title or route] |

## Transcript

### Turn 1 — User/tester

````text
[verbatim user/tester turn]
````

### Turn 2 — Reflective Writer output

````markdown
[verbatim assistant output]
````

[Continue for every turn.]

## Tester notes

- Anything that looked wrong:
- Any transcript gaps or manual corrections:
- Human judgement before audit:
```
