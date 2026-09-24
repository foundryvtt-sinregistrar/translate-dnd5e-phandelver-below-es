"""Extract local bilingual PDF references; OCR pages with damaged text layers."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv
from datetime import datetime, timezone
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import threading
import unicodedata

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'dev-tools/.python'))
import pymupdf

DATA = ROOT / 'dev-tools/export/_data'
OUT = DATA / 'references'
TESSERACT = Path('C:/Program Files/Tesseract-OCR/tesseract.exe')
SOURCES = {'en': 'Phandelver and Below The Shattered Obelisk pdf.pdf',
           'es': 'Phandelver y Más Allá - El Obelisco Despedazado.pdf'}
PDF_LOCK = threading.Lock()


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def write_json(path, value):
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temp.replace(path)


def damaged_characters(text):
    return sum(c == '\ufffd' or (c.isalpha() and 'LATIN' not in unicodedata.name(c, ''))
               or unicodedata.category(c) == 'Co' for c in text)


def process_page(task):
    language, filename, number, signature, tessdata, force_ocr = task
    folder = OUT / language / 'pages'
    base = folder / f'{number:04d}'
    meta = base.with_suffix('.json')
    if meta.exists():
        record = json.loads(meta.read_text(encoding='utf-8'))
        if record.get('signature') == signature and base.with_suffix('.txt').exists():
            return record
    with PDF_LOCK, pymupdf.open(filename) as pdf:
        page = pdf[number - 1]
        # Preserve the PDF's text flow: geometric line sorting interleaves columns.
        native = page.get_text(sort=False)
        blocks = page.get_text('blocks', sort=True)
        base.with_suffix('.native.txt').write_text(native, encoding='utf-8')
        write_json(base.with_suffix('.blocks.json'), blocks)
        damaged = damaged_characters(native)
        ocr = force_ocr or damaged > 3 or len(native.strip()) < 80
        if ocr:
            scratch = DATA / 'references/.scratch'
            scratch.mkdir(parents=True, exist_ok=True)
            png = scratch / f'{language}-{number:04d}.png'
            page.get_pixmap(dpi=300, alpha=False).save(png)
    record = {'pdf_page': number, 'signature': signature, 'method': 'native',
              'native_characters': len(native.strip()), 'damaged_native_characters': damaged}
    text = native
    if ocr:
        try:
            result = subprocess.run([str(TESSERACT), str(png), str(base), '--tessdata-dir',
                str(tessdata), '-l', 'spa' if language == 'es' else 'eng', '--psm', '3',
                '-c', 'tessedit_create_txt=1', '-c', 'tessedit_create_tsv=1'],
                capture_output=True, timeout=240, env={**os.environ, 'OMP_THREAD_LIMIT': '1'})
            if result.returncode:
                raise RuntimeError(result.stderr.decode('utf-8', errors='replace'))
            text = base.with_suffix('.txt').read_text(encoding='utf-8')
            tsv = base.with_suffix('.tsv').read_text(encoding='utf-8')
            rows = csv.DictReader(io.StringIO(tsv), delimiter='\t', quoting=csv.QUOTE_NONE)
            confidence = [float(r['conf']) for r in rows if r['text'].strip() and float(r['conf']) >= 0]
            with gzip.open(base.with_suffix('.tsv.gz'), 'wt', encoding='utf-8') as stream:
                stream.write(tsv)
            record.update(method='tesseract-ocr', mean_confidence=round(sum(confidence)/len(confidence), 2) if confidence else None,
                          low_confidence_words=sum(c < 60 for c in confidence),
                          warning=result.stderr.decode('utf-8', errors='replace').strip())
        finally:
            png.unlink(missing_ok=True)
            base.with_suffix('.tsv').unlink(missing_ok=True)
    record.update(characters=len(text.strip()), words=len(text.split()),
                  needs_review=len(text.split()) < 20 or damaged_characters(text) > 3
                  or (record['method'] == 'tesseract-ocr' and (record['mean_confidence'] or 0) < 75))
    base.with_suffix('.txt').write_text(text, encoding='utf-8')
    write_json(meta, record)
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tessdata', type=Path, default=ROOT / 'dev-tools/.tessdata')
    parser.add_argument('--workers', type=int, default=4)
    parser.add_argument('--ocr-all', nargs='*', choices=['es', 'en'], default=[])
    args = parser.parse_args()
    engine = subprocess.check_output([str(TESSERACT), '--version']).decode().splitlines()[0]
    reports = []
    for language, name in SOURCES.items():
        source = DATA / 'pdf' / name
        folder = OUT / language
        (folder / 'pages').mkdir(parents=True, exist_ok=True)
        with pymupdf.open(source) as pdf:
            count = len(pdf)
            write_json(folder / 'bookmarks.json', pdf.get_toc())
        config = {'source_sha256': digest(source), 'pymupdf': pymupdf.VersionBind,
                  'tesseract': engine, 'model_sha256': digest(args.tessdata / ('spa.traineddata' if language == 'es' else 'eng.traineddata')),
                  'script_sha256': digest(Path(__file__)), 'dpi': 300, 'psm': 3,
                  'force_ocr': language in args.ocr_all}
        signature = hashlib.sha256(json.dumps(config, sort_keys=True).encode()).hexdigest()
        report = {'source': name, 'language': language, 'page_count': count, 'config': config, 'status': 'incomplete'}
        write_json(folder / 'manifest.json', report)
        records, errors = [], []
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            tasks = {pool.submit(process_page, (language, str(source), n, signature, args.tessdata, language in args.ocr_all)): n for n in range(1, count + 1)}
            for future in as_completed(tasks):
                try:
                    records.append(future.result())
                except Exception as exc:
                    errors.append({'pdf_page': tasks[future], 'error': str(exc)})
                if (len(records) + len(errors)) % 20 == 0:
                    print(f'{language}: {len(records)}/{count}; errors={len(errors)}', flush=True)
        records.sort(key=lambda r: r['pdf_page'])
        with (folder / 'text.txt').open('w', encoding='utf-8') as full, (folder / 'pages.jsonl').open('w', encoding='utf-8') as jsonl:
            for record in records:
                n = record['pdf_page']
                text = (folder / 'pages' / f'{n:04d}.txt').read_text(encoding='utf-8')
                full.write(f'\n\n===== PDF PAGE {n:04d} =====\n\n{text}')
                jsonl.write(json.dumps({**record, 'text': text}, ensure_ascii=False) + '\n')
        report.update(completed_pages=len(records), errors=errors, status='complete' if len(records) == count and not errors else 'incomplete',
                      ocr_pages=[r['pdf_page'] for r in records if r['method'] == 'tesseract-ocr'],
                      review_pages=[r['pdf_page'] for r in records if r['needs_review']],
                      finished_utc=datetime.now(timezone.utc).isoformat())
        write_json(folder / 'manifest.json', report)
        reports.append(report)
        print(f"{language}: {report['status']}; {len(records)}/{count}; OCR={len(report['ocr_pages'])}", flush=True)
    write_json(OUT / 'manifest.json', reports)
    return int(any(r['status'] != 'complete' for r in reports))


if __name__ == '__main__':
    raise SystemExit(main())
