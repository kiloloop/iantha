# Iantha

> Personal chief of staff + knowledge base curator, in markdown. A clone-and-run repo for Claude Code.

Iantha is a memory + skills bundle that turns Claude Code into a personal assistant for daily life — tasks, reminders, decisions, routines, anything you'd otherwise keep in your head. Clone the repo, launch Claude Code inside it, and you have an assistant that remembers across sessions.

Optionally point Iantha at an Obsidian vault and it doubles as a knowledge-base curator — daily notes, decisions, weekly reviews, and a reading list, all in plain markdown. The pattern is inspired by Andrej Karpathy's [LLM Knowledge Bases](https://x.com/karpathy) framing: raw material lands in your vault, an LLM helps you compile it into something queryable, and you keep editing in your IDE of choice (Obsidian).

## Setup

```bash
git clone https://github.com/kiloloop/iantha.git ~/iantha
cd ~/iantha
claude
```

That's it. Iantha reads `CLAUDE.md` and the `memory/` directory at session start.

## What's Inside

```
.
├── CLAUDE.md              # Persona, rules, memory map
├── README.md              # You're reading it
├── config.yaml            # Optional vault config (vault_dir + subdirs)
├── .claude/skills/        # /morning, /evening, /debrief, /obsidian, /housekeep, /consolidate-learning
├── memory/                # Tasks, personal context, decisions, learnings
└── vault-template/        # Starter VAULT.md to copy into your Obsidian vault
```

## Daily Use

| Command | When | What it does |
|---------|------|--------------|
| `/morning` | start of day | Briefs you on today's tasks, priorities, anything overdue |
| `/evening` | end of day | Archives what got done, rolls recurring tasks, notes tomorrow |
| `/debrief` | end of substantive session | Captures decisions, learnings, feedback into memory |
| `/obsidian` | as needed | Vault read/write primitives (no-op without `vault_dir`) |
| `/housekeep` | weekly | Audits memory + skills + vault hygiene |
| `/consolidate-learning` | monthly | Promotes skill "Learned from runs" entries into main instructions |

Plus two more skills installed from [`kiloloop/oacp-skills`](https://oacp.dev/skills/) (see "Shared Skills" below) — `/self-improve`, `/wrap-up`.

Outside those, just talk to Iantha. Mention "tomorrow" or "by Friday" — it auto-captures. Share preferences or routines — it remembers. Ask for context — it surfaces what's relevant.

## Memory

Iantha's persistent state is in `memory/`. The files are templates on first clone — they fill in as you use it.

| File | Purpose |
|------|---------|
| `tasks.md` | All actionable items (urgent / work / personal / recurring / archive) |
| `personal.md` | About you — preferences, routines, people, life context |
| `priorities.md` | What you're focused on right now |
| `decisions.md` | Decisions you've made, with date and rationale |
| `feedback.md` | Corrections you've given Iantha (so it doesn't repeat mistakes) |
| `learnings.md` | Operational knowledge — tool gotchas, workflow insights |
| `MEMORY.md` | Thin index, loaded at session start |

The repo is git-tracked. Commit your memory updates and your context follows you across machines.

## Knowledge Base mode (optional)

Set `vault_dir` in `config.yaml` to point Iantha at an Obsidian vault. Then:

- `/morning` and `/evening` append to `${vault_dir}/daily/YYYY-MM-DD.md`
- `/obsidian decision` files decisions into `${vault_dir}/decisions/`
- `/obsidian reading-list` queues docs for your review
- `/obsidian lint` flags broken wikilinks, stale `_to-delete/` items, orphans

Run `/obsidian init` once to seed the vault with the standard directories and copy `vault-template/VAULT.md` into it. The handbook there is the contract Iantha follows when writing.

```yaml
# config.yaml
vault_dir: ~/Documents/MyVault
```

If `vault_dir` is unset, every vault hook no-ops silently — Iantha works fully without a vault.

## Shared Skills

Two skills come from [`kiloloop/oacp-skills`](https://github.com/kiloloop/oacp-skills) (catalog: <https://oacp.dev/skills/>) rather than being shipped in-repo. Install once with:

```bash
npx skills add kiloloop/oacp-skills self-improve wrap-up
```

You get:

- `/self-improve` — audit CLAUDE.md, skills, and memory for drift
- `/wrap-up` — end-of-session orchestrator (cleanup + debrief + self-improve + commit). Composes with the in-repo `/debrief`.

Optional, install per-need: `/doctor`, `/check-inbox`, `/review-loop-*`.

## Multi-runtime setup (optional)

If you run Iantha alongside other agents (Claude Code + Codex + Gemini, etc.) and want them to share session memory across runtimes, look at [`kiloloop/cortex`](https://github.com/kiloloop/cortex) — a cross-session memory layer (SSOT + debrief inbox) built on the [OACP](https://github.com/kiloloop/oacp) protocol. Cortex publishes its own `/debrief` and `/sync` skills wired to a shared inbox; Iantha's in-repo `/debrief` is the single-agent equivalent.

For solo personal use, you don't need cortex.

## Personalize

The name "Iantha" is a default. To rename:

1. Edit `CLAUDE.md` — replace `Iantha` with your preferred name
2. Edit `README.md` and `memory/MEMORY.md` headers
3. Commit

Memory file conventions (timestamps, sections) are defined in `memory/MEMORY.md`. Adjust to your style.

For machine-specific overrides (real vault paths, your name) without polluting the public repo, create `config.local.yaml` next to `config.yaml` — it's gitignored and merges over the base config.

## Roadmap → v0.2.0

The current release covers the chief-of-staff half well. The knowledge-base half is intentionally minimal — Karpathy-style wiki compilation comes in v0.2.0:

- `/obsidian compile` — compile `raw/` (clippings, transcripts, raw notes) into curated `wiki/` entries
- `/obsidian ask` — Q&A over `wiki/` from the CLI
- Web-clipper / read-it-later ingest into `raw/`
- Marp slide rendering for wiki entries
- Vault search (full-text + semantic)

If you start collecting raw material in `raw/` now, the v0.2.0 compiler will work on what's already there.

## Upgrade Path

Iantha is the free, self-hosted starter. If you want a managed multi-agent version that coordinates across projects (work + life, multiple agents, cloud-synced), look at **Iris** — the paid product. *Iantha is your starter Iris.*

## Why "Iantha"

Greek for "violet flower." Iantha is the flower-pair sister of Iris (the rainbow goddess and flower) — naming chosen because the free starter complements the paid Iris.

## License

[Apache 2.0](LICENSE).
