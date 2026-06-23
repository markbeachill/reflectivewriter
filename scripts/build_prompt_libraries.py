#!/usr/bin/env python3
"""Build the Reflective Report Writing Tutor prompt libraries from src/.

Source of truth is the file-based layout under src/prompt-library/:

  header.md                        activation instruction (top of every file)
  shared/01-global-rules.md        the no-ghost-writing ethic + global rules
  shared/02-markdown-output-rules.md
  tools/<id>.md                    one self-contained markdown file per tool
  tool-metadata.json               codes, titles, families, descriptions, aliases
  pack-sections/<pack>/{00-manifest,03-launcher,04-router}.md   literal text with
                                   {{AVAILABLE_TOOLS_TABLE}}, {{LAUNCHER_MENU}},
                                   {{MENU_MAPPING}} placeholders
  section-markers/<family>-tools.md   group dividers used in the master file
  packs/<pack>.yml                 which sections + tools make each library

Each pack YAML names its section files and tool files, plus latest_output and
archive_output paths. The build assembles header + sections + tools, fills the
generated placeholders from tool-metadata.json, writes the latest and archive
copies, and zips the five mini libraries.

Usage:
    python scripts/build_prompt_libraries.py            # build into docs/
    python scripts/build_prompt_libraries.py --check    # verify build is current
    python scripts/build_prompt_libraries.py --ci       # build + check (CI)
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Sequence

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SRC = ROOT / "src" / "prompt-library"
HEADER = SRC / "header.md"
TOOL_METADATA = SRC / "tool-metadata.json"
PACKS_DIR = SRC / "packs"
RELEASE_YML = SRC / "release.yml"

# Order families appear in the master file and in grouped menus.
FAMILY_ORDER = [
    "reflective-foundations",
    "reflective-frameworks",
    "nhs-healthcare",
    "medical",
    "us-academic",
]

MASTER_LIBRARY_CHOICES = [
    ("A", "reflective-foundations", "Reflective Foundations — use when you need core reflective-writing help."),
    ("B", "reflective-frameworks", "Reflective Frameworks — use when you have been told to use a named model."),
    ("C", "nhs-healthcare", "NHS & Healthcare — use for nursing, midwifery, healthcare and NMC-style reflection."),
    ("D", "medical", "Medical — use for UK medical, PA/AA or portfolio-style reflection."),
    ("E", "us-academic", "US & Academic — use for service-learning, journals, eportfolio or academic reflection."),
]

MINI_PACKS = [
    "reflective-foundations",
    "reflective-frameworks",
    "nhs-healthcare",
    "medical",
    "us-academic",
]
MINI_ZIP = ROOT / "docs" / "prompt-libraries" / "latest" / "reflective_writing_tutor_mini_libraries.zip"

ALLOWED_TOOL_MODES = {"routing_helper", "interactive", "full_review", "tiered_review"}


# --- metadata --------------------------------------------------------------
@dataclass
class ToolMeta:
    id: str
    code: str
    title: str
    family: str
    family_label: str
    mini_family_label: str
    master_manifest_description: str
    mini_manifest_description: str
    launcher_description: str
    tool_mode: str
    aliases: List[str] = field(default_factory=list)


def load_tool_metadata() -> Dict[str, ToolMeta]:
    data = json.loads(TOOL_METADATA.read_text(encoding="utf-8"))
    out: Dict[str, ToolMeta] = {}
    for entry in data["tools"]:
        tool_id = entry["id"]
        if tool_id in out:
            raise ValueError(f"Duplicate tool id in metadata: {tool_id}")
        tool_mode = entry.get("tool_mode")
        if tool_mode not in ALLOWED_TOOL_MODES:
            allowed = ", ".join(sorted(ALLOWED_TOOL_MODES))
            raise ValueError(f"Tool {tool_id} has invalid or missing tool_mode {tool_mode!r}; allowed: {allowed}")
        out[tool_id] = ToolMeta(
            id=tool_id,
            code=entry["code"],
            title=entry["title"],
            family=entry["family"],
            family_label=entry["family_label"],
            mini_family_label=entry["mini_family_label"],
            master_manifest_description=entry["master_manifest_description"],
            mini_manifest_description=entry["mini_manifest_description"],
            launcher_description=entry["launcher_description"],
            tool_mode=tool_mode,
            aliases=entry.get("aliases", []),
        )
    return out


def read_simple_yaml(path: Path) -> Dict[str, object]:
    """Minimal YAML reader for the flat pack files (scalars + simple lists)."""
    result: Dict[str, object] = {}
    current_key = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.startswith("  - "):
            if current_key is None:
                continue
            result.setdefault(current_key, [])
            result[current_key].append(raw[4:].strip())  # type: ignore[union-attr]
            continue
        if ":" in raw and not raw.startswith(" "):
            key, _, value = raw.partition(":")
            key = key.strip()
            value = value.strip()
            if value:
                result[key] = _unquote(value)
                current_key = None
            else:
                result[key] = []
                current_key = key
    return result


def _unquote(value: str) -> str:
    if len(value) >= 2 and value[0] in "\"'" and value[-1] == value[0]:
        return value[1:-1]
    return value


def read_source(rel_path: str) -> str:
    return (SRC / rel_path).read_text(encoding="utf-8")


def read_front_matter(path: Path) -> Dict[str, str]:
    """Read the simple YAML front matter used in tool markdown files."""
    text = path.read_text(encoding="utf-8")
    match = re.search(r"^---\n(.*?)\n---", text, flags=re.MULTILINE | re.DOTALL)
    if not match:
        raise ValueError(f"No YAML front matter found in {path.relative_to(ROOT)}")
    data: Dict[str, str] = {}
    for raw in match.group(1).splitlines():
        if not raw.strip() or raw.lstrip().startswith("#") or ":" not in raw:
            continue
        key, _, value = raw.partition(":")
        data[key.strip()] = _unquote(value.strip())
    return data


def validate_tool_files(metadata: Dict[str, ToolMeta]) -> None:
    """Ensure each source tool declares the canonical tool_mode from metadata."""
    errors: List[str] = []
    for tool in metadata.values():
        path = SRC / "tools" / f"{tool.id}.md"
        if not path.exists():
            errors.append(f"{tool.id}: missing source file {path.relative_to(ROOT)}")
            continue
        front_matter = read_front_matter(path)
        file_mode = front_matter.get("tool_mode")
        if file_mode != tool.tool_mode:
            errors.append(
                f"{tool.id}: tool file has tool_mode {file_mode!r}, metadata has {tool.tool_mode!r}"
            )
        if file_mode not in ALLOWED_TOOL_MODES:
            errors.append(f"{tool.id}: invalid tool file tool_mode {file_mode!r}")
    if errors:
        raise ValueError("Tool metadata validation failed:\n  " + "\n  ".join(errors))


# --- placeholder generation -------------------------------------------------
def grouped_tools(tools: Sequence[ToolMeta]) -> List[tuple[str, List[ToolMeta]]]:
    groups: List[tuple[str, List[ToolMeta]]] = []
    for family in FAMILY_ORDER:
        items = [t for t in tools if t.family == family]
        if items:
            groups.append((family, items))
    return groups


def generate_available_tools_table(spec: Dict[str, object], tools: Sequence[ToolMeta]) -> str:
    is_master = spec.get("id") == "master"
    groups = grouped_tools(tools) if is_master else [(tools[0].family, list(tools))]
    lines: List[str] = []
    for _family, items in groups:
        number = 1  # numbering restarts within each group
        heading = items[0].family_label if is_master else items[0].mini_family_label
        if lines:
            lines.append("")
        lines.append(f"**{heading}**")
        lines.append("")
        lines.append("| Menu | Code | ID | Tool title | Use when the writer wants to... |")
        lines.append("|---:|---|---|---|---|")
        for t in items:
            desc = t.master_manifest_description if is_master else t.mini_manifest_description
            lines.append(f"| {number} | {t.code} | {t.id} | {t.title} | {desc} |")
            number += 1
    return "\n".join(lines)


def _tool_menu_lines(tools: Sequence[ToolMeta], *, grouped: bool = False) -> List[str]:
    """Return visible menu lines for mini-library, family or full-tool menus."""
    lines: List[str] = []
    if grouped:
        number = 1
        for _family, items in grouped_tools(tools):
            if lines:
                lines.append("")
            lines.append(f"**{items[0].family_label}**")
            for t in items:
                lines.append(f"{number}. **{t.code} — {t.title}** — {t.launcher_description}")
                number += 1
        return lines
    for number, t in enumerate(tools, start=1):
        lines.append(f"{number}. **{t.code} — {t.title}** — {t.launcher_description}")
    return lines


def generate_launcher_menu(spec: Dict[str, object], tools: Sequence[ToolMeta]) -> str:
    is_master = spec.get("id") == "master"
    if is_master:
        return "\n".join(
            f"{letter}. **{label}**"
            for letter, _family, label in MASTER_LIBRARY_CHOICES
        )
    return "\n".join(_tool_menu_lines(tools))


def generate_master_family_menus(tools: Sequence[ToolMeta]) -> str:
    lines: List[str] = []
    by_family = {family: [t for t in tools if t.family == family] for family in FAMILY_ORDER}
    for letter, family, label in MASTER_LIBRARY_CHOICES:
        items = by_family.get(family, [])
        if not items:
            continue
        if lines:
            lines.append("")
        family_name = label.split(" — ", 1)[0]
        lines.append(f"### {letter} — {family_name}")
        lines.extend(_tool_menu_lines(items))
    return "\n".join(lines)


def generate_master_full_tool_menu(tools: Sequence[ToolMeta]) -> str:
    return "\n".join(_tool_menu_lines(tools, grouped=True))


def generate_number_routing_table(tools: Sequence[ToolMeta]) -> str:
    lines = ["| Writer choice | Code | Tool ID |", "|---:|---|---|"]
    for number, t in enumerate(tools, start=1):
        lines.append(f"| {number} | `{t.code}` | `{t.id}` |")
    return "\n".join(lines)


def generate_menu_mapping(spec: Dict[str, object], tools: Sequence[ToolMeta]) -> str:
    is_master = spec.get("id") == "master"
    lines: List[str] = []
    for number, t in enumerate(tools, start=1):
        if is_master:
            aliases = [a for a in t.aliases if not a.isdigit()] or [t.code]
        else:
            aliases = t.aliases or [str(number), t.code, t.title]
        alias_str = ", ".join(f"`{a}`" for a in aliases)
        lines.append(f"- {alias_str} → run `{t.id}`")
    return "\n".join(lines) + "\n"


def render_generated_sections(text: str, spec: Dict[str, object], tools: Sequence[ToolMeta]) -> str:
    replacements = {
        "{{AVAILABLE_TOOLS_TABLE}}": generate_available_tools_table(spec, tools),
        "{{LAUNCHER_MENU}}": generate_launcher_menu(spec, tools),
        "{{MASTER_FAMILY_MENUS}}": generate_master_family_menus(tools) if spec.get("id") == "master" else "",
        "{{MASTER_FULL_TOOL_MENU}}": generate_master_full_tool_menu(tools) if spec.get("id") == "master" else "",
        "{{NUMBER_ROUTING_TABLE}}": generate_number_routing_table(tools),
        "{{MENU_MAPPING}}": generate_menu_mapping(spec, tools),
    }
    for marker, generated in replacements.items():
        text = text.replace(marker, generated)
    if "{{" in text or "}}" in text:
        raise ValueError(f"Unresolved template marker in pack {spec.get('id')}")
    return text


def mini_tool_metadata(block: str, menu_number: int) -> str:
    """Renumber a tool's menu_number front-matter for its position in a mini pack."""
    return re.sub(r"^menu_number: .*$", f"menu_number: {menu_number}",
                  block, count=1, flags=re.MULTILINE)


# --- pack assembly ----------------------------------------------------------
def pack_tool_ids(spec: Dict[str, object]) -> List[str]:
    ids: List[str] = []
    for rel in spec.get("tools", []):  # type: ignore[union-attr]
        rel = str(rel)
        if rel.startswith("tools/"):
            ids.append(Path(rel).stem)
    return ids


def ordered_tool_meta(spec: Dict[str, object], metadata: Dict[str, ToolMeta]) -> List[ToolMeta]:
    out: List[ToolMeta] = []
    for tool_id in pack_tool_ids(spec):
        if tool_id not in metadata:
            raise ValueError(f"Pack {spec.get('id')}: no metadata for tool id {tool_id}")
        out.append(metadata[tool_id])
    return out


def build_pack(spec: Dict[str, object], metadata: Dict[str, ToolMeta]) -> tuple[Path, Path | None, str]:
    for key in ("id", "latest_output", "sections", "tools"):
        if key not in spec:
            raise ValueError(f"pack {spec.get('id')} missing required key: {key}")

    tool_meta = ordered_tool_meta(spec, metadata)
    mode = str(spec.get("tool_metadata_mode", "master"))

    parts: List[str] = [HEADER.read_text(encoding="utf-8")]
    for rel in spec["sections"]:  # type: ignore[union-attr]
        section = read_source(str(rel))
        section = render_generated_sections(section, spec, tool_meta)
        parts.append(section)

    menu_i = 0
    for rel in spec["tools"]:  # type: ignore[union-attr]
        rel = str(rel)
        block = read_source(rel)
        if rel.startswith("tools/"):
            menu_i += 1
            if mode == "mini":
                block = mini_tool_metadata(block, menu_i)
        parts.append(block)

    output_text = "\n\n\n".join(p.rstrip("\n") for p in parts).rstrip() + "\n"
    latest = ROOT / str(spec["latest_output"])
    archive = ROOT / str(spec["archive_output"]) if spec.get("archive_output") else None
    return latest, archive, output_text


def write_if_changed(path: Path, text: str) -> bool:
    old = path.read_text(encoding="utf-8") if path.exists() else None
    if old == text:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return True


# --- mini zip ---------------------------------------------------------------
def build_mini_zip_bytes(latest_dir: Path, metadata: Dict[str, ToolMeta]) -> bytes:
    import io
    names = []
    for pack_id in MINI_PACKS:
        spec = read_simple_yaml(PACKS_DIR / f"{pack_id}.yml")
        names.append(Path(str(spec["latest_output"])).name)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for name in names:
            z.write(latest_dir / name, arcname=name)
    return buf.getvalue()


# --- main -------------------------------------------------------------------
def iter_packs() -> List[Path]:
    # mini packs first (in defined order), then master
    files = [PACKS_DIR / f"{p}.yml" for p in MINI_PACKS]
    files.append(PACKS_DIR / "master.yml")
    return files


def run(check_only: bool) -> int:
    metadata = load_tool_metadata()
    validate_tool_files(metadata)
    changed: List[str] = []
    latest_dir = ROOT / "docs" / "prompt-libraries" / "latest"

    for pack_file in iter_packs():
        spec = read_simple_yaml(pack_file)
        latest, archive, text = build_pack(spec, metadata)
        for target in (latest, archive):
            if target is None:
                continue
            if check_only:
                current = target.read_text(encoding="utf-8") if target.exists() else None
                if current != text:
                    changed.append(str(target.relative_to(ROOT)))
            else:
                if write_if_changed(target, text):
                    print(f"built {target.relative_to(ROOT)}")
        if not check_only:
            n_tools = len(pack_tool_ids(spec))
            print(f"  {spec['id']}: {len(text):,} bytes, {n_tools} tools")

    # mini zip
    zip_bytes = build_mini_zip_bytes(latest_dir, metadata)
    if check_only:
        current = MINI_ZIP.read_bytes() if MINI_ZIP.exists() else b""
        # zip contents (names + payloads) compared, ignoring timestamps
        if _zip_payload(current) != _zip_payload(zip_bytes):
            changed.append(str(MINI_ZIP.relative_to(ROOT)))
    else:
        MINI_ZIP.parent.mkdir(parents=True, exist_ok=True)
        MINI_ZIP.write_bytes(zip_bytes)
        print(f"built {MINI_ZIP.relative_to(ROOT)}")

    if check_only:
        if changed:
            print("Out-of-date generated files:", file=sys.stderr)
            for c in changed:
                print(f"  {c}", file=sys.stderr)
            print("\nRun: python scripts/build_prompt_libraries.py", file=sys.stderr)
            return 1
        print("Prompt libraries are up to date.")
    return 0


def _zip_payload(data: bytes) -> Dict[str, bytes]:
    import io
    if not data:
        return {}
    out: Dict[str, bytes] = {}
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        for name in sorted(z.namelist()):
            out[name] = z.read(name)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the reflective-writing prompt libraries.")
    parser.add_argument("--check", action="store_true", help="verify generated files are current")
    parser.add_argument("--ci", action="store_true", help="build then check (for CI)")
    args = parser.parse_args()

    if args.check:
        return run(check_only=True)
    rc = run(check_only=False)
    if rc != 0:
        return rc
    if args.ci:
        rc = run(check_only=True)
        if rc == 0:
            print("CI checks passed.")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
