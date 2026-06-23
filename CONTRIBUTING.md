# Contributing

Thank you for improving Reflective Writer. This repository is intentionally source-driven: edit source files under `src/` or generators under `scripts/`, then rebuild the generated public outputs under `docs/`.

## Core contribution rule

Reflective Writer must help people write their own reflections. It must not write a reflection for them or invent their experience, feelings, insight, professional judgement or learning.

That rule applies to prompt text, examples, source material and audit tests.

## Safe content rules

Do not commit real identifiable reflective material. Avoid names, rare roles, exact placements, unusual incidents, dates, locations or combinations that could identify a patient, service user, colleague, student, workplace or family member.

Use fictional, composite or placeholder material for:

```text
src/examples/
src/source-material/
src/audit-library/
```

## Common changes

### Change a tool

1. Edit `src/prompt-library/tools/<id>.md`.
2. Update `src/prompt-library/tool-metadata.json` if the title, description, aliases, family or `tool_mode` changed.
3. Rebuild and check:

```bash
python scripts/build_prompt_libraries.py
python scripts/build_prompt_libraries.py --check
python scripts/build_site_data.py
python scripts/build_site_data.py --check
python scripts/build_site_data.py --validate
```

### Change a worked example

1. Edit `src/examples/items/<id>.yml`.
2. Keep public safety checks true.
3. Rebuild and check:

```bash
python scripts/build_examples.py
python scripts/build_examples.py --check
python scripts/build_site_data.py
python scripts/build_site_data.py --check
```

### Change source material

1. Edit `src/source-material/items/<id>.md`.
2. Rebuild and check:

```bash
python scripts/build_source_material_library.py
python scripts/build_source_material_library.py --check
python scripts/build_site_data.py
python scripts/build_site_data.py --check
```

### Change audit/testing files

1. Edit `src/audit-library/files/*.md` or `src/audit-library/audit-pack.yml`.
2. Rebuild and check:

```bash
python scripts/build_audit_pack.py
python scripts/build_audit_pack.py --ci
```

## Full local check

Before opening a pull request or handing back a changed ZIP, run:

```bash
python scripts/build_prompt_libraries.py
python scripts/build_prompt_libraries.py --check
python scripts/build_source_material_library.py
python scripts/build_source_material_library.py --check
python scripts/build_site_main.py
python scripts/build_site_pages.py
python scripts/build_site_guides.py
python scripts/build_examples.py
python scripts/build_examples.py --check
python scripts/build_site_data.py
python scripts/build_site_data.py --check
python scripts/build_site_data.py --validate
python scripts/build_audit_pack.py
python scripts/build_audit_pack.py --ci
```

## Generated files

Do not fix generated prompt libraries, generated JSON, generated examples, generated source-material pages or generated audit files by editing them directly. Change the source or generator, then rebuild.

## More documentation

Start with:

```text
BUILD_AND_GENERATOR_GUIDE.md
UPDATE-CHECKLISTS.md
PROMPTS.md
project-docs/README.md
```
