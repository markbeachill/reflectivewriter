#!/usr/bin/env python3
"""Update Reflective Writer release/version metadata consistently.

This script is the release-version source-of-truth updater. It updates the files
that must move together when a public version changes:

- src/prompt-library/release.yml
- src/prompt-library/packs/*.yml archive_output paths
- src/prompt-library/pack-sections/*/00-manifest.md prompt-library stamps
- src/audit-library/files/*.md testing-pack stamps
- CHANGELOG.md

It does not rebuild generated outputs by itself unless --build is supplied. After a
version update, run ``python scripts/build_all.py --ci`` or use ``--build``.
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path
from typing import Iterable, Sequence

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "prompt-library"
RELEASE_YML = SRC / "release.yml"
PACKS_DIR = SRC / "packs"
PACK_SECTIONS_DIR = SRC / "pack-sections"
TOOLS_DIR = SRC / "tools"
AUDIT_FILES_DIR = ROOT / "src" / "audit-library" / "files"
CHANGELOG = ROOT / "CHANGELOG.md"
VERSION_RE = re.compile(r"\d+(?:\.\d+){1,3}")
DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")

DEFAULT_SUMMARY = "Maintenance release."


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def normalise_version(version: str) -> str:
    version = version.strip().lstrip("v")
    if not VERSION_RE.fullmatch(version):
        raise SystemExit(f"Invalid version {version!r}. Use a numeric version such as 1.1 or 2.0.0.")
    return version


def normalise_date(value: str | None) -> str:
    if value is None:
        return dt.date.today().isoformat()
    value = value.strip()
    if not DATE_RE.fullmatch(value):
        raise SystemExit(f"Invalid date {value!r}. Use YYYY-MM-DD.")
    return value


def version_suffix(version: str) -> str:
    return version.replace(".", "_")


def read_simple_yaml(path: Path) -> dict[str, object]:
    data: dict[str, object] = {}
    current: str | None = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.startswith("  - ") and current:
            data.setdefault(current, [])
            assert isinstance(data[current], list)
            data[current].append(raw[4:].strip().strip("'\""))
            continue
        if ":" in raw and not raw.startswith(" "):
            key, value = raw.split(":", 1)
            key = key.strip()
            value = value.strip().strip("'\"")
            if value:
                data[key] = value
                current = None
            else:
                data[key] = []
                current = key
    return data


def write_if_changed(path: Path, text: str, changed: list[str]) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else None
    if old != text:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")
        changed.append(rel(path))


def update_release_yml(version: str, release_date: str, changed: list[str]) -> None:
    text = (
        f"release_version: {version}\n"
        f"toolkit_version: {version}\n"
        f"prompt_library_version: {version}\n"
        f"release_date: {release_date}\n"
        f"last_updated: {release_date}\n"
        "status: active public release\n"
    )
    write_if_changed(RELEASE_YML, text, changed)


def update_pack_archives(version: str, changed: list[str]) -> None:
    suffix = version_suffix(version)
    for path in sorted(PACKS_DIR.glob("*.yml")):
        data = read_simple_yaml(path)
        latest = str(data.get("latest_output", ""))
        if not latest:
            continue
        archive = f"docs/prompt-libraries/v{version}/{Path(latest).stem}_v{suffix}.md"
        lines: list[str] = []
        replaced = False
        for raw in path.read_text(encoding="utf-8").splitlines():
            if raw.startswith("archive_output:"):
                lines.append(f"archive_output: {archive}")
                replaced = True
            else:
                lines.append(raw)
        if not replaced:
            output_lines: list[str] = []
            for raw in lines:
                output_lines.append(raw)
                if raw.startswith("latest_output:"):
                    output_lines.append(f"archive_output: {archive}")
            lines = output_lines
        write_if_changed(path, "\n".join(lines).rstrip() + "\n", changed)


def pack_specs_by_id() -> dict[str, dict[str, object]]:
    return {str(read_simple_yaml(path).get("id", path.stem)): read_simple_yaml(path) for path in PACKS_DIR.glob("*.yml")}


def update_manifest_text(text: str, *, version: str, release_date: str, archive_output: str | None) -> str:
    suffix = version_suffix(version)
    text = re.sub(r"^version:\s*.+$", f"version: {version}", text, flags=re.MULTILINE)
    text = re.sub(r"\*\*Version:\*\* v[0-9][0-9.]*", f"**Version:** v{version}", text)
    text = re.sub(r"\*\*Last updated:\*\* \d{4}-\d{2}-\d{2}", f"**Last updated:** {release_date}", text)
    text = re.sub(
        r"Reflective Writer toolkit v[0-9][0-9.]* / Prompt-library suite v[0-9][0-9.]*",
        f"Reflective Writer toolkit v{version} / Prompt-library suite v{version}",
        text,
    )
    text = re.sub(r"(\*\*This file:\*\* .+?) v[0-9][0-9.]*", rf"\1 v{version}", text)
    if archive_output:
        text = re.sub(
            r"\*\*Fixed archive:\*\* `[^`]+`",
            f"**Fixed archive:** `{archive_output.removeprefix('docs/')}`",
            text,
        )
    # Fallback for any remaining archive paths in older manifest prose.
    text = re.sub(r"prompt-libraries/v[0-9][0-9.]*/([^`\s/]+)_v[0-9_]+\.md", lambda m: f"prompt-libraries/v{version}/{m.group(1)}_v{suffix}.md", text)
    return text


def update_pack_manifests(version: str, release_date: str, changed: list[str]) -> None:
    specs = pack_specs_by_id()
    for manifest in sorted(PACK_SECTIONS_DIR.glob("*/00-manifest.md")):
        pack_id = manifest.parent.name
        spec = specs.get(pack_id)
        archive_output = str(spec.get("archive_output", "")) if spec else None
        old = manifest.read_text(encoding="utf-8")
        new = update_manifest_text(old, version=version, release_date=release_date, archive_output=archive_output)
        write_if_changed(manifest, new, changed)


def update_prompt_display_versions(version: str, changed: list[str]) -> None:
    """Update visible vX headings inside launcher/router/tool prompt source files."""
    for path in sorted(list(PACK_SECTIONS_DIR.glob("*/*.md")) + list(TOOLS_DIR.glob("*.md"))):
        text = path.read_text(encoding="utf-8")
        # Prompt sections use H1 titles such as '# RF2 — So-What Deepener v1.0'.
        new = re.sub(r"^(# .+?) v[0-9][0-9.]*$", rf"\1 v{version}", text, flags=re.MULTILINE)
        write_if_changed(path, new, changed)


def update_audit_source_stamps(version: str, changed: list[str]) -> None:
    for path in sorted(AUDIT_FILES_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        text = re.sub(
            r"Reflective Writer version v[0-9][0-9.]* / Prompt-library suite v[0-9][0-9.]* / Testing pack v[0-9][0-9.]*",
            f"Reflective Writer version v{version} / Prompt-library suite v{version} / Testing pack v{version}",
            text,
        )
        text = re.sub(r"(\| Reflective Writer version \| )v[0-9][0-9.]*", rf"\1v{version}", text)
        text = re.sub(r"(\| Prompt-library version \| )v[0-9][0-9.]*", rf"\1v{version}", text)
        text = re.sub(r"(\| Testing pack version \| )v[0-9][0-9.]*", rf"\1v{version}", text)
        text = re.sub(r"^(# .+?) v[0-9][0-9.]*$", rf"\1 v{version}", text, flags=re.MULTILINE)
        text = re.sub(
            r"audit-library/v[0-9][0-9.]*/([^`\s/]+)_v[0-9_]+\.md",
            lambda m: f"audit-library/v{version}/{m.group(1)}_v{version_suffix(version)}.md",
            text,
        )
        write_if_changed(path, text, changed)


def bullet_lines(changes: Iterable[str]) -> str:
    return "".join(f"- {item.strip()}\n" for item in changes if item.strip())


def changelog_has_version(text: str, version: str) -> bool:
    return re.search(rf"^##\s+v{re.escape(version)}(?:\s|$)", text, flags=re.MULTILINE) is not None


def update_changelog(version: str, release_date: str, summary: str, changes: list[str], changed: list[str]) -> None:
    existing = CHANGELOG.read_text(encoding="utf-8") if CHANGELOG.exists() else "# Changelog\n"
    if changelog_has_version(existing, version):
        # Keep existing notes, but normalise the date on the heading.
        new = re.sub(
            rf"^##\s+v{re.escape(version)}\s+[—-]\s+\d{{4}}-\d{{2}}-\d{{2}}",
            f"## v{version} — {release_date}",
            existing,
            flags=re.MULTILINE,
        )
        write_if_changed(CHANGELOG, new, changed)
        return

    summary = summary.strip() or DEFAULT_SUMMARY
    items = changes or ["Updated release metadata, generated archives and public site outputs."]
    entry = f"## v{version} — {release_date}\n\n{summary}\n\n{bullet_lines(items)}\n"
    if existing.startswith("# Changelog"):
        parts = existing.split("\n", 1)
        new = parts[0].rstrip() + "\n\n" + entry + (parts[1].lstrip("\n") if len(parts) > 1 else "")
    else:
        new = "# Changelog\n\n" + entry + existing.lstrip("\n")
    write_if_changed(CHANGELOG, new.rstrip() + "\n", changed)


def current_release_metadata() -> dict[str, str]:
    raw = read_simple_yaml(RELEASE_YML)
    return {str(k): str(v) for k, v in raw.items()}


def validate_release_consistency() -> list[str]:
    problems: list[str] = []
    release = current_release_metadata()
    version = normalise_version(str(release.get("release_version") or release.get("toolkit_version") or ""))
    release_date = str(release.get("release_date") or release.get("last_updated") or "")
    suffix = version_suffix(version)
    if not DATE_RE.fullmatch(release_date):
        problems.append(f"{rel(RELEASE_YML)} has invalid or missing release_date/last_updated")

    for key in ("toolkit_version", "prompt_library_version"):
        if str(release.get(key, "")).strip().lstrip("v") != version:
            problems.append(f"{rel(RELEASE_YML)} {key} is not {version}")

    for path in sorted(PACKS_DIR.glob("*.yml")):
        data = read_simple_yaml(path)
        latest = str(data.get("latest_output", ""))
        expected = f"docs/prompt-libraries/v{version}/{Path(latest).stem}_v{suffix}.md" if latest else ""
        if data.get("archive_output") != expected:
            problems.append(f"{rel(path)} archive_output should be {expected}")

    specs = pack_specs_by_id()
    for manifest in sorted(PACK_SECTIONS_DIR.glob("*/00-manifest.md")):
        text = manifest.read_text(encoding="utf-8", errors="ignore")
        archive = specs.get(manifest.parent.name, {}).get("archive_output")
        expected_bits = [f"version: {version}", f"**Version:** v{version}", f"**Last updated:** {release_date}"]
        if archive:
            expected_bits.append(str(archive).removeprefix("docs/"))
        for bit in expected_bits:
            if bit not in text:
                problems.append(f"{rel(manifest)} missing {bit!r}")
                break

    for path in sorted(list(PACK_SECTIONS_DIR.glob("*/*.md")) + list(TOOLS_DIR.glob("*.md"))):
        text = path.read_text(encoding="utf-8", errors="ignore")
        stale_headings = re.findall(r"^# .+ v(?!" + re.escape(version) + r"$)[0-9][0-9.]*$", text, flags=re.MULTILINE)
        if stale_headings:
            problems.append(f"{rel(path)} contains stale visible prompt heading version")

    for path in sorted(AUDIT_FILES_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8", errors="ignore")
        if f"v{version}" not in text:
            problems.append(f"{rel(path)} does not contain v{version}")
        stale_heading = re.search(r"^# .+ v(?!" + re.escape(version) + r"$)[0-9][0-9.]*$", text, flags=re.MULTILINE)
        if stale_heading:
            problems.append(f"{rel(path)} contains stale visible audit heading version")
        if "audit-library/v1.0/" in text and version != "1.0":
            problems.append(f"{rel(path)} contains stale audit archive path")

    changelog = CHANGELOG.read_text(encoding="utf-8", errors="ignore") if CHANGELOG.exists() else ""
    if not changelog_has_version(changelog, version):
        problems.append(f"{rel(CHANGELOG)} is missing a v{version} entry")
    return problems


def run_update(args: argparse.Namespace) -> int:
    version = normalise_version(args.version)
    release_date = normalise_date(args.date)
    changes: list[str] = []

    update_release_yml(version, release_date, changes)
    update_pack_archives(version, changes)
    update_pack_manifests(version, release_date, changes)
    update_prompt_display_versions(version, changes)
    update_audit_source_stamps(version, changes)
    update_changelog(version, release_date, args.summary, args.change, changes)

    if changes:
        print(f"Updated release version to v{version} ({release_date}):")
        for path in changes:
            print(f"  - {path}")
    else:
        print(f"Release metadata already aligned with v{version} ({release_date}).")

    problems = validate_release_consistency()
    if problems:
        print("\nVersion consistency problems remain:", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        return 1
    print("Version metadata consistency: OK")

    if args.build:
        scripts_dir = ROOT / "scripts"
        if str(scripts_dir) not in sys.path:
            sys.path.insert(0, str(scripts_dir))
        import build_all  # type: ignore
        return build_all.main(["--ci"])
    return 0


def run_check() -> int:
    problems = validate_release_consistency()
    if problems:
        print("Version metadata consistency: PROBLEMS FOUND")
        for problem in problems:
            print(f"  - {problem}")
        print("\nCommon fix:")
        print("  python scripts/update_version.py <version> --date YYYY-MM-DD")
        print("  python scripts/build_all.py --ci")
        return 1
    print("Version metadata consistency: OK")
    return 0


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Update Reflective Writer release/version metadata consistently.")
    parser.add_argument("version", nargs="?", help="new public version, for example 1.1")
    parser.add_argument("--date", help="release date as YYYY-MM-DD; defaults to today")
    parser.add_argument("--summary", default=DEFAULT_SUMMARY, help="summary paragraph for a new CHANGELOG.md entry")
    parser.add_argument("--change", action="append", default=[], help="bullet for a new CHANGELOG.md entry; may be supplied multiple times")
    parser.add_argument("--build", action="store_true", help="run python scripts/build_all.py --ci after updating version metadata")
    parser.add_argument("--check", action="store_true", help="check release/version metadata consistency without writing")
    args = parser.parse_args(argv)
    if not args.check and not args.version:
        parser.error("version is required unless --check is used")
    return args


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    if args.check:
        return run_check()
    return run_update(args)


if __name__ == "__main__":
    raise SystemExit(main())
