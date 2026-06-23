# Worked example source library

Source records for the public **worked examples** at `docs/examples/`. Each item is
one short teaching exchange for a Reflective Writer tool. The examples show the
AI diagnosing, questioning and setting a next task; they must never show the AI
writing a finished reflection or inventing the writer's experience, feelings,
insight or learning.

Edit the YAML files in `src/examples/items/`, then rebuild the examples:

```bash
python scripts/build_examples.py
python scripts/build_examples.py --check   # verify generated pages are current
```

## Safety standard

Use fictional or composite examples by default. Do not publish real reflective
material unless permission, manual anonymisation and local policy checks are in
place. Public examples must pass the privacy and authorship checks in each YAML
file before publication.

A safe example:

- removes direct identifiers such as names, dates, institutions and locations;
- avoids jigsaw identifiers such as unusual cases, rare roles or recognisable
  combinations of detail;
- uses the AI to teach a reflective move, not to produce the student's reflection;
- keeps the student's own meaning, feeling, judgement and learning unwritten by
  the AI;
- includes a clear `privacy_note` and true/false checks.

See `example-schema.md` for the required fields and `docs/guides/creating-examples.html`
for the tutor-facing workflow.
