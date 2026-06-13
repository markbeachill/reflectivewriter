# Reflective Report Writing Tutor

A toolkit of downloadable **prompt libraries** that turn an ordinary AI tool into a
*tutor* for reflective report writing — one that helps you write your own reflection
rather than writing it for you.

**Live site:** https://markbeachill.github.io/reflectivewriter/

It is part of the same family as the
[AI Personal Tutor Toolkit](https://markbeachill.github.io/tutorprompts/) and follows
the same tutor-not-ghost-writer design.

---

## What it is

Reflective writing is required across nursing, medicine, teaching, social work and
higher education, but it is rarely taught — and general AI tools make it trivial to
generate a plausible reflection that contains no actual reflection. This toolkit takes
the opposite approach. Each library is a Markdown file you upload to an AI tool; typing
`prompt` shows a menu of tools. Each tool diagnoses where your writing is, explains the
move you need, shows a worked example on unrelated content, asks you to attempt it, and
reviews what you wrote.

**The core rule:** the tutor never invents your experience, feelings, insight or
learning, and never produces a finished reflection for you. Because reflections involve
real people, anonymisation and confidentiality are built in.

## The libraries

Five libraries, thirty tools, plus a combined master library.

| Library | Audience | Tools |
| --- | --- | --- |
| **Reflective Foundations** (RF) | Anyone, any subject | Core reflection skills: description, the "so what", feelings, depth, action, voice |
| **Reflective Frameworks** (FW) | Told to use a named model | Gibbs; What? So What? Now What?; Kolb; Brookfield; Choose a Model; Anti-Box-Ticking |
| **NHS & Healthcare** (NH) | Nurses, midwives, students (NMC) | Revalidation accounts, placement, significant events, anonymisation, the Code, discussion prep |
| **Medical** (MD) | Doctors, students, PAs, AAs (UK) | Insight-focused entries, anonymisation & disclosure, significant events, tone, capability linkage |
| **US & Academic** (US) | US higher education | DEAL model, service-learning, journals, learning outcomes, ePortfolio, critical incidents |

Specialist libraries (NH, MD, US) build a professional standard in, so they ask fewer
setup questions.

## Repository layout

```
docs/                         GitHub Pages site (published from /docs)
  index.html                  Home
  tools/                      Tools index + one explore page per library
  examples/                   Example sessions
  student-help/               How to use the toolkit
  guides/                     Frameworks, anonymisation, teaching-approach
  changelog/                  Version history
  about.html
  style.css                   Calm paper aesthetic, indigo accent
  prompt-libraries/
    latest/                   Current downloadable libraries (+ zip of mini libraries)
    v1.0/                     Versioned archive copies
scripts/                      Generators (source of truth — edit here, then rebuild)
  _shared.py                  Activation text, global rules, manifest, launcher, router
  _tools_general.py           RF + FW tool definitions
  _tools_specialist.py        NH + MD + US tool definitions
  build_prompt_libraries.py   Builds the libraries into docs/prompt-libraries/
  _site.py                    Shared page template for the website
  build_site_main.py          Builds home + tools pages
  build_site_pages.py         Builds about, examples, student-help, guides, changelog
.github/workflows/            CI that rebuilds and checks the libraries
```

## Building

Requires Python 3 (standard library only).

```bash
# Rebuild the downloadable prompt libraries
python scripts/build_prompt_libraries.py

# Rebuild the website
python scripts/build_site_main.py
python scripts/build_site_pages.py
```

`python scripts/build_prompt_libraries.py --ci` runs the build with consistency checks
and is what the GitHub Action runs on every push.

## Publishing (GitHub Pages)

In the repository settings, set **Pages → Build and deployment → Source: Deploy from a
branch**, branch **main**, folder **/docs**. The `.nojekyll` file in `docs/` ensures the
plain HTML is served as-is.

## A note on customising

The prompt libraries are generated from `scripts/`. Edit the tool definitions there and
rebuild rather than editing the generated Markdown by hand, so the website downloads and
the archive copies stay in step. See [`PROMPTS.md`](PROMPTS.md) for the file format.

## Important limits

This project is not affiliated with the NMC, GMC, any medical royal college, or any
university. It summarises publicly available guidance to help you write your own
reflection; it does not replace your course, placement, employer or regulator's rules,
and it cannot guarantee anonymity.

## Credits

Created by [Dr Mark Beachill](https://www.linkedin.com/in/markbeachill/). Licensed under
the MIT License — see [`LICENSE`](LICENSE).
