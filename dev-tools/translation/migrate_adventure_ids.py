"""Migrate existing Adventure text keys after checking the historical EN export.

No translation generation. Reject changed English pages or unexpected old keys.
"""
import copy
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'dev-tools/export'))
from validate_current_export import BASE, validate


def keyed(documents):
    used = set()
    result = {}
    for doc in documents:
        key = next((k for k in (doc['name'], doc['_id']) if k not in used), None)
        if key is None:
            raise ValueError('Cannot reconstruct historical key')
        used.add(key)
        result[key] = doc
    return result


def main():
    directory = sorted(BASE.glob('*/inventory.json'))[-1].parent
    validate(directory)
    filename = 'dnd-phandelver-below.pbso-adventures.json'
    def load(path):
        return json.loads(path.read_text(encoding='utf-8'))
    source = load(directory / filename.replace('.json', '.en.json'))['documents'][0]
    target = ROOT / 'compendium' / filename
    payload = load(target)
    if payload.get('mapping', {}).get('folders', {}).get('converter') == 'phandelverFoldersById':
        print('Already migrated; no changes.')
        return
    historical = load(ROOT / 'dev-tools/export/_data/source/translations' / filename)['entries'][source['_id']]
    translated = payload['entries'][source['_id']]
    journals = keyed(source['journal'])
    if set(journals) != set(historical['journals']):
        raise ValueError('Journal keys changed; manual matching required')
    for key, journal in journals.items():
        pages = keyed(journal['pages'])
        old = historical['journals'][key].get('pages', {})
        if set(pages) != set(old):
            raise ValueError(f'Page keys changed: {key}')
        for page_key, page in pages.items():
            if old[page_key].get('text', '') != (page.get('text') or {}).get('content', ''):
                raise ValueError(f'English text changed: {key}/{page_key}')
    migrated = {}
    for key, patch in translated['journals'].items():
        journal = journals[key]
        result = copy.deepcopy(patch)
        if set(result) - {'name', 'pages'}:
            raise ValueError(f'Unsupported journal fields: {key}')
        if 'pages' in result:
            pages = keyed(journal['pages'])
            for page_key, text in result['pages'].items():
                if set(text) - {'name', 'text', 'caption'}:
                    raise ValueError(f'Unsupported page fields: {key}/{page_key}')
            result['pages'] = {pages[k]['_id']: v for k, v in result['pages'].items()}
        migrated[journal['_id']] = result
    folders = translated['folders']
    if set(folders) - {f['name'] for f in source['folders']}:
        raise ValueError('Unknown folder names')
    translated['folders'] = {f['_id']: folders[f['name']] for f in source['folders'] if f['name'] in folders}
    translated['journals'] = migrated
    payload['mapping'].update({
        'folders': {'path': 'folders', 'converter': 'phandelverFoldersById'},
        'journals': {'path': 'journal', 'converter': 'phandelverJournalsById'},
    })
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(f"Migrated {len(migrated)} journals, {sum(len(j.get('pages', {})) for j in migrated.values())} pages, {len(translated['folders'])} folders; text preserved.")


if __name__ == '__main__':
    main()
