# Contributing to Iantha

Thank you for your interest in contributing!

Please read and follow our [Code of Conduct](https://github.com/kiloloop/.github/blob/main/CODE_OF_CONDUCT.md).

## What Iantha Is

Iantha is a clone-and-run repo for Claude Code: persona, memory templates, in-repo skills, and helper scripts. It is **not** a Python package — there is no `pyproject.toml`, no console scripts, and no PyPI release. Contributions are markdown edits, skill additions, and small helper-script changes.

## How to Contribute

### Reporting Issues

- Use [GitHub Issues](https://github.com/kiloloop/iantha/issues) to report bugs or request features.
- Search existing issues before creating a new one.
- For skill bugs, include the skill name, the command you ran, and the unexpected behavior.

### Pull Requests

1. Fork the repository and create a feature branch from `main`.
2. Make your changes with clear, focused commits.
3. CI (`.github/workflows/validate.yml`) runs markdown lint, Python syntax checks, and an absolute-path sweep on PRs — confirm it passes.
4. Open a PR against `main` with a clear description of what and why.
5. PRs require one approval before merging.

## Project Layout

```
iantha/
  CLAUDE.md                 persona, rules, memory map (entry point for Claude Code)
  README.md                 user-facing intro
  config.yaml               optional vault config
  .claude/skills/<name>/    in-repo skills (SKILL.md + optional scripts/)
  memory/                   memory templates (tasks, personal, decisions, etc.)
  vault-template/           starter VAULT.md for users with an Obsidian vault
```

## Adding or Editing a Skill

In-repo skills live under `.claude/skills/<skill-name>/`:

```
.claude/skills/<skill-name>/
  SKILL.md           required — slash command instructions
  scripts/           optional — helper Python scripts the skill invokes
```

Skill conventions:

- `SKILL.md` starts with YAML frontmatter (`name`, `description`).
- Scripts are Python 3.9+ standard library only (no external deps).
- Scripts that read or write user files must respect the `vault_dir` switch in `config.yaml` — no-op silently if it is unset.

## Conventions

- **Markdown**: ATX headings (`#`), one sentence per line in prose sections.
- **Python**: Standard library only. Add `# SPDX-FileCopyrightText: 2026 Kiloloop` and `# SPDX-License-Identifier: Apache-2.0` headers to new `.py` files.
- **YAML**: 2-space indentation. Match existing schema in `config.yaml`.
- **Memory files**: timestamps use `*Updated: YYYY-MM-DD HH:MM*`. Don't invent commitments or facts the user hasn't stated.
- **No machine-specific paths**: use `~/`, `$HOME`, or `<placeholder>`. Don't hardcode absolute home directories from your local machine.

## Commit Messages

- Use imperative mood: "Add feature" not "Added feature"
- Keep the first line under 72 characters
- Reference issue numbers where applicable: "Fix vault path expansion (#42)"

## License

By contributing, you agree that your contributions will be licensed under the [Apache 2.0 License](LICENSE).
