# Worked example schema

Each file in `src/examples/items/` is a YAML record with this structure:

```yaml
id: rf1-description-detox
code: RF1
tool_id: description-detox
title: RF1 — Description Detox worked example
status: public
safety_level: fictional
context: How RF1 separates retelling from reflection.
learning_point: How RF1 separates retelling from reflection.
privacy_note: Fictional or composite teaching example; no real person is identifiable.
transcript:
  - role: tutor
    html: "<h2>RF1 — Description Detox</h2><p>Paste a passage...</p>"
  - role: student
    html: "<p>During my placement...</p>"
checks:
  authorship_boundary: true
  no_identifying_detail: true
  unrelated_made_up_example_only: true
  no_finished_reflection: true
  privacy_reviewed: true
```

## Required fields

| Field | Meaning |
| --- | --- |
| `id` | Stable source id, normally `<code-lower>-<tool-id>`. |
| `code` | Tool code, such as `RF1` or `MD3`. Must match `tool-metadata.json`. |
| `tool_id` | Canonical tool id from `src/prompt-library/tool-metadata.json`. |
| `title` | Human-readable title for maintainers. |
| `status` | `public`, `draft` or `internal`. Public examples are rendered. |
| `safety_level` | `fictional`, `composite`, `anonymised_real` or `internal_test`. Public examples should normally be `fictional` or `composite`. |
| `context` | Short page lead explaining the example situation. |
| `learning_point` | What the example demonstrates pedagogically. |
| `privacy_note` | Why the example is safe to publish. |
| `transcript` | Ordered turns. Each turn has `role` (`student` or `tutor`) and an HTML fragment in `html`. |
| `checks` | Boolean safety/authorship checks. Public examples require all listed checks to be `true`. |

## Public-example checks

Public examples must have these checks set to `true`:

- `authorship_boundary`
- `no_identifying_detail`
- `unrelated_made_up_example_only`
- `no_finished_reflection`
- `privacy_reviewed`

If any check is uncertain, leave the example as `draft` or `internal` and do not
publish it.

## Transcript rules

Use `role: tutor` for the AI and `role: student` for the writer. The `html` field
is an HTML fragment because the public pages render chat bubbles. Keep fragments
simple: headings, paragraphs, blockquotes, emphasis, strong text and lists are
preferred. Do not include scripts, forms or externally loaded media.
