#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kiloloop
# SPDX-License-Identifier: Apache-2.0
"""Initialize an Obsidian vault for Iantha.

Creates the standard subdirectories, copies the VAULT.md handbook from
vault-template/, and writes a starter reading-list.md if missing.

Idempotent: never overwrites existing files. Reports what was created vs
skipped.

Usage:
    python init_vault.py --vault-dir ~/Documents/MyVault [--template <path>]
"""

from __future__ import annotations

import argparse
import shutil
import sys
from datetime import datetime
from pathlib import Path

# Standard dirs Iantha writes to. Optional Karpathy-mode dirs (wiki/, raw/)
# are NOT auto-created — users opt in by creating them manually.
STANDARD_DIRS = [
    "daily",
    "weekly",
    "decisions",
    "tasks",
    "personal",
    "artifacts",
    "_to-delete",
]

READING_LIST_TEMPLATE = """# Reading List

*Updated: {today}*

## Action Required

(empty — Iantha will append items here)

## Completed

(empty)
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--vault-dir", required=True, help="Path to vault root")
    parser.add_argument(
        "--template",
        help="Path to vault-template/VAULT.md (auto-detected if omitted)",
    )
    args = parser.parse_args()

    if not args.vault_dir.strip():
        print("ERROR: --vault-dir is empty.", file=sys.stderr)
        return 1

    vault = Path(args.vault_dir).expanduser().resolve()
    if vault == Path(__file__).resolve().parent or any(
        (vault / m).exists() for m in ("CLAUDE.md", "memory")
    ):
        print(
            f"ERROR: {vault} looks like an Iantha repo, not a vault. "
            "Pass an empty/dedicated directory.",
            file=sys.stderr,
        )
        return 1
    if not vault.parent.exists():
        print(f"ERROR: Parent of {vault} doesn't exist. Create it first.", file=sys.stderr)
        return 1

    vault.mkdir(parents=True, exist_ok=True)

    created: list[str] = []
    skipped: list[str] = []

    for d in STANDARD_DIRS:
        path = vault / d
        if path.exists():
            skipped.append(f"{d}/")
        else:
            path.mkdir()
            created.append(f"{d}/")

    template_path = (
        Path(args.template).expanduser().resolve()
        if args.template
        else _find_default_template()
    )
    vault_md = vault / "VAULT.md"
    if vault_md.exists():
        skipped.append("VAULT.md")
    elif template_path and template_path.exists():
        shutil.copy(template_path, vault_md)
        created.append("VAULT.md")
    else:
        print(
            f"WARNING: vault-template/VAULT.md not found at {template_path}. "
            "Skipping VAULT.md copy.",
            file=sys.stderr,
        )

    reading_list = vault / "reading-list.md"
    if reading_list.exists():
        skipped.append("reading-list.md")
    else:
        reading_list.write_text(
            READING_LIST_TEMPLATE.format(today=datetime.now().strftime("%Y-%m-%d %H:%M"))
        )
        created.append("reading-list.md")

    print(f"Vault: {vault}")
    print(f"Created: {', '.join(created) if created else '(nothing — already initialized)'}")
    if skipped:
        print(f"Skipped (already present): {', '.join(skipped)}")
    return 0


def _find_default_template() -> Path | None:
    here = Path(__file__).resolve()
    for parent in here.parents:
        candidate = parent / "vault-template" / "VAULT.md"
        if candidate.exists():
            return candidate
    return None


if __name__ == "__main__":
    sys.exit(main())
