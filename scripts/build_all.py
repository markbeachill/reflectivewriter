#!/usr/bin/env python3
"""Run all Reflective Writer generators in the standard order.

Typical use from the repository root:
    python scripts/build_all.py          # rebuild all generated outputs
    python scripts/build_all.py --check  # run non-writing checks where available
    python scripts/build_all.py --ci     # rebuild, check, validate and compile

The individual generators remain the source of detailed behaviour. This runner is a
small convenience wrapper so maintainers and CI can use one stable command.
"""
from __future__ import annotations

import argparse
import importlib
import py_compile
import runpy
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Sequence

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

Action = Callable[[], int | None]


@dataclass(frozen=True)
class Step:
    label: str
    display_command: str
    action: Action


def _module(name: str):
    return importlib.import_module(name)


def _ok(value: int | None) -> int:
    return 0 if value is None else int(value)


def _run_script(filename: str) -> None:
    """Run a build-only script in-process.

    Some older site builders execute at module top level rather than exposing a
    reusable build() function. runpy keeps this wrapper fast while preserving their
    current behaviour.
    """
    runpy.run_path(str(SCRIPTS / filename), run_name="__main__")


def build_prompt_libraries() -> int:
    return _module("build_prompt_libraries").run(check_only=False)


def check_prompt_libraries() -> int:
    return _module("build_prompt_libraries").run(check_only=True)


def build_source_material() -> int:
    return _module("build_source_material_library").build(check=False)


def check_source_material() -> int:
    return _module("build_source_material_library").build(check=True)


def build_examples() -> int:
    return _module("build_examples").build(check=False)


def check_examples() -> int:
    return _module("build_examples").build(check=True)


def build_site_data() -> int:
    changes = _module("build_site_data").write_outputs()
    if changes:
        print("Updated generated site data files:")
        for change in changes:
            print(f"  - {change}")
    else:
        print("No site data changes needed.")
    return 0


def check_site_data() -> int:
    changes = _module("build_site_data").check_outputs()
    if changes:
        print("Generated site data files are out of date:", file=sys.stderr)
        for change in changes:
            print(f"  - {change}", file=sys.stderr)
        print("\nLikely fix from the repository root:", file=sys.stderr)
        print("  python scripts/build_site_data.py", file=sys.stderr)
        print("  python scripts/build_site_data.py --check", file=sys.stderr)
        return 1
    print("Generated site data files are up to date.")
    return 0


def validate_site_data() -> int:
    _module("build_site_data").validate_current_outputs()
    print("Generated site data files validated.")
    return 0


def build_audit_pack() -> int:
    audit = _module("build_audit_pack")
    spec = audit.load_spec()
    version = audit.read_release_version()
    audit.build(spec, version)
    return 0


def check_audit_pack() -> int:
    audit = _module("build_audit_pack")
    spec = audit.load_spec()
    version = audit.read_release_version()
    return 0 if audit.check(spec, version) else 1


def validate_audit_pack() -> int:
    audit = _module("build_audit_pack")
    spec = audit.load_spec()
    version = audit.read_release_version()
    return 0 if audit.validate(spec, version) else 1


def compile_scripts() -> int:
    for path in sorted(SCRIPTS.glob("*.py")):
        py_compile.compile(str(path), doraise=True)
    return 0


def check_version_metadata() -> int:
    problems = _module("update_version").validate_release_consistency()
    if problems:
        print("Version metadata consistency: PROBLEMS FOUND", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        print("\nCommon fix:", file=sys.stderr)
        print("  python scripts/update_version.py <version> --date YYYY-MM-DD", file=sys.stderr)
        print("  python scripts/build_all.py --ci", file=sys.stderr)
        return 1
    print("Version metadata consistency: OK")
    return 0


BUILD_STEPS: tuple[Step, ...] = (
    Step("Build prompt libraries", "python scripts/build_prompt_libraries.py", build_prompt_libraries),
    Step("Build source-material library", "python scripts/build_source_material_library.py", build_source_material),
    Step("Build main and tool pages", "python scripts/build_site_main.py", lambda: _run_script("build_site_main.py")),
    Step("Build support site pages", "python scripts/build_site_pages.py", lambda: _run_script("build_site_pages.py")),
    Step("Build guide pages", "python scripts/build_site_guides.py", lambda: _run_script("build_site_guides.py")),
    Step("Build worked examples", "python scripts/build_examples.py", build_examples),
    Step("Build generated site data", "python scripts/build_site_data.py", build_site_data),
    Step("Build audit/testing pack", "python scripts/build_audit_pack.py", build_audit_pack),
)

CHECK_STEPS: tuple[Step, ...] = (
    Step("Check version metadata", "python scripts/update_version.py --check", check_version_metadata),
    Step("Check prompt libraries", "python scripts/build_prompt_libraries.py --check", check_prompt_libraries),
    Step("Check source-material library", "python scripts/build_source_material_library.py --check", check_source_material),
    Step("Check worked examples", "python scripts/build_examples.py --check", check_examples),
    Step("Check generated site data", "python scripts/build_site_data.py --check", check_site_data),
    Step("Validate generated site data", "python scripts/build_site_data.py --validate", validate_site_data),
    Step("Check audit/testing pack", "python scripts/build_audit_pack.py --check", check_audit_pack),
    Step("Validate audit/testing pack", "python scripts/build_audit_pack.py --validate", validate_audit_pack),
)

COMPILE_STEP = Step("Compile Python scripts", "python -m py_compile scripts/*.py", compile_scripts)


def run_steps(steps: Sequence[Step]) -> int:
    for step in steps:
        print(f"\n==> {step.label}", flush=True)
        print(f"    {step.display_command}", flush=True)
        try:
            rc = _ok(step.action())
        except SystemExit as exc:
            rc = int(exc.code or 0) if isinstance(exc.code, int) else 1
        except Exception as exc:  # keep top-level failure readable in CI
            print(f"\nFAILED: {step.label}: {exc}", file=sys.stderr)
            return 1
        if rc != 0:
            print(f"\nFAILED: {step.label} exited with status {rc}", file=sys.stderr)
            return rc
    return 0


def print_steps(title: str, steps: Sequence[Step]) -> None:
    print(title)
    for step in steps:
        print(f"  - {step.display_command}")


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build/check all Reflective Writer generated outputs.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="run non-writing checks and validation where generators support them")
    mode.add_argument("--ci", action="store_true", help="rebuild everything, then run checks, validation and Python compile checks")
    parser.add_argument("--list", action="store_true", help="show the commands this runner uses and exit")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)

    if args.list:
        print_steps("Build steps:", BUILD_STEPS)
        print()
        print_steps("Check steps:", CHECK_STEPS)
        print()
        print_steps("Compile step:", (COMPILE_STEP,))
        return 0

    if args.check:
        rc = run_steps(CHECK_STEPS + (COMPILE_STEP,))
        if rc == 0:
            print("\nAll available generated-output checks passed.")
        return rc

    if args.ci:
        rc = run_steps(BUILD_STEPS + CHECK_STEPS + (COMPILE_STEP,))
        if rc == 0:
            print("\nAll build, check and compile steps passed.")
        return rc

    rc = run_steps(BUILD_STEPS)
    if rc == 0:
        print("\nAll generated outputs rebuilt.")
        print("Next check: python scripts/build_all.py --check")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
