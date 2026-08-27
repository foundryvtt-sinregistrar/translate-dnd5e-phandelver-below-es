#!/usr/bin/env python3
"""Build a private page-level translation worklist for the Adventure pack."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "dev-tools/export/_data/source/translations/dnd-phandelver-below.pbso-adventures.json"
OUTPUT = ROOT / "dev-tools/export/_data/adventure-worklist.csv"


def main() -> int:
    payload = json.loads(SOURCE.read_text(encoding="utf-8"))
    adventure_id, adventure = next(iter(payload["entries"].items()))
    rows = []

    for journal_key, journal in adventure.get("journals", {}).items():
        for page_key, page in journal.get("pages", {}).items():
            text = page.get("text", "")
            rows.append({
                "adventure_id": adventure_id,
                "journal_key": journal_key,
                "journal_name": journal.get("name", journal_key),
                "page_key": page_key,
                "page_name": page.get("name", page_key),
                "source_characters": len(text),
                "pdf_page_start": "",
                "pdf_page_end": "",
                "status": "pending",
                "notes": "",
            })

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Created {OUTPUT} with {len(rows)} journal pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
