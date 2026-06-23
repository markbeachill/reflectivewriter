# Release process

Reflective Writer currently uses a small release metadata file:

```text
src/prompt-library/release.yml
```

Current fields:

```yaml
toolkit_version: 1.0
prompt_library_version: 1.0
last_updated: 2026-06-13
```

The site-data generator derives release JSON from this file.

## Versioned outputs

Prompt-library archives currently write to:

```text
docs/prompt-libraries/v1.0/
```

Audit/testing archives currently write to:

```text
docs/audit-library/v1.0/
```

If the public version changes, update release metadata and archive paths together.

## Pre-release build

```bash
python scripts/build_all.py
```

## Pre-release checks

```bash
python scripts/build_all.py --ci
```

## Manual inspection

Before publishing, inspect:

```text
docs/index.html
docs/tools/index.html
docs/try-it/index.html
docs/testing.html
docs/prompt-libraries/latest/reflective_writing_tutor_mini_libraries.zip
docs/audit-library/latest/reflective_writer_testing_pack.zip
```

Confirm that the site links, downloads, examples and testing materials reflect the release.
