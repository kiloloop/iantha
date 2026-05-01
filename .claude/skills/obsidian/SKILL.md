---
name: obsidian
description: Vault read/write primitives for an optional Obsidian vault. Handles daily-log writes, decision filing, weekly reviews, reading-list maintenance, archiving, and lint. Use this whenever the user types /obsidian, wants to file a decision into their vault, asks to log something to today's daily note, mentions "vault" or "Obsidian," needs vault hygiene checks, or another skill (morning, evening, housekeep) needs to read or write the vault. No-op silently if config.yaml has no vault_dir.
---

# /obsidian — Vault Read/Write Primitives

Encode how Iantha consumes and writes to an Obsidian vault. No-op if `config.yaml` doesn't set `vault_dir`.

The deterministic parts (init, lint, archive) are bundled scripts so each invocation doesn't re-derive the recipe. Content writes (daily-log, decision, weekly) stay LLM-driven because they need session context.

## When to invoke

The user typed `/obsidian <mode> [args]`, OR another skill (morning, evening, housekeep) needs to read or write the vault.

## Step 0: Config check

Read `config.yaml` from the repo root. If `config.local.yaml` exists, merge it (local wins). If `vault_dir` is missing or commented out, say so and stop:

> "No `vault_dir` configured. Set it in `config.yaml` to enable vault writes."

Resolve `${vault_dir}` to an absolute path (expand `~`). Resolve subdirectories using `vault_daily`, `vault_weekly`, `vault_decisions`, etc. — fall back to defaults (`daily`, `weekly`, `decisions`, `tasks`, `personal`, `artifacts`) if a key is unset.

## Modes

### `init` — one-time vault setup

Run the bundled script:

```bash
python3 .claude/skills/obsidian/scripts/init_vault.py --vault-dir "$VAULT_DIR"
```

The script auto-finds `vault-template/VAULT.md` (pass `--template <path>` to override). It creates the standard subdirectories, copies `VAULT.md`, and writes a starter `reading-list.md`. Idempotent — never overwrites existing files. Reports created vs skipped.

**Example:**

```
$ python3 .claude/skills/obsidian/scripts/init_vault.py --vault-dir ~/Documents/MyVault
Vault: /Users/me/Documents/MyVault
Created: daily/, weekly/, decisions/, tasks/, personal/, artifacts/, _to-delete/, VAULT.md, reading-list.md
```

### `daily-log` — append or create today's daily note

Path: `${vault_dir}/${vault_daily}/YYYY-MM-DD.md`.

1. If the file doesn't exist, create with `# YYYY-MM-DD` header and `*Updated:*` line.
2. Append the caller's content under a `## <section>` heading. The caller passes the section name — `## Briefing` for /morning, `## Wrap` for /evening, `## Notes` for ad-hoc captures, etc.
3. Update the `*Updated:*` line.
4. Keep evening wraps to ≤ 30 lines; briefings to ≤ 20 lines. The LLM trims if needed.

**Why one mode for both briefing and wrap:** they're the same operation (append section to today's daily note) with different section names. One mode keeps the surface lean.

### `weekly` — write weekly review

Path: `${vault_dir}/${vault_weekly}/YYYY-WXX.md` (ISO week). Create if missing, otherwise append. Caller provides the body.

### `reading-list` — append a doc to the review queue

Path: `${vault_dir}/reading-list.md`. Append under `## Action Required`:

```
- [ ] [YYYY-MM-DD] [Title](relative/path.md) — one-line context
```

When the user reviews and decides, check off and move the line to `## Completed`.

### `decision` — file a new decision

Path: `${vault_dir}/${vault_decisions}/YYYY-MM-DD-kebab-title.md`. Body template:

```
# YYYY-MM-DD: [Title]

*Updated: YYYY-MM-DD HH:MM*

**Decision**: [what was decided]
**Why**: [reasoning]
**Notes**: [context, prior alternatives, links]
```

Also append a one-line summary to `memory/decisions.md` so the in-repo SSOT stays current.

**Example:**

User: *"Let's note we're going with the M5 MBA over the Pro for travel."*

Output: `${vault_dir}/decisions/2026-05-01-mba-m5-for-travel.md` with:

```
# 2026-05-01: MacBook Air M5 for travel

*Updated: 2026-05-01 14:22*

**Decision**: Use the M5 MBA as the travel laptop, not the 14" Pro.
**Why**: 1.24kg vs 1.55kg matters for long flights; M5 handles CC + light dev fine; battery life > Pro for the same workloads.
**Notes**: Pro stays as desk machine. Reconsider if travel workload shifts to multi-agent local runs.
```

Plus one line in `memory/decisions.md`:

```
- 2026-05-01 — MBA M5 for travel — chosen over 14" Pro on weight + battery. ([[2026-05-01-mba-m5-for-travel]])
```

### `archive <source>` — stage for deletion

Run the bundled script:

```bash
python3 .claude/skills/obsidian/scripts/archive.py --vault-dir "$VAULT_DIR" --source "decisions/2026-05-01-foo.md"
```

The script moves the file to `${vault_dir}/_to-delete/<flat-source>__<filename>`, preserving subdirectory info in the flattened name (so `research/topic/r1_foo.md` becomes `_to-delete/research_topic__r1_foo.md`). Refuses to overwrite — appends a timestamp on collision. Never hard-deletes; the user reviews `_to-delete/` periodically (handled in /housekeep).

### `lint` — vault hygiene check

Run the bundled script:

```bash
python3 .claude/skills/obsidian/scripts/lint_vault.py --vault-dir "$VAULT_DIR"
```

Reports (no auto-fixes):

- **Broken wikilinks**: `[[target]]` where target file is missing
- **Orphans**: markdown files no other file links to (excluding `daily/`, `weekly/`, `_to-delete/`, which are intentionally orphaned)
- **Stale `_to-delete/`**: items older than the SLA (default 14 days, override with `--sla-days`)
- **Misnamed**: files violating the ISO-date-prefix convention for their dir

Surface the report to the user. Ask before fixing anything.

## Vault Structure

PARA-aligned and slimmed for personal life:

| Directory | Purpose | Writer |
|-----------|---------|--------|
| `daily/` | Daily notes, briefings | /morning, /evening |
| `weekly/` | Weekly reviews | /obsidian weekly |
| `decisions/` | Decisions with rationale | /obsidian decision |
| `tasks/` | Task plans, checklists | manual |
| `personal/` | Personal docs (preferences, routines, contacts) | manual |
| `artifacts/` | Misc — brainstorms, drafts, references | manual |
| `_to-delete/` | Staging for deletion (human reviews) | /obsidian archive |

Optional Karpathy-mode dirs (v0.2.0 will lean on these):

| Directory | Purpose |
|-----------|---------|
| `wiki/` | Compiled, polished notes — the knowledge base |
| `raw/` | Ingested source material (clippings, quotes, raw notes) |

Top-level files:

| File | Purpose |
|------|---------|
| `VAULT.md` | This handbook (copy from `vault-template/VAULT.md`) |
| `reading-list.md` | Docs pending the user's review (Rule G) |

## Naming convention

**Standard**: ISO date prefix + kebab-case.

| Pattern | Example |
|---------|---------|
| `YYYY-MM-DD-kebab-title.md` | Dated outputs (decisions, dated artifacts) |
| `kebab-title.md` | Standing/reference docs (personal/, tasks/) |
| `YYYY-MM-DD.md` | Daily notes |
| `YYYY-WXX.md` | Weekly reviews (ISO week) |

## Write contract

- Only Iantha writes to the vault. Manual edits by the user are fine; other agents do not write here.
- Never hard-delete — stage in `_to-delete/`, the user confirms trash.
- Don't fabricate content. If memory/context doesn't have it, ask.
- Daily logs ≤ 30 lines per section; briefings ≤ 20 lines.
- All vault writes update the file's `*Updated:*` line if present.

## Learned from runs

(empty — populated as the skill is used)
