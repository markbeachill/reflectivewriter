# Build system overview

The build system is a set of small Python scripts plus an all-in-one wrapper, `scripts/build_all.py`. Use the wrapper for full local builds and CI-style checks; use individual scripts for targeted subsystem work.

## Build layers

| Layer | Script | Main output |
| --- | --- | --- |
| All generated outputs | `scripts/build_all.py` | Runs the full standard build/check sequence |
| Version updater | `scripts/update_version.py` | Aligns release metadata, archive paths, prompt stamps and changelog |
| Prompt libraries | `scripts/build_prompt_libraries.py` | `docs/prompt-libraries/` |
| Source material | `scripts/build_source_material_library.py` | `docs/source-material/`, `docs/data/source_material_index.json` |
| Main/tool pages | `scripts/build_site_main.py` | `docs/index.html`, `docs/tools/` |
| Other site pages | `scripts/build_site_pages.py` | About, testing, try-it, student-help, guides index, changelog |
| Additional guides | `scripts/build_site_guides.py` | Detailed guide and student-help pages |
| Worked examples | `scripts/build_examples.py` | `docs/examples/` |
| Site data | `scripts/build_site_data.py` | `docs/data/` |
| Audit/testing pack | `scripts/build_audit_pack.py` | `docs/audit-library/` |

## Full local build/check

```bash
python scripts/build_all.py
python scripts/build_all.py --check
```

For the same build/check/compile sequence used by CI:

```bash
python scripts/build_all.py --ci
```

To see the underlying commands:

```bash
python scripts/build_all.py --list
```

## Dependency notes

- Prompt-library metadata feeds prompt-library outputs and site data.
- Example source records feed example pages and site data.
- Source-material source records feed the public source-material page and site data.
- Shared site navigation lives in `scripts/_site.py`; if it changes, rebuild all site pages.

## Build-first rule

When in doubt, rebuild the generated outputs before checking. Check mode should confirm that the generated files are current, not be used as a substitute for generating them after a source edit.

## Version updates

Use the version updater before a public release bump:

```bash
python scripts/update_version.py <version> --date YYYY-MM-DD
python scripts/build_all.py --ci
```

`build_all.py --check` includes the same version-consistency check, so stale archive paths or prompt-version stamps fail early.
