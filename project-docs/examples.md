# Worked examples

Worked examples demonstrate how a tool behaves without using real reflective material.

Source records live under:

```text
src/examples/items/*.yml
```

Generated public pages live under:

```text
docs/examples/index.html
docs/examples/example-*.html
```

## Supporting files

```text
src/examples/README.md
src/examples/example-schema.md
docs/guides/creating-examples.html
scripts/build_examples.py
```

## Build commands

```bash
python scripts/build_examples.py
python scripts/build_examples.py --check
python scripts/build_site_data.py
python scripts/build_site_data.py --check
```

## Public-example safety rules

Public examples should normally be fictional or composite. They must:

- preserve the writer's authorship;
- avoid identifying detail;
- avoid jigsaw identification;
- avoid producing a finished reflection;
- teach a reflective move rather than supply submission content;
- include required safety checks in the YAML record.

## When updating an example

1. Edit the YAML source record.
2. Validate against `src/examples/example-schema.md`.
3. Rebuild examples.
4. Rebuild site data.
5. Spot-check the generated example page.


For a full repository rebuild/check, use `python scripts/build_all.py` followed by `python scripts/build_all.py --check`.
