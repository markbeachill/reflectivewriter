# Audit and testing pack

The audit/testing pack provides lightweight release and deployment checks for Reflective Writer.

Source lives under:

```text
src/audit-library/
```

Generated outputs live under:

```text
docs/audit-library/latest/
docs/audit-library/v<version>/
docs/testing.html
```

## Source files

```text
src/audit-library/audit-pack.yml
src/audit-library/files/reflective_writer_audit_prompt_with_menu.md
src/audit-library/files/reflective_writer_output_collector.md
src/audit-library/files/reflective_writer_test_cards.md
src/audit-library/files/reflective_writer_test_log_template.md
src/audit-library/files/reflective_writer_testing_guide_for_educators.md
```

## Build commands

```bash
python scripts/build_audit_pack.py
python scripts/build_audit_pack.py --check
python scripts/build_audit_pack.py --validate
python scripts/build_audit_pack.py --ci
```

## What the tests cover

The pack focuses on Reflective Writer-specific risks:

- ghost-writing refusal;
- invented feelings or learning;
- anonymisation and jigsaw identification;
- over-description support;
- venting, blame and professional tone;
- EAL support without rewriting;
- framework box-ticking;
- local-rule uncertainty;
- help/stuckness controls;
- master routing and direct codes.

## Safety rule

Do not put real student, patient, service-user, colleague, placement or family details in audit prompts or test logs. Use fictional, composite or placeholder material only.


For a full repository rebuild/check, use `python scripts/build_all.py` followed by `python scripts/build_all.py --check`.
