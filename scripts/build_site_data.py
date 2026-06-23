#!/usr/bin/env python3
"""Build generated JSON data used by the Reflective Writer static site.

This script mirrors the useful site-data pattern from the Tutor Prompts repo,
but keeps Reflective Writer's existing release metadata location:
``src/prompt-library/release.yml``.

Outputs:
  docs/data/release.json
  docs/data/tool_index.json
  docs/data/prompt_library_packs.json
  docs/data/source_material_index.json

Run from the repository root:
    python scripts/build_site_data.py
    python scripts/build_site_data.py --check
    python scripts/build_site_data.py --validate
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Sequence

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import build_examples as examples  # type: ignore  # local generator module
import build_prompt_libraries as bpl  # type: ignore  # local generator module
import build_source_material_library as source_material  # type: ignore  # local generator module

DATA_DIR = ROOT / "docs" / "data"
RELEASE_JSON = DATA_DIR / "release.json"
TOOL_INDEX_JSON = DATA_DIR / "tool_index.json"
PROMPT_LIBRARY_PACKS_JSON = DATA_DIR / "prompt_library_packs.json"
SOURCE_MATERIAL_INDEX_JSON = DATA_DIR / "source_material_index.json"

OUTPUTS = [
    RELEASE_JSON,
    TOOL_INDEX_JSON,
    PROMPT_LIBRARY_PACKS_JSON,
    SOURCE_MATERIAL_INDEX_JSON,
]
GENERATOR_VERSION = "1.0"


def json_text(data: Any) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def rel(path: Path | str | None) -> str | None:
    if path is None:
        return None
    p = ROOT / path if isinstance(path, str) else path
    try:
        return p.relative_to(ROOT).as_posix()
    except ValueError:
        return p.as_posix()


def read_release_metadata() -> dict[str, str]:
    raw = bpl.read_simple_yaml(bpl.RELEASE_YML)
    return {str(key): str(value) for key, value in raw.items()}


def release_data() -> dict[str, Any]:
    release = read_release_metadata()
    release_version = release.get("release_version") or release.get("toolkit_version", "")
    release_date = release.get("release_date") or release.get("last_updated", "")
    return {
        "generated_by": f"reflective-writer-site-data-v{GENERATOR_VERSION}",
        "release_version": release_version,
        "toolkit_version": release.get("toolkit_version", release_version),
        "prompt_library_version": release.get("prompt_library_version", release_version),
        "release_date": release_date,
        "last_updated": release.get("last_updated", release_date),
        "status": release.get("status", ""),
        "source": rel(bpl.RELEASE_YML),
    }


def configured_pack_files() -> list[Path]:
    return bpl.iter_packs()


def pack_records(metadata: dict[str, bpl.ToolMeta]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for pack_file in configured_pack_files():
        raw = bpl.read_simple_yaml(pack_file)
        tools = bpl.ordered_tool_meta(raw, metadata)
        pack_id = str(raw.get("id", ""))
        records.append({
            "id": pack_id,
            "title": str(raw.get("title", "")),
            "kind": "master" if pack_id == "master" else "mini-library",
            "source": rel(pack_file),
            "latest_output": str(raw.get("latest_output", "")),
            "archive_output": str(raw.get("archive_output", "")) if raw.get("archive_output") else None,
            "tool_metadata_mode": str(raw.get("tool_metadata_mode", "")),
            "tool_count": len(tools),
            "tool_codes": [tool.code for tool in tools],
            "tool_ids": [tool.id for tool in tools],
        })
    return records


def prompt_library_packs_data(metadata: dict[str, bpl.ToolMeta]) -> dict[str, Any]:
    packs = pack_records(metadata)
    kind_counts = Counter(pack["kind"] for pack in packs)
    return {
        **release_data(),
        "pack_count": len(packs),
        "master_pack_count": kind_counts.get("master", 0),
        "mini_library_pack_count": kind_counts.get("mini-library", 0),
        "packs": packs,
    }


def example_source_by_tool_id() -> dict[str, dict[str, str]]:
    loaded = examples.load_examples()
    out: dict[str, dict[str, str]] = {}
    for tool_id, item in loaded.items():
        code = str(item["code"])
        item_id = str(item["id"])
        out[tool_id] = {
            "id": item_id,
            "status": str(item.get("status", "")),
            "safety_level": str(item.get("safety_level", "")),
            "source": f"src/examples/items/{item_id}.yml",
            "page": f"docs/examples/example-{code.lower()}.html",
        }
    return out


def source_material_ids_by_tool_code() -> dict[str, list[str]]:
    by_code: dict[str, list[str]] = defaultdict(list)
    for item in source_material.load_items():
        by_code[item.tool_code].append(item.id)
    return {code: sorted(ids) for code, ids in by_code.items()}


def tool_index_data(metadata: dict[str, bpl.ToolMeta]) -> dict[str, Any]:
    packs = pack_records(metadata)
    example_by_tool = example_source_by_tool_id()
    source_material_by_code = source_material_ids_by_tool_code()
    tools: list[dict[str, Any]] = []
    for tool in metadata.values():
        included_in = [pack["id"] for pack in packs if tool.id in pack["tool_ids"]]
        example = example_by_tool.get(tool.id, {})
        source_material_ids = source_material_by_code.get(tool.code, [])
        tools.append({
            "code": tool.code,
            "id": tool.id,
            "title": tool.title,
            "family": tool.family,
            "family_label": tool.family_label,
            "mini_family_label": tool.mini_family_label,
            "source": f"src/prompt-library/tools/{tool.id}.md",
            "master_manifest_description": tool.master_manifest_description,
            "mini_manifest_description": tool.mini_manifest_description,
            "launcher_description": tool.launcher_description,
            "aliases": tool.aliases,
            "tool_mode": tool.tool_mode,
            "included_in_packs": included_in,
            "example_source": example.get("source"),
            "example_page": example.get("page"),
            "example_status": example.get("status"),
            "example_safety_level": example.get("safety_level"),
            "source_material_ids": source_material_ids,
            "source_material_count": len(source_material_ids),
        })
    mode_counts = Counter(tool.tool_mode for tool in metadata.values())
    family_counts = Counter(tool.family for tool in metadata.values())
    return {
        **release_data(),
        "tool_count": len(tools),
        "tool_mode_counts": dict(sorted(mode_counts.items())),
        "family_counts": dict((family, family_counts.get(family, 0)) for family in bpl.FAMILY_ORDER),
        "tools": tools,
    }


def source_material_index_data() -> dict[str, Any]:
    """Return the source-material index using its owning generator's payload.

Keeping this shape unchanged protects any existing page or downstream code that
expects `version` and `items` as the top-level fields.
    """
    return source_material.source_material_index_data()


def expected_outputs() -> dict[Path, str]:
    metadata = bpl.load_tool_metadata()
    bpl.validate_tool_files(metadata)
    # Validate pack/tool consistency before writing any data.
    for pack_file in configured_pack_files():
        bpl.ordered_tool_meta(bpl.read_simple_yaml(pack_file), metadata)
    return {
        RELEASE_JSON: json_text(release_data()),
        TOOL_INDEX_JSON: json_text(tool_index_data(metadata)),
        PROMPT_LIBRARY_PACKS_JSON: json_text(prompt_library_packs_data(metadata)),
        SOURCE_MATERIAL_INDEX_JSON: json_text(source_material_index_data()),
    }


def write_outputs() -> list[str]:
    changes: list[str] = []
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    for path, text in expected_outputs().items():
        old = path.read_text(encoding="utf-8") if path.exists() else None
        if old != text:
            path.write_text(text, encoding="utf-8")
            changes.append(rel(path) or str(path))
    return changes


def check_outputs() -> list[str]:
    changes: list[str] = []
    for path, text in expected_outputs().items():
        current = path.read_text(encoding="utf-8") if path.exists() else ""
        if current != text:
            changes.append(rel(path) or str(path))
    return changes


def validate_current_outputs() -> None:
    for path, expected_text in expected_outputs().items():
        if not path.exists():
            raise FileNotFoundError(f"Missing generated site data file: {rel(path)}")
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON in {rel(path)}: {exc}") from exc
        expected = json.loads(expected_text)
        if data != expected:
            raise ValueError(f"Generated site data is out of date: {rel(path)}")

    tool_data = json.loads(TOOL_INDEX_JSON.read_text(encoding="utf-8"))
    if tool_data.get("tool_count") != len(tool_data.get("tools", [])):
        raise ValueError("tool_index.json tool_count does not match tools length")

    pack_data = json.loads(PROMPT_LIBRARY_PACKS_JSON.read_text(encoding="utf-8"))
    if pack_data.get("pack_count") != len(pack_data.get("packs", [])):
        raise ValueError("prompt_library_packs.json pack_count does not match packs length")

    source_data = json.loads(SOURCE_MATERIAL_INDEX_JSON.read_text(encoding="utf-8"))
    if not isinstance(source_data.get("items"), list):
        raise ValueError("source_material_index.json items field is missing or not a list")


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build generated site integration JSON data.")
    parser.add_argument("--check", action="store_true", help="Fail if docs/data generated files are missing or out of date.")
    parser.add_argument("--validate", action="store_true", help="Validate source metadata and current docs/data generated files.")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    if args.check:
        changes = check_outputs()
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
    if args.validate:
        validate_current_outputs()
        print("Generated site data files validated.")
        return 0
    changes = write_outputs()
    if changes:
        print("Updated generated site data files:")
        for change in changes:
            print(f"  - {change}")
    else:
        print("No site data changes needed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
