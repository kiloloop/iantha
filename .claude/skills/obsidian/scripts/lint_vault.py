#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kiloloop
# SPDX-License-Identifier: Apache-2.0
"""Vault hygiene check.

Reports (does NOT auto-fix):
- Broken wikilinks: [[target]] where target file is missing
- Orphans: markdown files no other file links to (excluding daily/weekly notes,
  which are intentionally orphaned)
- Stale _to-delete/: items older than the SLA (default 14 days)
- Misnamed: files that violate the ISO-date-prefix convention for their dir

Usage:
    python lint_vault.py --vault-dir ~/Documents/MyVault [--sla-days 14]
"""

from __future__ import annotations

import argparse
import re
import sys
import time
from collections import defaultdict
from pathlib import Path

# Dirs whose files are expected to be orphans (nothing links to them by design).
ORPHAN_OK_DIRS = {"daily", "weekly", "_to-delete"}

WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:\|[^\]]*)?\]\]")
DATE_PREFIX_RE = re.compile(r"^\d{4}-\d{2}-\d{2}([-_].+)?\.md$")
DATE_ONLY_RE = re.compile(r"^\d{4}-\d{2}-\d{2}\.md$")
ISO_WEEK_RE = re.compile(r"^\d{4}-W\d{2}\.md$")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--vault-dir", required=True)
    parser.add_argument("--sla-days", type=int, default=14)
    args = parser.parse_args()

    vault = Path(args.vault_dir).expanduser().resolve()
    if not vault.exists():
        print(f"ERROR: vault dir {vault} doesn't exist.", file=sys.stderr)
        return 1

    md_files = [p for p in vault.rglob("*.md") if ".obsidian" not in p.parts]

    name_index: dict[str, list[Path]] = defaultdict(list)
    for p in md_files:
        name_index[p.stem].append(p)

    broken_links: list[tuple[Path, str, int]] = []
    referenced: set[Path] = set()

    for p in md_files:
        try:
            text = p.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for ln, line in enumerate(text.splitlines(), 1):
            for match in WIKILINK_RE.finditer(line):
                target = match.group(1).strip()
                if not target:
                    continue
                # Strip embed prefix (![[...]])
                stem = Path(target).stem
                if stem in name_index:
                    referenced.update(name_index[stem])
                else:
                    broken_links.append((p.relative_to(vault), target, ln))

    orphans: list[Path] = []
    for p in md_files:
        if p in referenced:
            continue
        rel = p.relative_to(vault)
        if rel.parts and rel.parts[0] in ORPHAN_OK_DIRS:
            continue
        if rel.name in {"VAULT.md", "reading-list.md"}:
            continue
        orphans.append(rel)

    sla_seconds = args.sla_days * 86400
    now = time.time()
    stale_to_delete: list[tuple[Path, int]] = []
    to_delete_dir = vault / "_to-delete"
    if to_delete_dir.exists():
        for p in to_delete_dir.iterdir():
            if not p.is_file():
                continue
            age = int((now - p.stat().st_mtime) // 86400)
            if (now - p.stat().st_mtime) >= sla_seconds:
                stale_to_delete.append((p.relative_to(vault), age))

    misnamed: list[Path] = []
    for p in md_files:
        rel = p.relative_to(vault)
        if not rel.parts:
            continue
        top = rel.parts[0]
        name = rel.name
        if top == "daily" and not (DATE_ONLY_RE.match(name) or "summary" in name):
            misnamed.append(rel)
        elif top == "weekly" and not ISO_WEEK_RE.match(name):
            misnamed.append(rel)
        elif top == "decisions" and not DATE_PREFIX_RE.match(name):
            misnamed.append(rel)

    print(f"## Vault lint — {vault}")
    print()
    _section("Broken wikilinks", [
        f"{f}:{ln} → [[{target}]]" for f, target, ln in broken_links
    ])
    _section("Orphans (excluding daily/weekly/_to-delete)", [str(p) for p in orphans])
    _section(
        f"Stale _to-delete/ (>{args.sla_days}d)",
        [f"{p} ({age}d old)" for p, age in stale_to_delete],
    )
    _section("Misnamed (violates dir naming convention)", [str(p) for p in misnamed])

    total = len(broken_links) + len(orphans) + len(stale_to_delete) + len(misnamed)
    print(f"\nTotal findings: {total}")
    return 0 if total == 0 else 0  # always exit 0; lint is informational


def _section(title: str, items: list[str]) -> None:
    if not items:
        print(f"### {title}\n  (clean)\n")
        return
    print(f"### {title} ({len(items)})")
    for item in items:
        print(f"  - {item}")
    print()


if __name__ == "__main__":
    sys.exit(main())
