# Release process

Reflective Writer uses a single release-update workflow so the source version, prompt-library archive paths, prompt manifest text, audit-pack stamps, changelog and generated site data stay aligned.

## Source release metadata

The current release stamp lives in:

```text
src/prompt-library/release.yml
```

Current fields:

```yaml
release_version: 1.1
toolkit_version: 1.1
prompt_library_version: 1.1
release_date: 2026-06-23
last_updated: 2026-06-23
status: active public release
```

Do not update version strings manually across the repo. Use the updater.

## Version-update command

```bash
python scripts/update_version.py <version> --date YYYY-MM-DD
```

For example:

```bash
python scripts/update_version.py 1.2 --date 2026-07-15 \
  --summary "Short release summary." \
  --change "First public changelog bullet." \
  --change "Second public changelog bullet."
```

The updater touches:

```text
src/prompt-library/release.yml
src/prompt-library/packs/*.yml
src/prompt-library/pack-sections/*/00-manifest.md
src/prompt-library/pack-sections/*/03-launcher.md
src/prompt-library/tools/*.md
src/audit-library/files/*.md
CHANGELOG.md
```

It can also check consistency without writing:

```bash
python scripts/update_version.py --check
```

## Versioned outputs

The prompt-library builder writes current downloads to `docs/prompt-libraries/latest/` and fixed archives to:

```text
docs/prompt-libraries/v<version>/
```

The audit/testing builder writes current files to `docs/audit-library/latest/` and fixed archives to:

```text
docs/audit-library/v<version>/
```

Old version folders should normally remain in the repo as historical fixed archives.

## Pre-release build and checks

```bash
python scripts/build_all.py --ci
```

This rebuilds generated outputs, checks version metadata, validates generated JSON and audit outputs, and compiles scripts.

## Manual inspection

Before publishing, inspect:

```text
docs/index.html
docs/changelog/index.html
docs/data/release.json
docs/tools/index.html
docs/try-it/index.html
docs/testing.html
docs/prompt-libraries/latest/reflective_writing_tutor_mini_libraries.zip
docs/audit-library/latest/reflective_writer_testing_pack.zip
```

Confirm that the site links, downloads, examples and testing materials reflect the release.
