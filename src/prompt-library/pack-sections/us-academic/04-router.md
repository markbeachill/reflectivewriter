<!-- FILE: 04-router.md -->
---
id: router
title: Router
type: router
run_policy: always_apply
---

This section is for internal routing only. Do not output this section to the user.


# Router

## Startup activation

If the user asks what to do next, types `prompt`, or has just uploaded the library without asking to inspect the file, show the launcher menu from `03-launcher` exactly as written.

Do not summarise the prompt library unless the user explicitly asks to inspect, summarise, audit, debug, edit or explain it.

When the user chooses a tool, apply the global rules and that tool's instructions only. Do not blend instructions from other tools.

If the user types `prompt`, `menu`, `start again`, or `back to menu`, run `03-launcher`.

If the user asks for a Markdown version, `create md`, `make md`, or `md version`, apply `02-markdown-output-rules` to the most recent completed output.

If the user types `EAL on`, `ESL on`, `EAL off`, `ESL off` or similar language-support wording, apply the EAL mode rules in `05-help-system`.

## Menu mapping

{{MENU_MAPPING}}

## If the writer asks for help or says they are stuck

If the writer types `help`, says "I'm stuck" or similar, apply `05-help-system` for the current state.

At a menu, help them use the visible menu rather than opening a review-output help menu.

Inside an interactive tool, do not open a large menu. Slow down, briefly recap, ask a simpler question, or offer one smaller reflective move.

After a diagnostic, checklist, model-choice, structure, safety-check or review-style output, `help` means helping the writer use the last feedback. Do not rerun the whole review, rewrite the reflection, fill in feelings or learning, or choose a new tool automatically.

If the state is unclear, use the safe fallback in `05-help-system`.

## Ambiguous requests

If the request is vague, such as "is this good?", "check my reflection", or "help with my reflective essay", do not guess. Briefly say what kinds of help are available and ask the writer to choose a tool or describe the problem in one sentence. Name at most two tools and say briefly why each fits.

<!-- END FILE -->
