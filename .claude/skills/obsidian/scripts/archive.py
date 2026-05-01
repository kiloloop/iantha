#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kiloloop
# SPDX-License-Identifier: Apache-2.0
"""Stage a vault file for deletion by moving it to _to-delete/.

Preserves subdirectory structure in the flattened name to avoid collisions:
    decisions/2026-05-01-foo.md  →  _to-delete/decisions__2026-05-01-foo.md
    research/topic/r1_foo.md     →  _to-delete/research_topic__r1_foo.md

If a file with the same staged name already exists, append a timestamp.

Usage:
    python archive.py --vault-dir ~/Documents/MyVault --source decisions/2026-05-01-foo.md
"""

from __future__ import annotations

import argparse
import shutil
import sys
import time
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--vault-dir", required=True)
    parser.add_argument(
        "--source",
        required=True,
        help="Path relative to vault root, e.g., decisions/2026-05-01-foo.md",
    )
    args = parser.parse_args()

    vault = Path(args.vault_dir).expanduser().resolve()
    src = (vault / args.source).resolve()

    if not src.exists():
        print(f"ERROR: {src} doesn't exist.", file=sys.stderr)
        return 1
    try:
        src.relative_to(vault)
    except ValueError:
        print(f"ERROR: {src} is outside the vault.", file=sys.stderr)
        return 1
    if src.is_dir():
        print(f"ERROR: {src} is a directory; archive files only.", file=sys.stderr)
        return 1

    rel = src.relative_to(vault)
    if rel.parts and rel.parts[0] == "_to-delete":
        print(f"NOTE: {rel} is already in _to-delete/. Skipping.", file=sys.stderr)
        return 0

    parent_parts = "_".join(rel.parent.parts) if rel.parts[:-1] else ""
    flat = f"{parent_parts}__{rel.name}" if parent_parts else rel.name

    dest_dir = vault / "_to-delete"
    dest_dir.mkdir(exist_ok=True)
    dest = dest_dir / flat

    if dest.exists():
        ts = time.strftime("%Y%m%d%H%M%S")
        dest = dest.with_name(f"{dest.stem}.{ts}{dest.suffix}")

    shutil.move(str(src), str(dest))
    print(f"Archived: {rel} → _to-delete/{dest.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
