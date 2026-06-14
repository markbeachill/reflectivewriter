# Customising prompt libraries

A short guide for developers, teachers, placement leads and departments who want
a smaller or locally tailored reflective-writing library — without breaking the
core *tutor, not ghost-writer* design.

Most writers should use the official mini libraries or the master library as they
are. Customise only if you have a specific local need.

## Two ways to customise

**1. Edit the source and rebuild (recommended).**
The libraries are generated from `src/prompt-library/` (see `PROMPTS.md`). To make
a tailored library:

1. Copy an existing pack YAML in `src/prompt-library/packs/`, e.g.
   `cp packs/nhs-healthcare.yml packs/my-trust.yml`.
2. Edit the new file: give it a new `id`, `title`, `latest_output` and
   `archive_output`, and list only the `tools:` you want.
3. Add your local guidance. The cleanest place is a new shared file, e.g.
   `shared/03-local-rules.md`, added to the pack's `sections:` after
   `01-global-rules.md`. Keep, never weaken, the authorship, privacy and
   anonymisation rules.
4. Run `python scripts/build_prompt_libraries.py`.

Because every tool already works with the shared rules, you are only choosing
which tools to include and adding local notes — not writing new behaviour.

**2. Delete down from a built file (no tools needed).**
If you cannot run the build, open a generated file such as
`docs/prompt-libraries/latest/reflective_writing_tutor_master_library.md`. It is
one file made of marked sections:

```
<!-- FILE: some-tool.md -->
...
<!-- END FILE -->
```

To slim it down:

1. Delete the whole `<!-- FILE: ... -->` ... `<!-- END FILE -->` block for each
   tool you do not want.
2. Remove the matching line from the launcher menu and the router mapping so the
   menu still matches the tools.
3. Add any local rules as a short paragraph inside the global-rules section.

## What you must not remove

- The activation/header and the menu-source rule.
- The global rule that the reflection must be the writer's own (no inventing
  experiences, feelings, insight or learning).
- The confidentiality, anonymity and privacy rules.
- The wellbeing guidance.

These are what make the toolkit safe to put in front of writers. Removing them
turns it into a generic text generator, which is exactly what it is designed not
to be.

## Before you share a custom library

- Test it yourself with a real (anonymised) reflection.
- Check it still refuses to write a reflection on request.
- Confirm it fits your course, placement, employer or regulator rules,
  especially for assessed work.
