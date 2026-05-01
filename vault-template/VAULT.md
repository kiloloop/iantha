# Vault Handbook

> The write contract for Iantha when working in this Obsidian vault. Lives at the vault root so it's the first thing visible in Obsidian.
>
> Copy this file into your vault (or run `/obsidian init`).

## Directory map

PARA-aligned, slimmed for personal life:

| Directory | Purpose | Writer | Naming |
|-----------|---------|--------|--------|
| `daily/` | Daily notes, briefings | /morning, /evening | `YYYY-MM-DD.md`, `YYYY-MM-summary.md` |
| `weekly/` | Weekly reviews | /obsidian weekly | `YYYY-WXX.md` |
| `decisions/` | Decisions with rationale | /obsidian decision | `YYYY-MM-DD-kebab-title.md` |
| `tasks/` | Task plans, checklists | manual | `kebab-title.md` |
| `personal/` | Personal docs (preferences, routines, contacts) | manual | `kebab-title.md` |
| `artifacts/` | Brainstorms, drafts, references | manual | free-form |
| `_to-delete/` | Staging for deletion (human reviews) | /obsidian archive | flat, prefixed by source dir |

Optional Karpathy-mode dirs (v0.2.0 will lean on these):

| Directory | Purpose |
|-----------|---------|
| `wiki/` | Compiled, polished knowledge base |
| `raw/` | Ingested source material (clippings, quotes) |

## Top-level files

| File | Purpose | Maintained by |
|------|---------|---------------|
| `VAULT.md` | This handbook | Manual |
| `reading-list.md` | Docs pending your review (Rule G) | Iantha |

## Naming convention

**Standard**: ISO date prefix + kebab-case.

| Pattern | When | Example |
|---------|------|---------|
| `YYYY-MM-DD-kebab-title.md` | Dated outputs | `2026-05-01-quit-coffee.md` |
| `kebab-title.md` | Standing/reference docs | `morning-routine.md` |
| `YYYY-MM-DD.md` | Daily notes | `2026-05-01.md` |
| `YYYY-WXX.md` | Weekly reviews | `2026-W18.md` |

## File lifecycle

```
create → active → archive → _to-delete/ → trash
```

- Move to an `archive/` subdir when the project/decision is closed, or the file hasn't been referenced in 14+ days.
- Move to `_to-delete/` when archive isn't enough — staging for human deletion.
- Iantha never hard-deletes.

`_to-delete/` SLA:
- Reviewed during /housekeep (weekly).
- Files older than 14 days get flagged.
- Human confirms trash. Iantha never empties `_to-delete/`.

## Write ownership

**One rule: Only Iantha writes to this vault.**

Manual edits by you are fine — but no other agents or scripts touch the vault. All Iantha writes go through the `/obsidian` skill so the contract is consistent.

### Skills that write

| Skill | Writes to | What |
|-------|-----------|------|
| `/morning` | `daily/YYYY-MM-DD.md` | Morning briefing |
| `/evening` | `daily/YYYY-MM-DD.md` | Daily wrap (appends or creates) |
| `/obsidian decision` | `decisions/YYYY-MM-DD-*.md` | New decision |
| `/obsidian weekly` | `weekly/YYYY-WXX.md` | Weekly review |
| `/obsidian reading-list` | `reading-list.md` | Add review-pending doc |
| `/obsidian archive` | `_to-delete/` | Stage file for deletion |

## Karpathy-mode (optional, v0.2.0 roadmap)

If you create `wiki/` and/or `raw/`, Iantha will treat them per the Karpathy LLM-Knowledge-Bases pattern:

- `raw/` — drop in clippings, quotes, source material as-is.
- `wiki/` — Iantha helps you compile + curate a polished, query-friendly knowledge base from `raw/`.
- v0.2.0 will add a `/obsidian compile` mode (raw → wiki) plus Q&A and lint over `wiki/`.

For now, the dirs are inert. Use them if you want to start collecting raw material; the compiler ships in v0.2.0.

## Cleanup procedures

1. Read content, not just filenames — names can mislead.
2. Never hard-delete. Stage in `_to-delete/`.
3. Update broken wikilinks after batch moves.
4. Remove empty directories after moves.
5. Archive by topic, not by location — multi-round work belongs together.
