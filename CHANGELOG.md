# Changelog

## v1.1 — 2026-06-23

Architecture and maintenance refresh for the Reflective Writer prompt-library system.

- Added help, stuckness and EAL behaviour across the prompt libraries.
- Added explicit `tool_mode` metadata and validation for all 30 tools.
- Changed the master library to family-first routing while preserving direct tool codes.
- Moved worked examples into structured source records with privacy and authorship checks.
- Added generated site-data JSON for release, tools, packs and source material.
- Added a lightweight audit/testing pack for reflective-writing failure modes.
- Added maintainer documentation and an all-in-one build/check runner.
- Added a version-update workflow so release metadata, archives, prompt manifests, audit stamps, changelog and site output stay aligned.

## v1.0 — 2026-06-13

First public release.

- Two general libraries: Reflective Foundations and Reflective Frameworks.
- Three specialist libraries: NHS & Healthcare (NMC), Medical (GMC / AoMRC), and US & Academic (DEAL).
- Thirty tools in total, plus a combined master library.
- Strengthened no-ghost-writing rule: the tutor never invents the writer's experience, feelings, insight or learning.
- Anonymisation and confidentiality checks built into the healthcare and medical libraries, with a dedicated safety guide.
- Worked example pages for every tool, shown as chat transcripts using a separate chat stylesheet.
- Tutor and teacher guide, an educator case, and a ten-minute deployment check for confirming a tool refuses to ghost-write before classroom use.
- Source-material library of copy-ready practice passages, plus student guides for the reflective writing workflow and AI setup.
- A “Try it” page linking hosted ChatGPT and Gemini versions of the tutor, with a privacy and behaviour warning.
- File-based prompt source under `src/`: one Markdown file per tool, with pack manifests compiled by the build script.
