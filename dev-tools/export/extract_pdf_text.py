#!/usr/bin/env python3
"""Extract private, page-addressable text from the Spanish reference PDF."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LOCAL_PACKAGES = ROOT / "dev-tools" / ".python"
sys.path.insert(0, str(LOCAL_PACKAGES))

from pypdf import PdfReader  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "pdf",
        nargs="?",
        default="dev-tools/export/_data/pdf/Phandelver y Más Allá - El Obelisco Despedazado.pdf",
    )
    parser.add_argument(
        "--output",
        default="dev-tools/export/_data/pdf/extracted-pages.json",
    )
    args = parser.parse_args()

    pdf_path = (ROOT / args.pdf).resolve()
    output_path = (ROOT / args.output).resolve()
    reader = PdfReader(pdf_path)
    pages = []
    total = len(reader.pages)
    for number, page in enumerate(reader.pages, start=1):
        pages.append({
            "pdfPage": number,
            "text": page.extract_text() or "",
        })
        if number % 10 == 0 or number == total:
            print(f"Extracted {number}/{total} pages", flush=True)
    payload = {
        "source": pdf_path.name,
        "pageCount": len(pages),
        "metadata": {str(key): str(value) for key, value in (reader.metadata or {}).items()},
        "pages": pages,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Extracted {len(pages)} pages to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
