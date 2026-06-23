# Generated files

Reflective Writer keeps editable source and generated public output separate.

## Editable source areas

```text
src/prompt-library/        Prompt-library source files and pack definitions.
src/examples/              Worked-example source records.
src/source-material/       Practice-passage source records.
src/audit-library/         Audit/testing source files.
scripts/                   Generators and site helpers.
project-docs/              Maintainer documentation.
```

## Generated public outputs

```text
docs/prompt-libraries/     Downloadable prompt-library Markdown files and ZIP.
docs/examples/             Worked-example pages.
docs/source-material/      Copy-ready source-material page and Markdown downloads.
docs/audit-library/        Audit/testing pack files and ZIP.
docs/data/                 Release, tool, pack and source-material JSON.
docs/tools/                Tool overview pages.
docs/guides/               Guide pages.
docs/student-help/         Student-facing help pages.
docs/index.html            Home page.
docs/about.html            About page.
docs/testing.html          Testing page.
docs/try-it/index.html     Try-it page.
docs/changelog/index.html  Changelog page.
```

## Never hand-edit as the primary fix

Do not manually patch these as the main solution:

```text
docs/prompt-libraries/**/*.md
docs/data/*.json
docs/examples/*.html
docs/source-material/**
docs/audit-library/**
```

Instead, update the relevant source file or generator and rebuild.

## Commit rule

Commit source and generated output together unless the project explicitly changes to deploy-time-only generation.
