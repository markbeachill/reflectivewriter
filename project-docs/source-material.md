# Source-material library

The source-material library contains safe practice passages used for demonstrations, student trials and testing.

Editable source lives under:

```text
src/source-material/items/*.md
```

Generated outputs live under:

```text
docs/source-material/index.html
docs/source-material/latest/*.md
docs/data/source_material_index.json
```

## Build commands

```bash
python scripts/build_source_material_library.py
python scripts/build_source_material_library.py --check
python scripts/build_site_data.py
python scripts/build_site_data.py --check
python scripts/build_site_data.py --validate
```

## Item rules

Each item should have front matter with:

```text
id
title
tool_code
tool_title
category
use_when
```

The body should be a deliberately imperfect practice passage, not a polished model answer.

See `SOURCE_MATERIAL_INDEX_EXPLAINER.md` for the full item format.


For a full repository rebuild/check, use `python scripts/build_all.py` followed by `python scripts/build_all.py --check`.
