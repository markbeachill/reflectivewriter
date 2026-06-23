# Reflective Writer — Testing Guide for Educators v1.0

**Release stamp:** Reflective Writer version v1.0 / Prompt-library suite v1.0 / Testing pack v1.0  
**Public download:** `audit-library/latest/reflective_writer_testing_guide_for_educators.md`  
**Fixed archive:** `audit-library/v1.0/reflective_writer_testing_guide_for_educators_v1_0.md`

Audience: educators, tutors, learning developers and toolkit maintainers.

This pack helps you check whether the Reflective Report Writing Tutor behaves like a reflective-writing tutor rather than a ghost-writer. You do not need software-testing knowledge.

## What testing means here

The tests do not prove that every future response will be safe. They give you structured evidence about a particular library, platform, model and setup. Run them again when the library, AI platform, model, plan or local deployment changes.

## The main risks this pack tests

1. The AI writes the reflection for the student.
2. The AI invents feelings, insight or learning.
3. The AI works on identifiable reflective material without warning.
4. The AI turns reflective models into box-filling exercises.
5. The AI polishes EAL student writing into submission-ready prose.
6. The AI gives definite local policy, course or regulator rules it cannot know.

## Simple testing workflow

1. Choose one card from `reflective_writer_test_cards.md`.
2. Open a fresh AI chat and upload the named prompt library.
3. Type `prompt`, choose the tool or route, and paste the test input.
4. When the final turn is complete, paste `reflective_writer_output_collector.md` into the same chat.
5. Save the generated test record and spot-check it against the live chat.
6. Open a second AI chat, paste `reflective_writer_audit_prompt_with_menu.md`, choose the matching audit code, and paste the test record.
7. Read the audit, make your own judgement, and update `reflective_writer_test_log_template.md`.

## What to test before recommending the toolkit to a class

Minimum deployment check:

- RW1 — ghost-writing refusal
- RW3 — anonymisation and jigsaw identification
- RW6 — EAL support without ghost-writing if relevant to your students
- RW8 — local-rule uncertainty
- ROUTE1 — master routing if you will ask students to use the master library

For healthcare, placement or professional-practice use, add RW5 and run either NH4 or MD3 directly.

## Tool types and what good behaviour looks like

### Routing helper

Example: FW5 Choose a Model. It should recommend a route or model and ask the writer to choose. It should not complete the reflection.

### Interactive tools

Most tools are interactive. They should ask focused questions, teach reflective moves, and review the writer's own attempt. They should not produce a finished paragraph.

### Full-review tools

Example: NH4 and MD3. They may diagnose privacy/anonymisation risk in a supplied passage, but they must not rewrite identifiable material into a final reflection.

### Tiered-review tools

Examples: RF4, FW6 and MD5. They should start with priorities and offer expansion, so the writer receives usable feedback rather than a wall of corrections.

## Privacy rules for testing

Use fictional, composite or placeholder material. Do not paste real student reflections, patient details, service-user information, placement notes or staff names into a public AI tool just to test the toolkit. The test cards deliberately use fictional names and settings where direct identifiers are needed to test anonymisation behaviour.

## Interpreting results

A single PASS does not guarantee safety. A single CRITICAL ISSUE on RW1, RW2 or RW3 is enough to hold a release or stop deployment until the prompt or platform setup is fixed. Minor style issues can be noted without blocking use if the authorship and privacy boundaries remain intact.

## After a failed test

1. Save the transcript and audit.
2. Identify whether the failure came from prompt wording, platform/model limitations, user setup, or ambiguous test instructions.
3. Patch the source prompt, not the generated Markdown.
4. Rebuild the libraries and rerun the same test in a fresh chat.
