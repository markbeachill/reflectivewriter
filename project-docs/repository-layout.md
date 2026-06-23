# Repository layout

Reflective Writer separates editable source files, generated public files and maintainer documentation.

## Top-level files

```text
README.md                         Public repository front door.
PROMPTS.md                        Developer guide to prompt-source structure.
CUSTOMISING_PROMPTS.md            Guide for adapting local versions.
BUILD_AND_GENERATOR_GUIDE.md      Maintainer build guide.
UPDATE-CHECKLISTS.md              Operational update checklists.
CONTRIBUTING.md                   Short contribution workflow.
SOURCE_MATERIAL_INDEX_EXPLAINER.md  Source-material item format and rules.
LICENSE                           MIT licence.
```

## Top-level folders

```text
src/             Editable source for prompt libraries, examples, source material and audit pack.
scripts/         Python generators and shared site helpers.
docs/            Public GitHub Pages site and generated downloads.
project-docs/    Current maintainer documentation.
.github/         GitHub Actions workflow.
```

## Source folders

```text
src/prompt-library/       Prompt-library header, shared rules, tools, packs, metadata and release stamp.
src/examples/             Worked-example YAML records and schema notes.
src/source-material/      Practice-passage Markdown records.
src/audit-library/        Audit/testing pack manifest and source files.
```

## Generated folders

```text
docs/prompt-libraries/    Downloadable master and mini prompt libraries.
docs/examples/            Public worked-example pages.
docs/source-material/     Copy-ready practice-passage page and Markdown downloads.
docs/audit-library/       Audit/testing pack outputs and ZIP.
docs/data/                Generated JSON integration data.
docs/tools/               Public tool overview pages.
docs/guides/              Public educator/student guides.
docs/student-help/        Student-facing help pages.
```

## Documentation status rule

```text
project-docs/ = current maintainer truth
src/          = editable content source
docs/         = public generated/published output
```

If a generated page needs a lasting change, update the generator or the source data that feeds it.
