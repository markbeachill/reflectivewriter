# Source material library

Copy-ready **practice passages** for the reflective-writing tutor tools. Each item
is a short, often anonymised piece of writing you can paste into a tool to try it,
demonstrate it to students, or run the tutor deployment check (see
`docs/guides/deployment-check.html`).

These are deliberately imperfect inputs — over-descriptive, venting, box-ticking,
or (for the anonymisation tools) deliberately identifying — so you can see whether
a tool diagnoses the problem rather than writing a fixed version for the student.
They are testing and teaching material; they are **not** intended for student
submission.

Edit the Markdown files in `src/source-material/items/`, then rebuild the public
page:

```bash
python scripts/build_source_material_library.py
python scripts/build_source_material_library.py --check   # verify it is current
```

Each item has a small front-matter block (`id`, `title`, `tool_code`,
`tool_title`, `category`, `use_when`) followed by the passage to display and copy.
