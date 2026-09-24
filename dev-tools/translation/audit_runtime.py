"""Compare saved Babele output with originals; fail on non-text changes."""
import json
from collections import Counter
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'dev-tools/export/_data'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def differences(original, translated, path=''):
    if type(original) is not type(translated):
        yield path, original, translated
    elif isinstance(original, dict):
        for key in original.keys() | translated.keys():
            if key not in original or key not in translated:
                yield path+'/'+key, original.get(key), translated.get(key)
            else:
                yield from differences(original[key], translated[key], path+'/'+key)
    elif isinstance(original, list):
        if len(original) != len(translated):
            yield path+'/length', len(original), len(translated)
        for index, (a, b) in enumerate(zip(original, translated)):
            yield from differences(a, b, path+'/'+str(index))
    elif original != translated:
        yield path, original, translated


def is_text(path, original, translated):
    if not isinstance(original, str) or not isinstance(translated, str):
        return False
    patterns = [
        r'/(name|description|caption)',
        r'/folders/\d+/name',
        r'/journal/\d+/name',
        r'/journal/\d+/pages/\d+/(name|text/content|image/caption)',
        r'/results/\d+/(name|description)',
        r'/(actors/\d+/)?items/\d+/(name|system/description/value)',
        r'/actors/\d+/(name|prototypeToken/name|system/details/biography/value)',
    ]
    return any(re.fullmatch(pattern, path) for pattern in patterns)


def main():
    runtime = read(DATA/'runtime-validation.json')
    if runtime['errors']:
        raise SystemExit('Runtime validation contains errors')
    source = ROOT/runtime['source']
    manifest = read(source/'inventory.json')
    summary = Counter()
    protected_changes = []
    for pack in manifest['packs']:
        original = read(source/pack['filename'])['documents']
        name = pack['collection'].split('.')[-1]
        translated = read(DATA/f'{name}.runtime.json')['documents']
        if [d['_id'] for d in original] != [d['_id'] for d in translated]:
            raise SystemExit(f'Document identity/order differs: {name}')
        for a, b in zip(original, translated):
            for path, old, new in differences(a, b):
                if path.endswith('/flags/babele') or re.fullmatch(
                    r'(?:/(?:actors|items|results)/\d+)*/(?:translated|hasTranslation|originalName)', path
                ):
                    summary['babele_metadata'] += 1
                elif is_text(path, old, new):
                    summary['text_fields'] += 1
                else:
                    protected_changes.append({'pack':name, 'id':a['_id'], 'path':path})
    report = {'runtime_date':runtime['date'], 'summary':dict(summary),
              'protected_changes':protected_changes,
              'scope':'Includes fallback translations supplied by other active modules.'}
    (DATA/'runtime-diff.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({**report, 'protected_changes':len(protected_changes)},indent=2))
    if protected_changes:
        raise SystemExit('Unexpected changes outside approved text paths')


if __name__ == '__main__':
    main()
