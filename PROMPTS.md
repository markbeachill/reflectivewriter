# PROMPTS.md — developer guide to the prompt files

This explains how the downloadable prompt libraries are structured and how to change
them. **The Markdown libraries in `docs/prompt-libraries/` are generated.** Edit the
Python sources in `scripts/` and rebuild; do not hand-edit the generated files.

## Source files

| File | Contents |
| --- | --- |
| `scripts/_shared.py` | Version, the activation instruction, `GLOBAL_RULES`, `MARKDOWN_RULES`, and the `manifest()`, `launcher()` and `router()` builders shared by every library. |
| `scripts/_tools_general.py` | The `_hdr()` header helper and the `RF` and `FW` tool lists. |
| `scripts/_tools_specialist.py` | The `NH`, `MD` and `US` tool lists (imports `_hdr`). |
| `scripts/build_prompt_libraries.py` | Assembles each library and the master file, writes them to `docs/prompt-libraries/latest/` and `docs/prompt-libraries/v1.0/`, and zips the mini libraries. |

## Anatomy of a built library

Each generated Markdown file is assembled in this order:

1. **Activation instruction** ("READ THIS FIRST") — tells the AI tool what it is and to
   wait for the user to type `prompt`.
2. **Manifest** (internal) — names the library and lists the tools.
3. **global-rules** — the rules that always apply. This is where the **no-ghost-writing
   ethic** lives: never invent the writer's experience, feelings, insight or learning;
   protect confidentiality and anonymity; supportive tone; honest register.
4. **markdown-output-rules** — keep output clean and readable.
5. **launcher** — the **only** place the on-screen menu is defined.
6. **router** (internal) — maps what the user types (numbers, codes, aliases) to a tool.
7. **One section per tool**, each beginning with the header from `_hdr()`.

## Tool definition format

Every tool is a dict. Example (from `_tools_general.py`):

```python
{
    "menu": 2, "code": "RF2", "id": "so-what-deepener",
    "title": "So-What Deepener",
    "use_when": "turn 'what happened' into 'what it meant and why it matters'",
    "menu_line": "**RF2 — So-What Deepener** — move from describing the event to analysing why it mattered.",
    "aliases": ["2", "RF2", "So-What Deepener", "So What Deepener"],
    "interaction": "interactive tutoring",
    "body": "...full markdown for the tool...",
}
```

| Key | Purpose |
| --- | --- |
| `menu` | Menu number within its library. |
| `code` | Short tool code (e.g. `RF2`, `NH4`). |
| `id` | Slug used in the generated `<!-- FILE: id.md -->` marker and YAML `id`. |
| `title` | Human title. |
| `use_when` | One line shown to help users pick the tool. |
| `menu_line` | The exact line printed in the launcher menu. |
| `aliases` | Everything the router accepts to reach this tool. |
| `interaction` | YAML `interaction_type` (usually `interactive tutoring`). |
| `body` | The tutoring script: diagnose → explain → worked example on unrelated content → ask the writer to attempt → review. |

The `_hdr()` helper emits the YAML front-matter (`id`, `tool_code`, `title`, `type`,
`menu_number`, `run_policy: selected_only`, `interaction_type`) and the `# CODE — Title`
heading, followed by `Apply global-rules. Run only this tool.`

## How each tool must behave

Tool bodies must respect the global rules. In particular a tool must **never**:

- write the user's reflection, or any portion of it, for them;
- invent what happened, how the user felt, what they realised, or what they learned;
- supply identifying detail or encourage the user to include it.

A tool **should**: ask first, explain the move, show an example on *different* content,
get the user to attempt it, then review. Support `prompt` (return to menu) and respond
to "I'm stuck" by making the next step smaller.

## Editing workflow

1. Edit the relevant tool dict or shared text in `scripts/`.
2. Rebuild:
   ```bash
   python scripts/build_prompt_libraries.py
   ```
3. If you bumped the version, update `VERSION` / `LAST_UPDATED` in `scripts/_shared.py`
   and `scripts/_site.py`, add a changelog entry in `scripts/build_site_pages.py`, and
   create a new `docs/prompt-libraries/vX.Y/` archive (the build writes the archive copy
   automatically using the current `VERSION`).
4. Rebuild the site:
   ```bash
   python scripts/build_site_main.py
   python scripts/build_site_pages.py
   ```
5. Run the CI check locally before pushing:
   ```bash
   python scripts/build_prompt_libraries.py --ci
   ```

## Adding a tool

Append a dict to the appropriate list (`RF`, `FW`, `NH`, `MD`, `US`) with a unique
`menu` number and `code`, a `menu_line`, sensible `aliases`, and a `body` that follows
the teaching loop and the global rules. Rebuild. The launcher and router are generated
from the lists, so the menu and routing update automatically.
