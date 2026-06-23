# Source Material Index Explainer

The source-material library contains copy-ready practice passages for tutors, students and maintainers to try Reflective Writer tools safely.

The source files live in:

```text
src/source-material/items/*.md
```

The generated public files live in:

```text
docs/source-material/index.html
docs/source-material/latest/*.md
docs/data/source_material_index.json
```

## Item format

Each item is a Markdown file with YAML front matter followed by the passage.

```markdown
---
id: over-description-practice
title: Over-description practice passage
tool_code: RF1
tool_title: Description Detox
category: Reflective Foundations
use_when: Use this to practise moving from event summary to reflective selection.
---

I went to the meeting and then...
```

Required fields:

| Field | Purpose |
| --- | --- |
| `id` | Stable identifier used in filenames and generated JSON. |
| `title` | Human-readable title on the public source-material page. |
| `tool_code` | Primary tool code, such as `RF1` or `NH4`. |
| `tool_title` | Matching tool title. |
| `category` | Broad library or teaching category. |
| `use_when` | Short explanation of when to use the passage. |

## Safety rules

Source-material passages must be fictional, composite or safely anonymised. Do not include real names, exact placements, unusual dates, identifiable workplaces, rare clinical details or combinations of details that could identify someone.

Passages should be deliberately imperfect. They are testing and teaching inputs, not model student submissions.

Good source material may include:

- over-description;
- weak analysis;
- missing learning;
- tone problems;
- poor anonymisation using obvious placeholders;
- framework box-ticking;
- uncertainty about what should be included.

It should not include:

- real confidential reflective material;
- private student work without explicit permission and manual anonymisation;
- a finished polished reflection for submission;
- material that encourages the AI to invent feelings, insight or learning.

## Build commands

Run from the repository root:

```bash
python scripts/build_source_material_library.py
python scripts/build_source_material_library.py --check
python scripts/build_site_data.py
python scripts/build_site_data.py --check
python scripts/build_site_data.py --validate
```

The source-material builder writes the public page and Markdown downloads. The site-data builder keeps `docs/data/source_material_index.json` aligned with the same source records.

## When adding or changing an item

1. Create or edit the item under `src/source-material/items/`.
2. Check that `tool_code` and `tool_title` match the live tool metadata.
3. Keep the passage safe, fictional/composite and intentionally imperfect.
4. Rebuild source material and site data.
5. Spot-check the public page at `docs/source-material/index.html`.
