# PROMPTS.md — developer guide to the prompt source

The downloadable libraries in `docs/prompt-libraries/` are **generated**. The
source of truth is the file-based layout under `src/prompt-library/`. Edit the
source, then run the build; never hand-edit the generated Markdown.

This layout mirrors the AI Personal Tutor Toolkit reference repository.


## Maintainer documentation

General build and update guidance lives outside this prompt-source guide:

```text
BUILD_AND_GENERATOR_GUIDE.md      Canonical build commands, build_all runner and generated-output map.
UPDATE-CHECKLISTS.md              Step-by-step checklists for common updates.
CONTRIBUTING.md                   Short safe contribution workflow.
SOURCE_MATERIAL_INDEX_EXPLAINER.md  Source-material item format and safety rules.
project-docs/                     Current maintainer documentation by topic.
```

Use this file for the prompt-source format. Use the maintainer docs for build order,
release checks and generated-file rules.

## Source layout

```
src/prompt-library/
  header.md                         Activation instruction placed at the top of every library
  shared/
    01-global-rules.md              The no-ghost-writing ethic + global rules (applied by every tool)
    02-markdown-output-rules.md     How to emit a clean Markdown document on request
    05-help-system.md               Help, stuckness and EAL support rules
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
src/examples/items/                 Worked-example source records
src/audit-library/                  Audit/testing-pack source records
src/source-material/items/          Copy-ready practice-passage source records
```

## How a library is assembled

`scripts/build_prompt_libraries.py` reads a pack YAML and concatenates, in order:

1. `header.md`
2. each file listed under `sections:` (manifest, global-rules, markdown-rules, launcher, router)
3. each file listed under `tools:` (the tool bodies, and section-markers for the master)

While assembling, placeholders are filled from `tool-metadata.json`:

| Placeholder | Filled with |
| --- | --- |
| `{{AVAILABLE_TOOLS_TABLE}}` | The manifest table (grouped by family in the master). |
| `{{LAUNCHER_MENU}}` | The mini-library menu, or the A–E family menu in the master. |
| `{{MASTER_FAMILY_MENUS}}` | Master-library A–E family menus with local 1–6 numbering. |
| `{{MASTER_FULL_TOOL_MENU}}` | Master-library full grouped 1–30 tool list for `list tools`. |
| `{{NUMBER_ROUTING_TABLE}}` | Master-library full-number routing table. |
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
tool_mode: interactive
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
  "interaction_type": "interactive tutoring",
  "tool_mode": "interactive"
}
```

The `family` must be one of the five in `FAMILY_ORDER` inside the build script.

`interaction_type` is the older human-readable behaviour description and is kept for continuity.
`tool_mode` is the canonical behaviour category used by generators, future site data and checks.
Allowed values are:

| `tool_mode` | Meaning |
| --- | --- |
| `routing_helper` | Helps the writer choose a tool, model or next route. It does not review or draft a full reflection. |
| `interactive` | Coaches through questions, short diagnosis, teaching examples on unrelated content, and review of the writer's own attempt. |
| `full_review` | Gives a structured diagnostic review of the writer's own text, then returns to one focused next step. It must not rewrite. |
| `tiered_review` | Starts with a short priority summary and offers expansion, so review feedback does not overwhelm the writer. |

Every tool source file and its `tool-metadata.json` entry must use the same `tool_mode`.
The prompt-library build now validates this before generating outputs.

## The rules every tool must follow

Tool bodies inherit `shared/01-global-rules.md`. In particular a tool must
**never** write the writer's reflection, or invent what happened, how they felt,
what they realised, or what they learned. It questions, diagnoses, teaches with a
made-up example on different content, sets one task, and reviews the attempt.
Anonymisation is treated as central because reflections involve real people.

## Worked example system

Worked examples are generated from structured YAML records in `src/examples/items/`.
The generator is `scripts/build_examples.py`; it validates that every tool has an
example source and that every public example has privacy and authorship checks.

Supporting files:

```text
src/examples/README.md
src/examples/example-schema.md
src/examples/items/*.yml
docs/guides/creating-examples.html
```

Public examples should normally be fictional or composite. They must show the AI
teaching a reflective move, not writing the reflective submission. If a source
record contains any uncertainty about privacy or authorship, keep it as `draft`
or `internal` until it has been manually reviewed.


## Audit/testing pack

The lightweight Reflective Writer testing pack is generated from source files in
`src/audit-library/`. It focuses on reflective-writing-specific risks: ghost-writing,
invented feelings or learning, anonymisation and jigsaw identification, venting or
blame tone, EAL support, framework box-ticking, routing and local-rule uncertainty.

Supporting files:

```text
src/audit-library/audit-pack.yml
src/audit-library/files/reflective_writer_audit_prompt_with_menu.md
src/audit-library/files/reflective_writer_output_collector.md
src/audit-library/files/reflective_writer_test_cards.md
src/audit-library/files/reflective_writer_test_log_template.md
src/audit-library/files/reflective_writer_testing_guide_for_educators.md
docs/audit-library/latest/
docs/audit-library/v1.0/
docs/testing.html
```

Build and check it with:

```bash
python scripts/build_audit_pack.py
python scripts/build_audit_pack.py --check
python scripts/build_audit_pack.py --validate
python scripts/build_audit_pack.py --ci
```

Do not use real student, patient, service-user, colleague or placement details in
test cards or test logs. Use fictional, composite or placeholder material only.

## Generated site data

Structured JSON under `docs/data/` is generated from the same source files as the
prompt libraries, examples and source-material library. Do not hand-edit these
files.

```text
docs/data/release.json
docs/data/tool_index.json
docs/data/prompt_library_packs.json
docs/data/source_material_index.json
```

The generator is:

```bash
python scripts/build_site_data.py
python scripts/build_site_data.py --check
python scripts/build_site_data.py --validate
```

`release.json` reads `src/prompt-library/release.yml`, preserving the existing
release metadata location. `tool_index.json` combines `tool-metadata.json`, tool
source paths, pack inclusion, worked-example links and source-material links.
`prompt_library_packs.json` summarises the master and mini libraries.
`source_material_index.json` is now produced through the shared source-material
index function so the site-data build and source-material build stay aligned.

## Editing workflow

1. Edit a tool file in `tools/`, a shared rule in `shared/`, or pack/section text.
2. If you changed codes, titles, descriptions, order, aliases or `tool_mode`, update
   `tool-metadata.json` to match.
3. Rebuild and verify:
   ```bash
   python scripts/build_prompt_libraries.py
   python scripts/build_prompt_libraries.py --check
   ```
4. Rebuild and check the full generated set when tool names, guide pages, examples, site data or audit materials might be affected:
   ```bash
   python scripts/build_all.py
   python scripts/build_all.py --check
   ```
   For CI-style validation before committing or release, run:
   ```bash
   python scripts/build_all.py --ci
   ```

## Adding a tool

1. Create `tools/<new-id>.md` following the format above.
2. Add its entry to `tool-metadata.json`, including the canonical `tool_mode`.
3. Add `- tools/<new-id>.md` to the relevant pack YAML and to `master.yml`
   (after the right `section-markers/<family>-tools.md`).
4. Add a worked example YAML record in `src/examples/items/`, following `src/examples/example-schema.md`.
5. Rebuild. The manifest, launcher and router update automatically.

See `CUSTOMISING_PROMPTS.md` for tailoring a local version without editing the
core design.
