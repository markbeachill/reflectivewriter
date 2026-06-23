# Prompt library

Prompt-library source lives under:

```text
src/prompt-library/
```

The generated prompt libraries live under:

```text
docs/prompt-libraries/latest/
docs/prompt-libraries/v1.0/
```

## Important source files

```text
header.md                 Activation instruction for every library.
shared/*.md               Global rules, Markdown output rules, help/EAL behaviour.
tools/*.md                One complete tool prompt per file.
tool-metadata.json        Canonical tool codes, titles, families, descriptions, aliases and tool modes.
pack-sections/**          Manifest, launcher and router text for master and mini libraries.
section-markers/*.md      Group dividers inserted into the master library.
packs/*.yml               Which sections and tools make each generated library.
release.yml               Version and last-updated metadata.
```

## Build commands

```bash
python scripts/build_prompt_libraries.py
python scripts/build_prompt_libraries.py --check
python scripts/build_prompt_libraries.py --ci
```

## Tool metadata

Every tool has both source-file front matter and a `tool-metadata.json` entry. These must agree on:

```text
id
tool_code / code
title
tool_mode
```

Allowed `tool_mode` values are:

```text
routing_helper
interactive
full_review
tiered_review
```

`interaction_type` remains a human-readable description. `tool_mode` is the canonical behaviour category for validation and future automation.

## Routing

The master library uses family-first routing:

```text
A. Reflective Foundations
B. Reflective Frameworks
C. NHS & Healthcare
D. Medical
E. US & Academic
```

Direct tool codes such as `RF2`, `FW1`, `NH4`, `MD3` and `US1` should still work. `list tools` exposes the full master numbered list.

Mini libraries use local 1–6 menus.

## Boundary rule

Every tool must preserve the authorship boundary. It may diagnose, question, teach using unrelated examples and review the writer's own attempt. It must not write the reflection, invent experience, feelings, insight or learning, or produce a polished submission.


For a full repository rebuild/check, use `python scripts/build_all.py` followed by `python scripts/build_all.py --check`.
