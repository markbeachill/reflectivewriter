# PROMPTS.md — developer guide to the prompt source

The downloadable libraries in `docs/prompt-libraries/` are **generated**. The
source of truth is the file-based layout under `src/prompt-library/`. Edit the
source, then run the build; never hand-edit the generated Markdown.

This layout mirrors the AI Personal Tutor Toolkit reference repository.

## Source layout

```
src/prompt-library/
  header.md                         Activation instruction placed at the top of every library
  shared/
    01-global-rules.md              The no-ghost-writing ethic + global rules (applied by every tool)
    02-markdown-output-rules.md     How to emit a clean Markdown document on request
  tools/
    <id>.md                         One self-contained file per tool (30 of them)
  tool-metadata.json                Canonical codes, titles, families, descriptions, aliases
  pack-sections/
    <pack>/00-manifest.md           Literal manifest text with {{AVAILABLE_TOOLS_TABLE}}
    <pack>/03-launcher.md           Literal launcher text with {{LAUNCHER_MENU}}
    <pack>/04-router.md             Literal router text with {{MENU_MAPPING}}
    master/...                      The same three sections for the master library
  section-markers/
    <family>-tools.md               Group dividers inserted between families in the master file
  packs/
    <pack>.yml                      Which sections + tools make up each library, and where it is written
    master.yml
  release.yml                       Version stamp
```

## How a library is assembled

`scripts/build_prompt_libraries.py` reads a pack YAML and concatenates, in order:

1. `header.md`
2. each file listed under `sections:` (manifest, global-rules, markdown-rules, launcher, router)
3. each file listed under `tools:` (the tool bodies, and section-markers for the master)

While assembling, three placeholders are filled from `tool-metadata.json`:

| Placeholder | Filled with |
| --- | --- |
| `{{AVAILABLE_TOOLS_TABLE}}` | The manifest table (grouped by family in the master). |
| `{{LAUNCHER_MENU}}` | The numbered launcher menu (grouped by family in the master). |
| `{{MENU_MAPPING}}` | The router's alias-to-tool mapping. |

For mini libraries, each tool's `menu_number` front-matter is renumbered to its
position in that pack. The output is written to both `latest_output` and
`archive_output`, and the five mini libraries are zipped.

## A pack file

```yaml
id: nhs-healthcare
title: "NHS and Healthcare Reflection Tutor Library"
latest_output: docs/prompt-libraries/latest/03_nhs_healthcare_reflection_library.md
archive_output: docs/prompt-libraries/v1.0/03_nhs_healthcare_reflection_library_v1_0.md
tool_metadata_mode: mini          # "mini" renumbers menu_number; "master" leaves it
sections:
  - pack-sections/nhs-healthcare/00-manifest.md
  - shared/01-global-rules.md
  - shared/02-markdown-output-rules.md
  - pack-sections/nhs-healthcare/03-launcher.md
  - pack-sections/nhs-healthcare/04-router.md
tools:
  - tools/nmc-revalidation-account.md
  - tools/placement-reflection.md
  - ...
```

## A tool file

Each `tools/<id>.md` is a complete prompt section: a `<!-- FILE: id.md -->`
marker, YAML front-matter, a heading, and the tutoring script, ending with
`<!-- END FILE -->`.

```markdown
<!-- FILE: so-what-deepener.md -->
---
id: so-what-deepener
tool_code: RF2
title: So-What Deepener
type: tool
menu_number: 2
run_policy: selected_only
interaction_type: interactive tutoring
---

# RF2 — So-What Deepener v1.0

Apply `global-rules`. Run only this tool.

Tool contract: interactive tutoring. ...
<!-- END FILE -->
```

## tool-metadata.json

One entry per tool drives the generated tables, menus and routing:

```json
{
  "id": "so-what-deepener",
  "code": "RF2",
  "title": "So-What Deepener",
  "family": "reflective-foundations",
  "family_label": "Reflective Foundations tools",
  "mini_family_label": "Reflective foundations tools",
  "master_manifest_description": "turn 'what happened' into 'what it meant and why it matters'",
  "mini_manifest_description": "turn 'what happened' into 'what it meant and why it matters'",
  "launcher_description": "move from describing the event to analysing why it mattered.",
  "aliases": ["2", "RF2", "So-What Deepener", "So What Deepener"],
  "interaction_type": "interactive tutoring"
}
```

The `family` must be one of the five in `FAMILY_ORDER` inside the build script.

## The rules every tool must follow

Tool bodies inherit `shared/01-global-rules.md`. In particular a tool must
**never** write the writer's reflection, or invent what happened, how they felt,
what they realised, or what they learned. It questions, diagnoses, teaches with a
made-up example on different content, sets one task, and reviews the attempt.
Anonymisation is treated as central because reflections involve real people.

## Editing workflow

1. Edit a tool file in `tools/`, a shared rule in `shared/`, or pack/section text.
2. If you changed codes, titles, descriptions, order or aliases, update
   `tool-metadata.json` to match.
3. Rebuild and verify:
   ```bash
   python scripts/build_prompt_libraries.py
   python scripts/build_prompt_libraries.py --check
   ```
4. Rebuild the site if tool names or examples changed:
   ```bash
   python scripts/build_site_main.py
   python scripts/build_site_pages.py
   python scripts/build_examples.py
   ```

## Adding a tool

1. Create `tools/<new-id>.md` following the format above.
2. Add its entry to `tool-metadata.json`.
3. Add `- tools/<new-id>.md` to the relevant pack YAML and to `master.yml`
   (after the right `section-markers/<family>-tools.md`).
4. Add a worked example to `EXAMPLES` in `scripts/build_examples.py`.
5. Rebuild. The manifest, launcher and router update automatically.

See `CUSTOMISING_PROMPTS.md` for tailoring a local version without editing the
core design.
