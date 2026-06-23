# Update Checklists

Use this file when changing Reflective Writer tools, examples, source material, audit/testing files, site pages or release metadata.

When using an AI assistant, ask it to report:

```text
- which checklist it followed;
- source files changed;
- generated files changed;
- checks run;
- checks not run or failed;
- anything intentionally left for a later phase.
```

## A. Updating an existing prompt-library tool

Use when editing:

```text
src/prompt-library/tools/*.md
```

1. Confirm scope.
   - Identify tool code, title and source file.
   - Decide whether this is wording, behaviour, boundary, routing, numbering or metadata work.
   - Check whether related examples, source material or tests mention the old behaviour.

2. Edit the tool source.
   - Keep the `<!-- FILE: ... -->` marker, YAML front matter and `<!-- END FILE -->` marker intact.
   - Check front matter: `id`, `tool_code`, `title`, `type`, `menu_number`, `run_policy`, `interaction_type`, `tool_mode`.
   - Keep the tool contract aligned with the body.
   - Preserve the no-ghost-writing boundary.

3. Check metadata.
   - Update `src/prompt-library/tool-metadata.json` if codes, titles, descriptions, aliases, family, ordering or `tool_mode` changed.
   - Make sure `tool_mode` in the tool file and metadata match.
   - Update pack YAML only if pack membership changes.

4. Rebuild and check.

```bash
python scripts/build_prompt_libraries.py
python scripts/build_prompt_libraries.py --check
python scripts/build_site_data.py
python scripts/build_site_data.py --check
python scripts/build_site_data.py --validate
```

5. Inspect generated output.
   - Check the relevant `docs/prompt-libraries/latest/*.md` file.
   - Check `docs/data/tool_index.json` if metadata changed.
   - Confirm old wording has not survived unexpectedly.

## B. Adding a new tool

1. Create the tool source in `src/prompt-library/tools/`.
2. Add an entry to `src/prompt-library/tool-metadata.json`.
3. Add the tool to the correct mini-library pack and to `master.yml`.
4. Add a public worked-example record in `src/examples/items/`.
5. Add or update practice source material if the tool needs a trial passage.
6. Add audit test coverage if the tool creates a new safety or behaviour risk.
7. Rebuild:

```bash
python scripts/build_prompt_libraries.py
python scripts/build_examples.py
python scripts/build_source_material_library.py
python scripts/build_site_data.py
python scripts/build_site_main.py
python scripts/build_site_pages.py
python scripts/build_site_guides.py
python scripts/build_audit_pack.py
```

8. Run checks:

```bash
python scripts/build_prompt_libraries.py --check
python scripts/build_examples.py --check
python scripts/build_source_material_library.py --check
python scripts/build_site_data.py --check
python scripts/build_site_data.py --validate
python scripts/build_audit_pack.py --ci
```

## C. Updating shared behaviour rules

Use when editing:

```text
src/prompt-library/shared/*.md
src/prompt-library/header.md
src/prompt-library/pack-sections/**
```

1. Identify whether the change affects all libraries, one family, or the master only.
2. Keep Reflective Writer's central rule explicit: the tutor must not invent the writer's experience, feelings, insight or learning.
3. Preserve help/EAL/stuckness behaviour if touching shared rules.
4. Rebuild prompt libraries and site data.
5. Spot-check the master library and one mini library.

```bash
python scripts/build_prompt_libraries.py
python scripts/build_prompt_libraries.py --check
python scripts/build_site_data.py
python scripts/build_site_data.py --check
```

## D. Updating worked examples

Use when editing:

```text
src/examples/items/*.yml
src/examples/example-schema.md
scripts/build_examples.py
```

1. Prefer fictional or composite material.
2. Check every public example has required safety checks set to `true`.
3. Do not include real student, patient, service-user, placement, colleague or family details.
4. Make sure the transcript teaches a move rather than writing a finished reflection.
5. Rebuild and check:

```bash
python scripts/build_examples.py
python scripts/build_examples.py --check
python scripts/build_site_data.py
python scripts/build_site_data.py --check
python scripts/build_site_data.py --validate
```

## E. Updating source material

Use when editing:

```text
src/source-material/items/*.md
```

1. Check front matter: `id`, `title`, `tool_code`, `tool_title`, `category`, `use_when`.
2. Use fictional, composite or safely anonymised passages.
3. Keep passages deliberately imperfect; they are practice/testing inputs, not model submissions.
4. Rebuild and check:

```bash
python scripts/build_source_material_library.py
python scripts/build_source_material_library.py --check
python scripts/build_site_data.py
python scripts/build_site_data.py --check
python scripts/build_site_data.py --validate
```

## F. Updating audit/testing materials

Use when editing:

```text
src/audit-library/audit-pack.yml
src/audit-library/files/*.md
scripts/build_audit_pack.py
```

1. Identify whether the change affects the audit prompt, test cards, output collector, log template or educator guide.
2. Keep test inputs fictional, composite or placeholder-based.
3. Ensure expected behaviour tests tutoring, not content production.
4. Rebuild and check:

```bash
python scripts/build_audit_pack.py
python scripts/build_audit_pack.py --ci
```

5. If public site wording changed, also run:

```bash
python scripts/build_site_pages.py
```

## G. Updating generated site pages or navigation

Use when editing:

```text
scripts/_site.py
scripts/_tools_specialist.py
scripts/build_site_main.py
scripts/build_site_pages.py
scripts/build_site_guides.py
scripts/build_examples.py
scripts/build_source_material_library.py
```

1. Decide whether the change is shared navigation/footer, a specific page, or a generator template change.
2. Rebuild the affected pages and any dependent pages.
3. If navigation changed, run all site-page generators:

```bash
python scripts/build_site_main.py
python scripts/build_site_pages.py
python scripts/build_site_guides.py
python scripts/build_examples.py
python scripts/build_source_material_library.py
```

## H. Release/update checklist

Before tagging or publishing a public release:

1. Use the release updater; do not edit version strings one by one.

```bash
python scripts/update_version.py <version> --date YYYY-MM-DD
```

Optional release-note fields:

```bash
python scripts/update_version.py <version> --date YYYY-MM-DD \
  --summary "Short release summary." \
  --change "First changelog bullet." \
  --change "Second changelog bullet."
```

2. Confirm the updater reports `Version metadata consistency: OK`.
3. Rebuild and check everything:

```bash
python scripts/build_all.py --ci
```

4. Inspect:

```text
docs/changelog/index.html
docs/data/release.json
docs/prompt-libraries/latest/*.md
docs/prompt-libraries/v<version>/*.md
docs/audit-library/latest/*
docs/audit-library/v<version>/*
```

5. Commit the changed source and generated files together.
