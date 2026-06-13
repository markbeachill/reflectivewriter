#!/usr/bin/env python3
"""Build the Reflective Report Writing Tutor prompt libraries.

Assembles five mini libraries and one master library from shared scaffolding
and per-tool definitions, writes them to docs/prompt-libraries/latest/ and to a
fixed archive folder, and zips the mini libraries.

Usage:
    python scripts/build_prompt_libraries.py          # build into docs/
    python scripts/build_prompt_libraries.py --ci     # build + checks, no write needed
"""
import os
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _shared import (  # noqa: E402
    VERSION, activation, GLOBAL_RULES, MARKDOWN_RULES, manifest, launcher, router,
)
from _tools_general import LIB1_TOOLS, LIB2_TOOLS  # noqa: E402
from _tools_specialist import LIB3_TOOLS, LIB4_TOOLS, LIB5_TOOLS  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
LATEST = os.path.join(ROOT, "docs", "prompt-libraries", "latest")
ARCHIVE = os.path.join(ROOT, "docs", "prompt-libraries", f"v{VERSION}")

# --- Library definitions ---------------------------------------------------

LIBRARIES = [
    {
        "file": "01_reflective_foundations_library.md",
        "title": "Reflective Foundations Tutor Library",
        "purpose": "My job is to help you learn to reflect well and write a clear, honest reflective report in your own voice. Paste a passage of your own reflective writing and I will help you go deeper. I will not write your reflection for you.",
        "tools": LIB1_TOOLS,
        "footer": [
            "Choose a tool to get started, then paste a passage of your own reflective writing. Not sure which tool? Describe your problem in a sentence and I will suggest one or two.",
            "You can tell me your level, course or task so I can pitch the feedback properly, for example \"first-year education module\" or \"workplace CPD reflection\".",
            "If you have a prescribed reflective model (such as Gibbs), or a professional standard (such as NMC revalidation, a medical portfolio, or US service-learning), there are specialist libraries for those.",
        ],
    },
    {
        "file": "02_reflective_frameworks_library.md",
        "title": "Reflective Frameworks Tutor Library",
        "purpose": "My job is to help you apply a reflective model to your own experience, or to choose one. I will guide you through the model's stages and ask for your own content; I will not write your reflection for you.",
        "tools": LIB2_TOOLS,
        "footer": [
            "Not sure which model your course wants? Check your assignment brief first; many courses require a particular model. If you are still unsure, use FW5 to choose one.",
            "Choose a tool to get started, then tell me the experience you want to reflect on, in anonymised terms.",
        ],
    },
    {
        "file": "03_nhs_healthcare_reflection_library.md",
        "title": "NHS and Healthcare Reflection Tutor Library",
        "purpose": "My job is to help nurses, midwives, nursing associates and healthcare students write reflective accounts to UK / NMC expectations, including revalidation accounts and placement reflections. I will not write your account for you, and I will help you keep it anonymous.",
        "tools": LIB3_TOOLS,
        "footer": [
            "This library is built around NMC revalidation and UK healthcare practice, so I will not keep asking you about the format. Always confirm details against current NMC guidance and the official forms, which can change.",
            "Choose a tool to get started, and describe your experience in anonymised terms only. Never paste anything that could identify a patient, service user or colleague.",
        ],
    },
    {
        "file": "04_medical_reflection_library.md",
        "title": "Medical Reflection Tutor Library",
        "purpose": "My job is to help doctors, medical students, physician associates and anaesthesia associates write reflective entries focused on insight and learning, in line with UK medical reflective-practice guidance. I will not write your entry for you, and I will help you keep it anonymous.",
        "tools": LIB4_TOOLS,
        "footer": [
            "This library is built around The reflective practitioner guidance (Academy of Medical Royal Colleges, COPMeD, GMC and Medical Schools Council), so I will not keep asking you about the format. Confirm details against current guidance and your own college or deanery rules.",
            "Choose a tool to get started, and describe your experience in anonymised terms only. Never paste patient-identifiable or personal data.",
        ],
    },
    {
        "file": "05_us_academic_reflection_library.md",
        "title": "US and Academic Reflection Tutor Library",
        "purpose": "My job is to help students in US higher education reflect on experiential, civic and service-learning, using models such as DEAL, and to tie reflections to course outcomes. I will guide and question; I will not write your reflection for you.",
        "tools": LIB5_TOOLS,
        "footer": [
            "This library uses US higher-education reflection practice, including the DEAL model. It defaults to US English. Tell me your course and any rubric or learning outcomes so I can pitch the feedback properly.",
            "Choose a tool to get started, then tell me the experience you want to reflect on.",
        ],
    },
]


def render_library(lib, public_dir="prompt-libraries/latest"):
    public_path = f"{public_dir}/{lib['file']}"
    archive_name = lib["file"].replace(".md", f"_v{VERSION.replace('.', '_')}.md")
    archive_path = f"prompt-libraries/v{VERSION}/{archive_name}"

    parts = [activation(lib["title"])]
    parts.append("\n" + manifest(
        lib["title"], lib["tools"][0]["code"][:2], lib["tools"], public_path, archive_path,
    ))
    parts.append("\n" + GLOBAL_RULES)
    parts.append("\n" + MARKDOWN_RULES)

    menu_lines = [f"{t['menu']}. {t['menu_line']}" for t in lib["tools"]]
    parts.append("\n" + launcher(lib["title"], lib["purpose"], menu_lines, lib["footer"]))

    mapping_lines = []
    for t in lib["tools"]:
        aliases = ", ".join(f"`{a}`" for a in t["aliases"])
        mapping_lines.append(f"- {aliases} → run `{t['id']}`")
    parts.append("\n" + router(lib["title"], mapping_lines))

    for t in lib["tools"]:
        parts.append("\n" + t["body"])

    return "".join(parts), archive_name


def render_master():
    """One file containing every tool, with a single set of scaffolding."""
    all_tools = []
    for lib in LIBRARIES:
        all_tools.extend(lib["tools"])

    title = "Reflective Report Writing Tutor — Master Library"
    public_path = "prompt-libraries/latest/reflective_writing_tutor_master_library.md"
    archive_path = f"prompt-libraries/v{VERSION}/reflective_writing_tutor_master_library_v{VERSION.replace('.', '_')}.md"

    purpose = ("My job is to help you reflect well and write a clear, honest reflective report in "
               "your own voice, across general skills, named models, and professional standards "
               "(NHS / NMC, UK medical, and US academic). I will guide and question; I will not "
               "write your reflection for you.")

    parts = [activation(title)]

    # Master manifest groups tools by library
    rows = []
    for lib in LIBRARIES:
        rows.append(f"\n_{lib['title']}_\n")
        rows.append("| Menu | Code | ID | Tool title | Use when the writer wants to... |")
        rows.append("|---:|---|---|---|---|")
        for t in lib["tools"]:
            rows.append(f"| {t['menu']} | {t['code']} | {t['id']} | {t['title']} | {t['use_when']} |")
    manifest_block = f"""<!-- FILE: 00-manifest.md -->
---
id: manifest
title: {title}
type: manifest
run_policy: reference_only
version: {VERSION}
created_for: reflective report writing toolkit
---

This section is for internal reference only. Do not output this section to the user.

# {title}

**Version:** v{VERSION}
**Last updated:** prompt-library suite v{VERSION}
**Public download:** `{public_path}`
**Fixed archive:** `{archive_path}`

This master file contains every tool from all five mini libraries. Use a mini library instead if you are on a free AI plan or want to focus on one area. Activate only `03-launcher` at the start; for every tool use, apply `01-global-rules` and `04-router`.

## Available tools
{os.linesep.join(rows)}

<!-- END FILE -->
"""
    parts.append("\n" + manifest_block)
    parts.append("\n" + GLOBAL_RULES)
    parts.append("\n" + MARKDOWN_RULES)

    # Master launcher: grouped menu using full codes
    menu_lines = []
    for lib in LIBRARIES:
        menu_lines.append(f"\n**{lib['title']}**")
        for t in lib["tools"]:
            menu_lines.append(f"- {t['menu_line']}")
    footer = [
        "Tools are grouped by area. Type a tool code (for example `RF2`, `FW1`, `NH4`, `MD3`, `US1`) or describe what you need and I will suggest a tool.",
        "If you have a prescribed model or a professional standard, the matching group already builds it in, so I will not over-quiz you on format.",
        "Tell me your level, course, task and English variety so I can pitch the feedback properly.",
    ]
    parts.append("\n" + launcher(title, purpose, menu_lines, footer))

    # Master router: map every full code
    mapping_lines = []
    for t in all_tools:
        aliases = ", ".join(f"`{a}`" for a in t["aliases"] if not a.isdigit())
        mapping_lines.append(f"- {aliases} → run `{t['id']}`")
    extra = ("\n## Bare numbers in the master library\n\n"
             "Because tools share menu numbers across groups, a bare number is ambiguous in this "
             "master file. If the writer types only a number, ask which group they mean, or invite "
             "them to use the full code such as `RF1` or `NH1`.\n")
    parts.append("\n" + router(title, mapping_lines, extra))

    for t in all_tools:
        parts.append("\n" + t["body"])

    return "".join(parts)


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def main():
    ci = "--ci" in sys.argv
    os.makedirs(LATEST, exist_ok=True)
    os.makedirs(ARCHIVE, exist_ok=True)

    mini_files = []
    for lib in LIBRARIES:
        text, archive_name = render_library(lib)
        # basic checks
        assert "READ THIS FIRST" in text
        assert text.count("<!-- FILE:") >= len(lib["tools"]) + 4
        for marker in ("manifest", "global-rules", "launcher", "04-router"):
            assert marker in text, f"missing {marker} in {lib['file']}"
        write(os.path.join(LATEST, lib["file"]), text)
        write(os.path.join(ARCHIVE, archive_name), text)
        mini_files.append(lib["file"])
        print(f"built {lib['file']}  ({len(text):,} bytes, {len(lib['tools'])} tools)")

    master = render_master()
    write(os.path.join(LATEST, "reflective_writing_tutor_master_library.md"), master)
    write(os.path.join(ARCHIVE, f"reflective_writing_tutor_master_library_v{VERSION.replace('.', '_')}.md"), master)
    print(f"built master library ({len(master):,} bytes)")

    # zip the mini libraries
    zip_path = os.path.join(LATEST, "reflective_writing_tutor_mini_libraries.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for f in mini_files:
            z.write(os.path.join(LATEST, f), arcname=f)
    print(f"built {os.path.basename(zip_path)}")

    if ci:
        print("CI checks passed.")


if __name__ == "__main__":
    main()
