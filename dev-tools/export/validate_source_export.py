#!/usr/bin/env python3
"""Validate a private Phandelver & Below source export before translation."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


PACK_IDS = (
    "dnd-phandelver-below.pbso-player-tables",
    "dnd-phandelver-below.pbso-player-options",
    "dnd-phandelver-below.pbso-items",
    "dnd-phandelver-below.pbso-bestiary",
    "dnd-phandelver-below.pbso-adventures",
)


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise ValueError(f"Missing file: {path}") from error
    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid JSON in {path}: {error}") from error


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "source",
        nargs="?",
        default="dev-tools/export/_data/source",
        help="Extracted private source-export directory",
    )
    args = parser.parse_args()

    source = Path(args.source).resolve()
    inventory = load_json(source / "inventory.json")
    inventory_packs = {pack["id"]: pack for pack in inventory.get("packs", [])}
    errors: list[str] = []

    print(
        "Versions:",
        f"Foundry {inventory.get('foundryVersion', '?')},",
        f"dnd5e {inventory.get('system', {}).get('version', '?')},",
        f"source module {inventory.get('sourceModule', {}).get('version', '?')}",
    )

    for pack_id in PACK_IDS:
        pack = inventory_packs.get(pack_id)
        if not pack:
            errors.append(f"Inventory is missing pack {pack_id}")
            continue

        payload = load_json(source / "translations" / f"{pack_id}.json")
        entries = payload.get("entries")
        if not isinstance(entries, dict):
            errors.append(f"{pack_id}: entries must be an object")
            continue

        documents = pack.get("documents", [])
        expected_ids = {document["id"] for document in documents}
        actual_ids = set(entries)
        missing = sorted(expected_ids - actual_ids)
        unexpected = sorted(actual_ids - expected_ids)
        duplicate_names = {
            name: count
            for name, count in Counter(document["name"] for document in documents).items()
            if count > 1
        }

        print(
            f"{pack_id}: inventory={len(expected_ids)}, entries={len(actual_ids)}, "
            f"duplicate names={sum(count - 1 for count in duplicate_names.values())}"
        )
        for name, count in sorted(duplicate_names.items()):
            print(f"  duplicate name ({count}): {name}")

        if missing:
            preview = ", ".join(missing[:10])
            suffix = f" (+{len(missing) - 10} more)" if len(missing) > 10 else ""
            errors.append(f"{pack_id}: missing {len(missing)} IDs: {preview}{suffix}")
        if unexpected:
            preview = ", ".join(unexpected[:10])
            suffix = f" (+{len(unexpected) - 10} more)" if len(unexpected) > 10 else ""
            errors.append(f"{pack_id}: unexpected {len(unexpected)} keys/IDs: {preview}{suffix}")

    if errors:
        print("\nFAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("\nOK: all exported translation entries match the Foundry document IDs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
