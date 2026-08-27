#!/usr/bin/env python3
"""Run resumable Spanish OCR over the private reference PDF."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PDF = ROOT / "dev-tools/export/_data/pdf/Phandelver y Más Allá - El Obelisco Despedazado.pdf"
DEFAULT_OUTPUT = ROOT / "dev-tools/export/_data/pdf/ocr-pages.json"
DEFAULT_TESSDATA = ROOT / "dev-tools/.tessdata"
GHOSTSCRIPT = Path("C:/Program Files/gs/gs10.06.0/bin/gswin64c.exe")
TESSERACT = Path("C:/Program Files/Tesseract-OCR/tesseract.exe")


def load_output(path: Path) -> dict:
    if not path.exists():
        return {"source": DEFAULT_PDF.name, "language": "spa", "pages": {}}
    return json.loads(path.read_text(encoding="utf-8"))


def save_output(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def render_page(pdf: Path, page: int, image: Path, dpi: int) -> None:
    subprocess.run(
        [
            str(GHOSTSCRIPT),
            "-dSAFER",
            "-dBATCH",
            "-dNOPAUSE",
            "-sDEVICE=pnggray",
            f"-r{dpi}",
            f"-dFirstPage={page}",
            f"-dLastPage={page}",
            f"-sOutputFile={image}",
            str(pdf),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
    )


def recognize_page(image: Path, tessdata: Path) -> str:
    result = subprocess.run(
        [
            str(TESSERACT),
            str(image),
            "stdout",
            "--tessdata-dir",
            str(tessdata),
            "-l",
            "spa",
            "--psm",
            "3",
        ],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return result.stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", type=Path, default=DEFAULT_PDF)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--start", type=int, default=1)
    parser.add_argument("--end", type=int, default=204)
    parser.add_argument("--dpi", type=int, default=180)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    if not GHOSTSCRIPT.exists():
        raise SystemExit(f"Ghostscript not found: {GHOSTSCRIPT}")
    if not TESSERACT.exists():
        raise SystemExit(f"Tesseract not found: {TESSERACT}")
    if not (DEFAULT_TESSDATA / "spa.traineddata").exists():
        raise SystemExit(f"Spanish OCR model not found: {DEFAULT_TESSDATA}")

    pdf = args.pdf.resolve()
    output = args.output.resolve()
    payload = load_output(output)
    payload["source"] = pdf.name
    payload["language"] = "spa"
    payload["dpi"] = args.dpi
    pages = payload.setdefault("pages", {})
    temp_dir = ROOT / "dev-tools/export/_data/pdf/ocr-temp"
    temp_dir.mkdir(parents=True, exist_ok=True)

    for page in range(args.start, args.end + 1):
        key = str(page)
        if key in pages and not args.force:
            print(f"Skipped {page}/{args.end} (already extracted)", flush=True)
            continue

        image = temp_dir / f"page-{page:03d}.png"
        try:
            render_page(pdf, page, image, args.dpi)
            pages[key] = recognize_page(image, DEFAULT_TESSDATA)
            save_output(output, payload)
            print(f"OCR {page}/{args.end}: {len(pages[key])} characters", flush=True)
        finally:
            image.unlink(missing_ok=True)

    print(f"OCR output: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
