"""Validate full original Phandelver documents exported from Foundry 14.368."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / 'dev-tools/export/_data/source-current'
PACKS = {'pbso-player-tables': 'RollTable', 'pbso-player-options': 'Item',
         'pbso-items': 'Item', 'pbso-bestiary': 'Actor', 'pbso-adventures': 'Adventure'}
EMBEDDED = ('actors', 'items', 'journal', 'pages', 'scenes', 'tables', 'results',
            'macros', 'folders', 'effects', 'tokens', 'notes', 'playlists', 'cards',
            'regions', 'behaviors')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check_markers(value, path):
    if isinstance(value, dict):
        flags = value.get('flags') or {}
        require(not (isinstance(flags, dict) and flags.get('babele')) and
                not any(value.get(key) for key in ('translated', 'hasTranslation', 'originalName')),
                f'Translation marker: {path}')
        for key, child in value.items():
            check_markers(child, f'{path}.{key}')
    elif isinstance(value, list):
        for index, child in enumerate(value):
            check_markers(child, f'{path}[{index}]')


def check_ids(documents, path):
    require(isinstance(documents, list), f'Expected document list: {path}')
    require(all(isinstance(d, dict) for d in documents), f'Invalid documents: {path}')
    ids = [d.get('_id') for d in documents]
    require(all(isinstance(i, str) and i for i in ids), f'Missing IDs: {path}')
    require(len(ids) == len(set(ids)), f'Duplicate IDs: {path}')
    for doc in documents:
        for key in EMBEDDED:
            if isinstance(doc.get(key), list):
                check_ids(doc[key], f"{path}.{doc['_id']}.{key}")


def summarize(documents):
    counts = dict.fromkeys(('documents', 'pages', 'activities', 'effects', 'advancement',
                           'items', 'results', 'actors', 'journal', 'scenes', 'tables',
                           'macros', 'playlists', 'cards', 'embeddedFolders'), 0)
    counts['documents'] = len(documents)
    def visit(doc):
        for key in ('pages', 'effects', 'items', 'results'):
            counts[key] += len(doc.get(key) or [])
        for key in ('activities', 'advancement'):
            counts[key] += len((doc.get('system') or {}).get(key) or [])
        for item in doc.get('items', []):
            visit(item)
        for key in ('actors', 'journal', 'scenes', 'tables', 'macros', 'playlists', 'cards', 'folders'):
            children = doc.get(key)
            children = children if isinstance(children, list) else []
            counts['embeddedFolders' if key == 'folders' else key] += len(children)
            for child in children:
                visit(child)
    for doc in documents:
        visit(doc)
    return counts


def validate(directory):
    manifest = json.loads((directory / 'inventory.json').read_text(encoding='utf-8'))
    require(manifest.get('schemaVersion') == 2, 'Unsupported inventory schema')
    require(manifest.get('foundry') == '14.368', 'Expected Foundry 14.368')
    require(manifest.get('system') == {'id': 'dnd5e', 'version': '6.0.3'}, 'Expected dnd5e 6.0.3')
    require(manifest.get('source', {}).get('id') == 'dnd-phandelver-below', 'Wrong source module')
    require(manifest.get('translationActive') is False, 'Translation must be inactive')
    packs = manifest.get('packs', [])
    expected = {f'dnd-phandelver-below.{p}' for p in PACKS}
    require(len(packs) == 5 and {p['collection'] for p in packs} == expected, 'Expected exactly five packs')
    for pack in packs:
        filename = pack['collection'] + '.en.json'
        require(pack['filename'] == filename, 'Unexpected filename')
        raw = (directory / filename).read_bytes()
        require(hashlib.sha256(raw).hexdigest() == pack['sha256'], f'Hash mismatch: {filename}')
        payload = json.loads(raw)
        require(payload.get('schemaVersion') == 1, f'Unsupported payload: {filename}')
        require(payload['collection'] == pack['collection'], f'Collection mismatch: {filename}')
        require(payload['sourceVersion'] == manifest['source']['version'], f'Source version mismatch: {filename}')
        kind = PACKS[pack['collection'].split('.')[-1]]
        require(payload['documentType'] == pack['documentType'] == kind, f'Type mismatch: {filename}')
        check_markers(payload, filename)
        check_ids(payload['documents'], filename)
        check_ids(payload['folders'], filename + '.folders')
        require(len(payload['folders']) == pack['folders'], f'Folder count mismatch: {filename}')
        for key, count in summarize(payload['documents']).items():
            require(pack[key] == count, f'Count mismatch: {filename}.{key}')
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', nargs='?', type=Path)
    args = parser.parse_args()
    directory = args.directory
    if directory is None:
        candidates = sorted(BASE.glob('*/inventory.json'))
        if not candidates:
            parser.error('No current export. Run export-source.js in Foundry first.')
        directory = candidates[-1].parent
    try:
        manifest = validate(directory)
    except (ValueError, KeyError, TypeError, OSError) as error:
        print(f'FAILED: {error}')
        return 1
    print(f"OK: {manifest['foundry']} / dnd5e {manifest['system']['version']}; {directory}")
    for pack in manifest['packs']:
        print(f"{pack['collection']}: {pack['documents']} documents; {pack['pages']} pages; SHA-256 OK")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
