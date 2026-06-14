#!/usr/bin/env python3
"""Build the copy-ready source-material (practice passages) library.

Source items live in src/source-material/items/*.md, each with a small
front-matter block plus the Markdown passage to display and copy. Outputs:

  docs/source-material/index.html        a browsable, copy-ready page
  docs/source-material/latest/*.md       one downloadable file per item
  docs/data/source_material_index.json   a small index used by the page

Run from the repository root:
    python scripts/build_source_material_library.py
    python scripts/build_source_material_library.py --check
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List

from _site import page, BRAND

ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "src" / "source-material" / "items"
OUT_DIR = ROOT / "docs" / "source-material"
LATEST_DIR = OUT_DIR / "latest"
DATA_JSON = ROOT / "docs" / "data" / "source_material_index.json"
INDEX_HTML = OUT_DIR / "index.html"

REQUIRED = {"id", "title", "tool_code", "tool_title", "category", "use_when"}
CATEGORY_ORDER = [
    "Reflective Foundations",
    "Reflective Frameworks",
    "NHS & Healthcare",
    "Medical Reflection",
    "US & Academic",
]


@dataclass(frozen=True)
class Item:
    id: str
    title: str
    tool_code: str
    tool_title: str
    category: str
    use_when: str
    body: str


def parse(path: Path) -> Item:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, flags=re.DOTALL)
    if not m:
        raise ValueError(f"{path.name}: missing front matter")
    data = {}
    for raw in m.group(1).splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        key, _, value = line.partition(":")
        data[key.strip()] = value.strip()
    missing = REQUIRED - data.keys()
    if missing:
        raise ValueError(f"{path.name}: missing fields {sorted(missing)}")
    return Item(
        id=data["id"], title=data["title"], tool_code=data["tool_code"],
        tool_title=data["tool_title"], category=data["category"],
        use_when=data["use_when"], body=m.group(2).strip() + "\n",
    )


def load_items() -> List[Item]:
    items = [parse(p) for p in sorted(SRC_DIR.glob("*.md"))]
    order = {c: i for i, c in enumerate(CATEGORY_ORDER)}
    items.sort(key=lambda it: (order.get(it.category, 99), it.tool_code))
    return items


def render_index(items: List[Item]) -> str:
    cards = []
    current = None
    for it in items:
        if it.category != current:
            if current is not None:
                cards.append("</section>")
            cards.append(f'<section><h2>{html.escape(it.category)}</h2>')
            current = it.category
        body_html = html.escape(it.body)
        cards.append(
            '<article class="notice">'
            f'<span class="tag">{html.escape(it.tool_code)} &middot; {html.escape(it.tool_title)}</span>'
            f'<h3>{html.escape(it.title)}</h3>'
            f'<p>{html.escape(it.use_when)}</p>'
            f'<details><summary>Show passage</summary>'
            f'<pre class="source-block">{body_html}</pre></details>'
            f'<div class="actions"><a class="button secondary" href="latest/{it.id}.md" download>Download Markdown</a></div>'
            '</article>'
        )
    if current is not None:
        cards.append("</section>")
    body = f"""<main>
<article class="reading"><header class="page-intro"><p class="kicker">Resources</p><h1>Source material library</h1><p class="lead">Copy-ready practice passages for trying the tutor tools, demonstrating them, or running the deployment check. They are deliberately imperfect inputs — testing and teaching material, not work for submission.</p>
<div class="btn-row"><a class="button secondary" href="../guides/">Back to guides</a><a class="button secondary" href="../guides/deployment-check.html">Deployment check</a><a class="button secondary" href="../tools/">Browse tools</a></div></header>
<section class="notice"><span class="tag">How to use</span><p>Pick an item, open the passage, copy it, and paste it into the matching tutor tool. A good tool will diagnose the problem and set you a task; it will not silently rewrite the passage for you. The anonymisation items contain deliberately identifying detail and exist only to test that the tool flags it.</p></section>
{''.join(cards)}
</article></main>"""
    htmlpage = page(f"Source material | {BRAND}", body, base="../", body_class="reference")
    return htmlpage


def build(check: bool) -> int:
    items = load_items()
    # generated files: latest/*.md, index.html, data json
    expected = {}
    for it in items:
        expected[LATEST_DIR / f"{it.id}.md"] = it.body
    expected[INDEX_HTML] = render_index(items)
    index_data = {
        "version": "1.0",
        "items": [
            {"id": it.id, "title": it.title, "tool_code": it.tool_code,
             "tool_title": it.tool_title, "category": it.category,
             "use_when": it.use_when, "markdown": f"source-material/latest/{it.id}.md"}
            for it in items
        ],
    }
    expected[DATA_JSON] = json.dumps(index_data, indent=2, ensure_ascii=False) + "\n"

    if check:
        stale = []
        for path, content in expected.items():
            current = path.read_text(encoding="utf-8") if path.exists() else None
            if current != content:
                stale.append(str(path.relative_to(ROOT)))
        # also flag orphaned latest files
        if LATEST_DIR.exists():
            keep = {LATEST_DIR / f"{it.id}.md" for it in items}
            for p in LATEST_DIR.glob("*.md"):
                if p not in keep:
                    stale.append(str(p.relative_to(ROOT)) + " (orphaned)")
        if stale:
            print("Source-material outputs out of date:", file=sys.stderr)
            for s in stale:
                print("  " + s, file=sys.stderr)
            return 1
        print("Source-material library is up to date.")
        return 0

    LATEST_DIR.mkdir(parents=True, exist_ok=True)
    DATA_JSON.parent.mkdir(parents=True, exist_ok=True)
    # remove orphaned latest files
    keep = {f"{it.id}.md" for it in items}
    for p in LATEST_DIR.glob("*.md"):
        if p.name not in keep:
            p.unlink()
    for path, content in expected.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    print(f"built source-material: {len(items)} items + index + data json")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    return build(check=args.check)


if __name__ == "__main__":
    raise SystemExit(main())
