# Build and Generator Guide

This is the maintainer build guide for the Reflective Report Writing Tutor repository.

The repository is source-driven. Human-edited source lives mainly in `src/`; generated public outputs live mainly in `docs/`. When you change source files, rebuild the relevant generated files and commit both the source change and the generated result.

## Quick build/check sequence

Run from the repository root. Prefer the all-in-one runner for broad changes and releases.

```bash
python scripts/build_all.py          # rebuild all generated outputs
python scripts/build_all.py --check  # check version metadata and generated outputs
python scripts/build_all.py --ci     # rebuild, check, validate and compile
python scripts/build_all.py --list   # show underlying commands
```

Use individual generator scripts only when you are working on one subsystem and already know which generated files it owns.

## Version/release update sequence

Use the version updater whenever the public toolkit version changes. It keeps the release stamp, prompt archive paths, prompt manifest versions, audit-pack stamps and changelog aligned.

```bash
python scripts/update_version.py 1.1 --date 2026-06-23 \
  --summary "Architecture and maintenance refresh." \
  --change "Added version-update workflow."
python scripts/build_all.py --ci
```

The updater can also validate the current release metadata without writing:

```bash
python scripts/update_version.py --check
```

## Source of truth

Edit these files and folders by hand:

```text
src/prompt-library/        Prompt-library source, shared rules, tools, packs and release stamp.
src/examples/              Worked-example source records.
src/source-material/       Practice-passage source records.
src/audit-library/         Audit/testing-pack source files.
scripts/                   Generators and site builders.
README.md                  Public repository front door.
PROMPTS.md                 Prompt-source developer guide.
CUSTOMISING_PROMPTS.md     Local adaptation guide.
project-docs/              Maintainer documentation.
```

Treat these as generated public outputs:

```text
docs/prompt-libraries/     Downloadable master and mini prompt libraries.
docs/examples/             Worked-example pages.
docs/source-material/      Copy-ready practice-passage page and downloads.
docs/audit-library/        Audit/testing pack outputs.
docs/data/                 Generated JSON integration data.
docs/*.html                Generated or normalised public site pages.
```

Do not hand-edit generated prompt libraries, generated JSON, generated audit outputs, or generated example/source-material pages as the primary fix. Edit the source or generator, then rebuild.

## Release metadata

The release stamp lives in:

```text
src/prompt-library/release.yml
```

Current fields are:

```yaml
release_version: 1.1
toolkit_version: 1.1
prompt_library_version: 1.1
release_date: 2026-06-23
last_updated: 2026-06-23
status: active public release
```

Do not update this file by itself for a public release. Use:

```bash
python scripts/update_version.py <version> --date YYYY-MM-DD
```

That also updates:

```text
src/prompt-library/packs/*.yml
src/prompt-library/pack-sections/*/00-manifest.md
src/prompt-library/pack-sections/*/03-launcher.md
src/prompt-library/tools/*.md
src/audit-library/files/*.md
CHANGELOG.md
```

Then run `python scripts/build_all.py --ci` so the downloadable libraries, site data, changelog page and audit archives reflect the new version.

## Prompt-library generation

Source:

```text
src/prompt-library/header.md
src/prompt-library/shared/*.md
src/prompt-library/pack-sections/**
src/prompt-library/tools/*.md
src/prompt-library/tool-metadata.json
src/prompt-library/packs/*.yml
src/prompt-library/release.yml
```

Generator:

```bash
python scripts/build_prompt_libraries.py
python scripts/build_prompt_libraries.py --check
python scripts/build_prompt_libraries.py --ci
```

Generated outputs:

```text
docs/prompt-libraries/latest/*.md
docs/prompt-libraries/v<version>/*.md
docs/prompt-libraries/latest/reflective_writing_tutor_mini_libraries.zip
```

The builder validates tool front matter, metadata consistency, `tool_mode`, pack membership and template placeholders. Mini libraries renumber visible menu numbers; the master library keeps the master numbering and family-first router.

## Worked-example generation

Source:

```text
src/examples/README.md
src/examples/example-schema.md
src/examples/items/*.yml
```

Generator:

```bash
python scripts/build_examples.py
python scripts/build_examples.py --check
```

Generated outputs:

```text
docs/examples/index.html
docs/examples/example-*.html
```

Public examples should normally be fictional or composite. Every public example must preserve the authorship boundary, avoid identifying detail and avoid producing a finished reflection.

## Source-material generation

Source:

```text
src/source-material/README.md
src/source-material/items/*.md
```

Generator:

```bash
python scripts/build_source_material_library.py
python scripts/build_source_material_library.py --check
```

Generated outputs:

```text
docs/source-material/index.html
docs/source-material/latest/*.md
docs/data/source_material_index.json
```

See `SOURCE_MATERIAL_INDEX_EXPLAINER.md` for the source-material item format and safety rules.

## Site-page generation

Generators:

```bash
python scripts/build_site_main.py
python scripts/build_site_pages.py
python scripts/build_site_guides.py
```

Generated or normalised pages include:

```text
docs/index.html
docs/tools/*.html
docs/about.html
docs/testing.html
docs/try-it/index.html
docs/student-help/*.html
docs/guides/*.html
docs/changelog/index.html
```

These scripts use shared helpers from `scripts/_site.py` and specialist-tool data from `scripts/_tools_specialist.py`.

## Site-data generation

Source inputs:

```text
src/prompt-library/release.yml
src/prompt-library/tool-metadata.json
src/prompt-library/packs/*.yml
src/examples/items/*.yml
src/source-material/items/*.md
```

Generator:

```bash
python scripts/build_site_data.py
python scripts/build_site_data.py --check
python scripts/build_site_data.py --validate
```

Generated outputs:

```text
docs/data/release.json
docs/data/tool_index.json
docs/data/prompt_library_packs.json
docs/data/source_material_index.json
```

## Audit/testing pack generation

Source:

```text
src/audit-library/audit-pack.yml
src/audit-library/files/*.md
```

Generator:

```bash
python scripts/build_audit_pack.py
python scripts/build_audit_pack.py --check
python scripts/build_audit_pack.py --validate
python scripts/build_audit_pack.py --ci
```

Generated outputs:

```text
docs/audit-library/latest/*
docs/audit-library/v<version>/*
docs/audit-library/latest/reflective_writer_testing_pack.zip
```

The audit pack tests Reflective Writer-specific risks: ghost-writing, invented feelings or learning, anonymisation, tone, EAL support, framework box-ticking, routing and local-rule uncertainty.

## What to commit

For a prompt-library change, commit:

```text
src/prompt-library/...
docs/prompt-libraries/...
docs/data/...
```

For an example change, commit:

```text
src/examples/...
docs/examples/...
```

For a source-material change, commit:

```text
src/source-material/...
docs/source-material/...
docs/data/source_material_index.json
```

For audit/testing changes, commit:

```text
src/audit-library/...
docs/audit-library/...
docs/testing.html
```

For generated page/navigation changes, commit the changed generator and generated pages.

## GitHub Actions

The workflow is:

```text
.github/workflows/build-prompt-libraries.yml
```

It rebuilds prompt libraries, source material, site pages, site data and the audit pack, then fails if generated files are out of date. GitHub Pages is served from the static `docs/` folder.
