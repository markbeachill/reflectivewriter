#!/usr/bin/env python3
"""Shared helpers for the Reflective Report Writing Tutor website build."""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
VERSION = "1.0"
LAST_UPDATED = "2026-06-13"

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
        ("Tools", f"{base}tools/"),
        ("Examples", f"{base}examples/"),
        ("Student Help", f"{base}student-help/"),
        ("Guides", f"{base}guides/"),
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
