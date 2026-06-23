#!/usr/bin/env python3
"""Generate worked example pages for every Reflective Writer tool.

Example source records live in ``src/examples/items/*.yml``. Each record is a
short, fictional or composite teaching exchange with explicit privacy and
authorship checks. The generated pages live in ``docs/examples/`` and are styled
with ``css/aichat.css``.

Run from the repository root:
    python scripts/build_examples.py
    python scripts/build_examples.py --check
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

import yaml

from _site import page, BRAND

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
META_PATH = ROOT / "src" / "prompt-library" / "tool-metadata.json"
EXAMPLES_DIR = ROOT / "src" / "examples" / "items"
OUT_DIR = DOCS / "examples"

META = json.loads(META_PATH.read_text(encoding="utf-8"))

FAMILY_LABELS = {
    "reflective-foundations": "Reflective Foundations",
    "reflective-frameworks": "Reflective Frameworks",
    "nhs-healthcare": "NHS & Healthcare",
    "medical": "Medical Reflection",
    "us-academic": "US & Academic",
}
FAMILY_ORDER = ["reflective-foundations", "reflective-frameworks", "nhs-healthcare", "medical", "us-academic"]

ALLOWED_STATUS = {"public", "draft", "internal"}
ALLOWED_SAFETY_LEVELS = {"fictional", "composite", "anonymised_real", "internal_test"}
ALLOWED_ROLES = {"student", "tutor"}
PUBLIC_REQUIRED_CHECKS = {
    "authorship_boundary",
    "no_identifying_detail",
    "unrelated_made_up_example_only",
    "no_finished_reflection",
    "privacy_reviewed",
}


def _require_text(item: Dict[str, Any], field: str, source: Path) -> str:
    value = item.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{source.name}: `{field}` must be a non-empty string")
    return value.strip()


def _validate_example(item: Dict[str, Any], source: Path, tool_by_id: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    item_id = _require_text(item, "id", source)
    code = _require_text(item, "code", source)
    tool_id = _require_text(item, "tool_id", source)
    _require_text(item, "title", source)
    _require_text(item, "context", source)
    _require_text(item, "learning_point", source)
    _require_text(item, "privacy_note", source)

    if tool_id not in tool_by_id:
        raise ValueError(f"{source.name}: unknown tool_id `{tool_id}`")
    if tool_by_id[tool_id]["code"] != code:
        expected = tool_by_id[tool_id]["code"]
        raise ValueError(f"{source.name}: code `{code}` does not match tool `{tool_id}` ({expected})")
    if item_id != f"{code.lower()}-{tool_id}":
        raise ValueError(f"{source.name}: id should be `{code.lower()}-{tool_id}`")

    status = _require_text(item, "status", source)
    if status not in ALLOWED_STATUS:
        raise ValueError(f"{source.name}: status must be one of {sorted(ALLOWED_STATUS)}")

    safety_level = _require_text(item, "safety_level", source)
    if safety_level not in ALLOWED_SAFETY_LEVELS:
        raise ValueError(f"{source.name}: safety_level must be one of {sorted(ALLOWED_SAFETY_LEVELS)}")

    transcript = item.get("transcript")
    if not isinstance(transcript, list) or len(transcript) < 2:
        raise ValueError(f"{source.name}: transcript must contain at least two turns")
    for idx, turn in enumerate(transcript, start=1):
        if not isinstance(turn, dict):
            raise ValueError(f"{source.name}: transcript turn {idx} must be a mapping")
        role = turn.get("role")
        if role not in ALLOWED_ROLES:
            raise ValueError(f"{source.name}: transcript turn {idx} role must be `student` or `tutor`")
        html = turn.get("html")
        if not isinstance(html, str) or not html.strip():
            raise ValueError(f"{source.name}: transcript turn {idx} needs non-empty `html`")

    checks = item.get("checks")
    if not isinstance(checks, dict):
        raise ValueError(f"{source.name}: checks must be a mapping")
    if status == "public":
        missing = sorted(PUBLIC_REQUIRED_CHECKS - checks.keys())
        failed = sorted(k for k in PUBLIC_REQUIRED_CHECKS if checks.get(k) is not True)
        if missing:
            raise ValueError(f"{source.name}: public example missing checks {missing}")
        if failed:
            raise ValueError(f"{source.name}: public example failed checks {failed}")
        if safety_level in {"anonymised_real", "internal_test"}:
            raise ValueError(
                f"{source.name}: public examples should normally be fictional or composite; "
                f"got `{safety_level}`"
            )

    return item


def load_examples() -> Dict[str, Dict[str, Any]]:
    tool_by_id = {tool["id"]: tool for tool in META["tools"]}
    files = sorted(EXAMPLES_DIR.glob("*.yml"))
    if not files:
        raise ValueError(f"No example source files found in {EXAMPLES_DIR.relative_to(ROOT)}")

    by_tool: Dict[str, Dict[str, Any]] = {}
    seen_ids = set()
    for source in files:
        raw = yaml.safe_load(source.read_text(encoding="utf-8"))
        if not isinstance(raw, dict):
            raise ValueError(f"{source.name}: YAML root must be a mapping")
        item = _validate_example(raw, source, tool_by_id)
        if item["id"] in seen_ids:
            raise ValueError(f"{source.name}: duplicate example id `{item['id']}`")
        if item["tool_id"] in by_tool:
            raise ValueError(f"{source.name}: duplicate example for tool `{item['tool_id']}`")
        seen_ids.add(item["id"])
        by_tool[item["tool_id"]] = item

    missing = [tool["id"] for tool in META["tools"] if tool["id"] not in by_tool]
    if missing:
        raise ValueError("Missing example source for: " + ", ".join(missing))

    return by_tool


def chat_block(turns: Iterable[Dict[str, str]]) -> str:
    rows = []
    for turn in turns:
        source_role = turn["role"]
        css_role = "user" if source_role == "student" else "chatbot"
        label = "User" if css_role == "user" else "Chatbot"
        rows.append(
            f'      <section class="ai-chat-turn ai-chat-{css_role} ai-chat-turn--{css_role}">\n'
            f'        <div class="ai-chat-role">{label}</div>\n'
            f'        <div class="ai-chat-bubble">{turn["html"]}</div>\n'
            f'      </section>'
        )
    inner = "\n".join(rows)
    return (
        '<section class="ai-chat-page" aria-label="Example chat">\n'
        '  <div class="ai-chat-window">\n'
        '    <div class="ai-chat-log">\n'
        f'{inner}\n'
        '    </div>\n'
        '  </div>\n'
        '</section>'
    )


def example_page(meta: Dict[str, Any], example: Dict[str, Any]) -> Tuple[Path, str]:
    code = meta["code"]
    title = meta["title"]
    lead = example["context"]
    privacy_note = example["privacy_note"]
    learning_point = example["learning_point"]
    body = (
        f'<main>\n<article class="reading"><header class="page-intro">'
        f'<p class="kicker">Example</p><h1>{code} — {title}</h1>'
        f'<p class="lead">{lead} This is one short exchange; real sessions continue interactively, responding to what you actually write.</p>'
        f'<div class="btn-row"><a class="button secondary" href="./">All examples</a>'
        f'<a class="button secondary" href="../tools/">Browse tools</a></div></header></article>\n'
        f'{chat_block(example["transcript"])}\n'
        f'<div class="container"><p class="small-note">The tutor questions, diagnoses and teaches, but never writes your experience, feelings, insight or learning. That boundary is the whole point.</p>'
        f'<p class="small-note"><strong>Example safety:</strong> {privacy_note}</p>'
        f'<p class="small-note"><strong>What this demonstrates:</strong> {learning_point}</p></div>\n'
        f'</main>'
    )
    css_extra = '<link href="../css/aichat.css" rel="stylesheet"/>'
    html = page(f"{code} {title} example | {BRAND}", body, base="../", body_class="reference")
    html = html.replace(
        '<link href="../style.css" rel="stylesheet"/>',
        '<link href="../style.css" rel="stylesheet"/>\n' + css_extra,
    )
    return OUT_DIR / f"example-{code.lower()}.html", html


def build_index(tools_by_family: Dict[str, List[Dict[str, Any]]]) -> Tuple[Path, str]:
    rows = []
    for fam in FAMILY_ORDER:
        rows.append(f'<tr><th colspan="3">{FAMILY_LABELS[fam]}</th></tr>')
        for meta in tools_by_family[fam]:
            code = meta["code"]
            rows.append(
                f'<tr><td><strong>{code}</strong></td><td>{meta["title"]}</td>'
                f'<td><a href="example-{code.lower()}.html">Open example</a></td></tr>'
            )
    table = "\n".join(rows)
    body = f"""<main><article class="reading"><header class="page-intro"><p class="kicker">Examples</p><h1>Worked examples for every tool</h1><p class="lead">Each page shows a short teaching exchange: fictional or composite writing pasted in, and the tutor's reply. The tutor diagnoses, teaches and sets a task — it never writes the reflection. Examples are rendered in a chat style using a separate stylesheet (<code>css/aichat.css</code>).</p></header>
<section class="notice"><span class="tag">Behind the examples</span><p>The public examples are generated from structured source records with privacy and authorship checks. Tutors creating local examples should read the <a href="../guides/creating-examples.html">creating safe examples guide</a>.</p></section>
<section>
<table><thead><tr><th aria-label="Tool code"></th><th>Tool</th><th>Example</th></tr></thead><tbody>
{table}
</tbody></table>
</section>
<section><h2>Ready to try one yourself?</h2><div class="btn-row"><a class="button" href="../student-help/">Go to student help</a><a class="button secondary" href="../tools/">Browse all tools</a><a class="button secondary" href="../index.html#downloads">Download a library</a></div></section>
</article></main>"""
    html = page(f"Examples | {BRAND}", body, base="../", body_class="reference")
    html = html.replace(
        '<link href="../style.css" rel="stylesheet"/>',
        '<link href="../style.css" rel="stylesheet"/>\n<link href="../css/aichat.css" rel="stylesheet"/>',
    )
    return OUT_DIR / "index.html", html


def expected_outputs() -> Dict[Path, str]:
    examples = load_examples()
    by_family = {family: [] for family in FAMILY_ORDER}
    for tool in META["tools"]:
        by_family[tool["family"]].append(tool)

    expected: Dict[Path, str] = {}
    for tool in META["tools"]:
        path, html = example_page(tool, examples[tool["id"]])
        expected[path] = html
    path, html = build_index(by_family)
    expected[path] = html
    return expected


def build(check: bool = False) -> int:
    try:
        expected = expected_outputs()
    except Exception as exc:  # keep the CLI message short and readable
        print(f"Example build failed: {exc}", file=sys.stderr)
        return 1

    if check:
        stale = []
        for path, content in expected.items():
            current = path.read_text(encoding="utf-8") if path.exists() else None
            if current != content:
                stale.append(str(path.relative_to(ROOT)))
        keep = {path.name for path in expected if path.parent == OUT_DIR}
        if OUT_DIR.exists():
            for path in OUT_DIR.glob("example-*.html"):
                if path.name not in keep:
                    stale.append(str(path.relative_to(ROOT)) + " (orphaned)")
        if stale:
            print("Example outputs out of date:", file=sys.stderr)
            for item in stale:
                print("  " + item, file=sys.stderr)
            return 1
        print("Worked examples are up to date.")
        return 0

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    keep = {path.name for path in expected if path.parent == OUT_DIR}
    for path in OUT_DIR.glob("example-*.html"):
        if path.name not in keep:
            path.unlink()
    for path, content in expected.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print("wrote", path.relative_to(DOCS))
    print(f"built {len(META['tools'])} example pages + index from {EXAMPLES_DIR.relative_to(ROOT)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="verify generated example pages are current")
    args = parser.parse_args()
    return build(check=args.check)


if __name__ == "__main__":
    raise SystemExit(main())
