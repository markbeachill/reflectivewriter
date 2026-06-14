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
  build_prompt_libraries.py   Compiles src/ into docs/prompt-libraries/ (+ --check, --ci)
  _site.py                    Shared HTML page template
  build_site_main.py          Home + tools pages
  build_site_pages.py         About, student-help, guides, changelog
  build_examples.py           Worked example pages (one per tool) using the chat CSS
docs/                    GitHub Pages site (published from /docs)
  index.html  tools/  examples/  student-help/  guides/  changelog/  about.html
  style.css              Main site stylesheet (calm paper, indigo accent)
  css/aichat*.css        Separate chat-bubble stylesheets for the example transcripts
  prompt-libraries/latest/    Current downloadable libraries (+ zip of the mini set)
  prompt-libraries/v1.0/      Versioned archive copies
.github/workflows/       CI that rebuilds and verifies the libraries and site
```

See [`PROMPTS.md`](PROMPTS.md) for the prompt-source format and
[`CUSTOMISING_PROMPTS.md`](CUSTOMISING_PROMPTS.md) for tailoring a local version.

## Page types

The site uses three layout types, selected by a `<body>` class in `style.css`:

- `home` — the landing page (hero + download cards).
- `reference` — reading pages: tools, examples, student help, guides, about, changelog.
- `menu` — an optional grid layout for menu-style pages.

Example pages additionally load a chat stylesheet (`css/aichat.css`) to render real
transcripts as chat bubbles. That CSS comes from a separate "AI chat" converter and is
kept apart from `style.css`; it is scoped under `.ai-chat-page` so the two never clash.

## Building

Requires Python 3 (standard library only).

```bash
# Compile the downloadable prompt libraries from src/
python scripts/build_prompt_libraries.py

# Verify the generated files are in sync with src/ (used by CI)
python scripts/build_prompt_libraries.py --check

# Rebuild the website
python scripts/build_site_main.py
python scripts/build_site_pages.py
python scripts/build_examples.py
```

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
