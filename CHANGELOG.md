# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [0.1.0] - 2026-05-01

### Added

- `.claude/skills/obsidian/SKILL.md` — vault read/write primitives (modes: init, daily-log, briefing, weekly, reading-list, decision, archive, lint). No-op if `vault_dir` unset.
- `.claude/skills/obsidian/scripts/{init_vault,lint_vault,archive}.py` — helper scripts for the obsidian skill.
- `.claude/skills/housekeep/SKILL.md` — weekly memory and skill audit (single-agent).
- `.claude/skills/housekeep/scripts/audit.py` — helper script for the housekeep skill.
- `.claude/skills/consolidate-learning/SKILL.md` — audit "Learned from runs" sections and promote/merge/prune.
- `config.yaml` — optional vault config (`vault_dir` plus subdirs). All settings optional.
- `vault-template/VAULT.md` — starter handbook for the user's vault root (PARA-aligned).

### Changed

- `CLAUDE.md` — Daily Ops table now lists 6 in-repo skills; added Shared Skills section (`kiloloop/oacp-skills`) and Multi-runtime section (`kiloloop/cortex`); Rule G (reading list, opt-in); Rule D vault-aware.
- `README.md` — knowledge-base positioning and Karpathy reference; Knowledge Base mode section; Shared Skills; Multi-runtime; v0.2.0 roadmap; `config.local.yaml` note.
- `.claude/skills/morning/SKILL.md` — loads `config.yaml`; optional vault peek and briefing write.
- `.claude/skills/evening/SKILL.md` — loads `config.yaml`; optional vault daily-log via `/obsidian daily-log`.
- `.gitignore` — adds `config.local.yaml` for personal overrides.

## [0.0.1] - 2026-04-30

### Added

- `CLAUDE.md` — persona, behavioral rules, memory map, daily ops table.
- `README.md` — public-facing intro: setup, daily use, customize.
- `.gitignore` — minimal exclusions (`.DS_Store`, swap files, IDE artifacts).
- `.claude/skills/{morning,evening,debrief}/SKILL.md` — initial 3-skill slate.
- `memory/{MEMORY,tasks,personal,priorities,decisions,feedback,learnings}.md` — 7 memory templates.

### Removed

- Legacy cortex-dev bootstrap content (CHANGELOG, CODE_OF_CONDUCT, CONTRIBUTING, DEVELOPMENT, LICENSE, SECURITY, SSOT, configs, claude/codex skill scaffolds). LICENSE re-added in this `oss-scaffolding` branch.

[0.1.0]: https://github.com/kiloloop/iantha/compare/v0.0.1...v0.1.0
[0.0.1]: https://github.com/kiloloop/iantha/releases/tag/v0.0.1
