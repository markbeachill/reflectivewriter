#!/usr/bin/env python3
"""Shared helpers for the Reflective Report Writing Tutor website build."""
from __future__ import annotations

import os
from pathlib import Path

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_PATH = Path(ROOT)
DOCS = os.path.join(ROOT, "docs")
RELEASE_YML = ROOT_PATH / "src" / "prompt-library" / "release.yml"


def _read_release_metadata() -> dict[str, str]:
    """Read the small release.yml file without requiring a YAML dependency."""
    data: dict[str, str] = {}
    if not RELEASE_YML.exists():
        return data
    for raw in RELEASE_YML.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, _, value = line.partition(":")
        data[key.strip()] = value.strip().strip("\"'")
    return data


_RELEASE = _read_release_metadata()
VERSION = _RELEASE.get("release_version") or _RELEASE.get("toolkit_version") or ""
LAST_UPDATED = _RELEASE.get("release_date") or _RELEASE.get("last_updated") or ""

BRAND = "Reflective Report Writing Tutor"
TAGLINE = "Reflect for yourself"

DESCRIPTION = (
    "A toolkit of downloadable prompt libraries that help you write honest, "
    "structured reflective reports yourself, with AI as a tutor rather than a "
    "ghost-writer."
)


def page(title, body, *, css="style.css", body_class="", base=""):
    nav_items = [
        ("Home", f"{base}index.html"),
        ("Try it", f"{base}try-it/"),
        ("Tools", f"{base}tools/"),
        ("Examples", f"{base}examples/"),
        ("Student Help", f"{base}student-help/"),
        ("Guides", f"{base}guides/"),
        ("Testing", f"{base}testing.html"),
    ]
    nav = "".join(f'<li><a href="{href}">{label}</a></li>' for label, href in nav_items)
    cls = f' class="{body_class}"' if body_class else ""
    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1" name="viewport"/>
<title>{title}</title>
<meta content="{DESCRIPTION}" name="description"/>
<link href="{base}{css}" rel="stylesheet"/>
</head>
<body{cls}>
<header><div class="container nav"><a class="brand" href="{base}index.html">{BRAND}<small>{TAGLINE}</small></a><nav><ul>{nav}</ul></nav></div></header>
{body}
<footer class="footer"><div class="container"><p>{BRAND}. Part of the AI Personal Tutor Toolkit family. Structured support for writing your own reflective reports.</p><p class="footer-links"><a href="{base}guides/anonymisation.html">Anonymisation</a> | <a href="{base}guides/frameworks.html">Frameworks</a> | <a href="{base}changelog/">Changelog</a> | <a href="{base}about.html">About this site</a></p></div></footer>
</body>
</html>"""


def write(rel, html):
    path = os.path.join(DOCS, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", rel)
