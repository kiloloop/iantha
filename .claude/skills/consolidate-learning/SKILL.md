---
name: consolidate-learning
description: Audits "Learned from runs" sections across .claude/skills/ — promotes durable lessons into the main SKILL.md body, prunes stale or already-covered entries. Use this whenever the user types /consolidate-learning, /housekeep flags a skill with a bloated learned section, the user asks to clean up skill learnings, says "this skill is getting cluttered," or a monthly cadence cycle hits. Conservative — proposes diffs for user approval before applying.
---

# /consolidate-learning — Audit "Learned from runs" Sections

Promote durable lessons from skill "Learned from runs" sections into the main instructions. Prune entries that are stale or already covered upstream.

## When to invoke

- A SKILL.md's "Learned from runs" section has >5 entries (surfaced by /housekeep).
- User typed `/consolidate-learning [skill-name]`.
- Monthly cadence (suggest at the end of /housekeep).

## Steps

For each `.claude/skills/*/SKILL.md` (or the named skill):

### 1. Read the skill

Look for a `## Learned from runs` (or similar) section. If absent, skip this skill.

### 2. Categorize each entry

For each lesson, decide:

- **Promote**: lesson is general guidance that applies every run → fold into the relevant section of the SKILL.md main body. Make sure the wording matches the rest of the doc. Then remove the entry from "Learned from runs".
- **Merge**: lesson is already implied or stated in the main body → remove the duplicate.
- **Prune**: lesson is stale (situation no longer applies, e.g., a tool was replaced) or one-off (specific to a single past run, no future relevance) → remove.
- **Keep**: lesson is not yet repeated enough to promote, still situational → leave in place.

### 3. Show the diff per skill

For each skill, show the user:

```
## <skill-name>

Promotions (N):
- "<lesson>" → into <section>
[diff preview]

Merges (M):
- "<lesson>" → already covered by <existing line>

Prunes (K):
- "<lesson>" → reason

Keeps (J): <list>
```

### 4. Apply with confirmation

User approves per skill. Apply edits. Update the SKILL.md's `*Updated:*` line if present.

### 5. Commit

Per skill:

```
<skill>: consolidate-learning — N promotions, M merges, K prunes
```

## Notes

- Conservative defaults: when in doubt, **keep**. Promotion bar is "applies every run, not just one situation."
- Don't promote lessons that are really feedback (corrections from the user) — those belong in `memory/feedback.md` instead.
- Don't promote tool gotchas — those go in `memory/learnings.md`.
- If a lesson reveals a missing rule in `CLAUDE.md`, propose adding the rule there separately.
- If a skill has zero entries to promote/merge/prune, say so cleanly: "<skill>: nothing to consolidate."
