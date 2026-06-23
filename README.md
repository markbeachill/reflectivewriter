# Reflective Report Writing Tutor

A toolkit of downloadable **prompt libraries** that turn an ordinary AI tool into a
*tutor* for reflective report writing — one that helps you write your own reflection
rather than writing it for you.

**Live site:** https://markbeachill.github.io/reflectivewriter/

Part of the same family as the
[AI Personal Tutor Toolkit](https://markbeachill.github.io/tutorprompts/), and built
the same way: a file-based prompt source compiled into shareable Markdown libraries
and a plain-HTML GitHub Pages site.

## What it is

Each library is a Markdown file you upload to an AI tool; typing `prompt` shows a menu
of tools. Each tool diagnoses where your writing is, explains the move you need, shows
a worked example on unrelated content, asks you to attempt it, and reviews what you
wrote. **The core rule:** the tutor never invents your experience, feelings, insight or
learning. Because reflections involve real people, anonymisation is built in.

Five libraries, thirty tools, plus a combined master library:

| Library | Audience | Codes |
| --- | --- | --- |
| Reflective Foundations | Anyone, any subject | RF1–RF6 |
| Reflective Frameworks | Told to use a named model | FW1–FW6 |
| NHS & Healthcare | Nurses, midwives, students (NMC) | NH1–NH6 |
| Medical | Doctors, students, PAs, AAs (UK) | MD1–MD6 |
| US & Academic | US higher education | US1–US6 |

Specialist libraries build a professional standard in, so they ask fewer setup
questions.

## Repository layout

```
src/source-material/     SOURCE OF TRUTH for the practice-passage library
  items/<id>.md          One practice passage per file (front-matter + text)
src/examples/            SOURCE OF TRUTH for worked example pages
src/audit-library/       SOURCE OF TRUTH for the audit/testing pack
src/prompt-library/      SOURCE OF TRUTH for the prompt libraries (file-based)
  header.md              Activation instruction
  shared/                Global rules + Markdown-output rules
  tools/<id>.md          One file per tool (30)
  tool-metadata.json     Codes, titles, families, descriptions, aliases
  pack-sections/         Per-library manifest / launcher / router (with placeholders)
  section-markers/       Group dividers for the master file
  packs/<pack>.yml       Which sections + tools make each library
  release.yml            Version stamp
scripts/
  build_all.py                All-in-one rebuild/check/CI runner
  build_prompt_libraries.py   Compiles src/ into docs/prompt-libraries/ (+ --check, --ci)
  _site.py                    Shared HTML page template
  build_site_main.py          Home + tools pages
  build_site_pages.py         About, student-help, guides, changelog
  build_examples.py           Worked example pages (one per tool) using the chat CSS
  build_site_guides.py        Tutor guide, deployment check, educator + resource + workflow pages
  build_source_material_library.py  Copy-ready practice passages (from src/source-material/)
  build_site_data.py      Generated JSON data for release, tools, packs and source material
  build_audit_pack.py     Builds the Reflective Writer audit/testing pack
docs/                    GitHub Pages site (published from /docs)
  index.html  try-it/  tools/  examples/  student-help/  guides/  source-material/  testing.html  changelog/  about.html
  style.css              Main site stylesheet (calm paper, indigo accent)
  css/aichat*.css        Separate chat-bubble stylesheets for the example transcripts
  prompt-libraries/latest/    Current downloadable libraries (+ zip of the mini set)
  prompt-libraries/v1.0/      Versioned archive copies
  audit-library/latest/       Current audit/testing pack and ZIP
  audit-library/v1.0/         Versioned audit/testing archive copies
  data/                       Generated JSON for release, tools, packs and source material
.github/workflows/       CI that rebuilds and verifies the libraries and site
```

See [`PROMPTS.md`](PROMPTS.md) for the prompt-source format,
[`CUSTOMISING_PROMPTS.md`](CUSTOMISING_PROMPTS.md) for tailoring a local version, and
[`BUILD_AND_GENERATOR_GUIDE.md`](BUILD_AND_GENERATOR_GUIDE.md) plus
[`UPDATE-CHECKLISTS.md`](UPDATE-CHECKLISTS.md) for maintainer workflows. Current
maintainer notes live in [`project-docs/`](project-docs/).

## Page types

The site uses three layout types, selected by a `<body>` class in `style.css`:

- `home` — the landing page (hero + download cards).
- `reference` — reading pages: tools, examples, student help, guides, about, changelog.
- `menu` — an optional grid layout for menu-style pages.

Example pages additionally load a chat stylesheet (`css/aichat.css`) to render real
transcripts as chat bubbles. That CSS comes from a separate "AI chat" converter and is
kept apart from `style.css`; it is scoped under `.ai-chat-page` so the two never clash.

## Building

Requires Python 3 (standard library only). The detailed maintainer build guide is
[`BUILD_AND_GENERATOR_GUIDE.md`](BUILD_AND_GENERATOR_GUIDE.md); the short version is below.

```bash
# Rebuild all generated outputs
python scripts/build_all.py

# Run all available generated-output checks and Python compile checks
python scripts/build_all.py --check

# CI-style: rebuild, check, validate and compile
python scripts/build_all.py --ci
```

The individual generator scripts are still available for targeted work; see
[`BUILD_AND_GENERATOR_GUIDE.md`](BUILD_AND_GENERATOR_GUIDE.md) for the full map.

For tutors, the site includes a **deployment check** (`guides/deployment-check.html`)
— a ten-minute test that confirms a tool behaves like a tutor and refuses to
ghost-write on a given platform — plus a **testing/audit pack** (`testing.html`)
for release checks and a **source-material library** of copy-ready practice
passages used by those checks.

The prompt libraries are written from `src/`, so to change a tool you edit
`src/prompt-library/tools/<id>.md` (and `tool-metadata.json` if codes or names
change) and rebuild — never edit the generated Markdown by hand.

## Publishing (GitHub Pages)

Settings → Pages → Deploy from a branch → **main** → **/docs**. The `.nojekyll`
files keep the plain HTML served as-is.

## Important limits

Not affiliated with the NMC, GMC, any medical royal college, or any university. It
summarises publicly available guidance to help you write your own reflection; it does
not replace your course, placement, employer or regulator's rules, and it cannot
guarantee anonymity.

## Credits

Created by [Dr Mark Beachill](https://www.linkedin.com/in/markbeachill/).
Licensed under the MIT License — see [`LICENSE`](LICENSE).
