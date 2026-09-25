"""Apply explicit editorial decisions to hash-pinned legacy Adventure pages."""
from hashlib import sha256
from text_schema import ROOT, SOURCE, load, save, fields, get, put, technical, numbers
from check_reviewed import Attributes


def main():
    directory = ROOT / 'dev-tools/translation'
    index = {r['id']: r for r in load(directory / 'legacy-source-index.json')}
    decisions = {}
    for path in sorted(directory.glob('legacy-corrections-*.json')):
        for key, replacements in load(path).items():
            if key in decisions:
                raise ValueError(f'Duplicate review: {key}')
            decisions[key] = replacements
    source = load(SOURCE / 'dnd-phandelver-below.pbso-adventures.en.json')
    doc = source['documents'][0]
    originals = dict(fields(doc, 'Adventure'))
    target = ROOT / f'compendium/{source["collection"]}.json'
    payload = load(target)
    patch = payload['entries'][doc['_id']]
    evidence_path = directory / 'reviewed-fields.json'
    evidence = {r['field']: r for r in load(evidence_path)}
    changed = 0
    for key, replacements in decisions.items():
        row = index[key]
        field = tuple(row['field'])
        en = originals[field]
        es = get(patch, field)
        address = '.'.join((source['collection'], doc['_id'], *field))
        assert sha256(en.encode()).hexdigest() == row['sourceSha256'], key
        if evidence.get(address, {}).get('review') == 'legacy-editorial':
            assert sha256(es.encode()).hexdigest() == evidence[address]['translationSha256'], key
            continue
        assert sha256(es.encode()).hexdigest() == row['translationSha256'], key
        before = es
        for old, new in replacements:
            assert old in es, (key, old)
            es = es.replace(old, new)
        assert technical(en) == technical(es), (key, 'technical tokens')
        assert numbers(en) == numbers(es), (key, 'numbers')
        assert Attributes(en).values == Attributes(es).values, (key, 'HTML attributes')
        put(patch, field, es)
        changed += before != es
        evidence[address] = {'field': address, 'sourceSha256': sha256(en.encode()).hexdigest(),
                             'translationSha256': sha256(es.encode()).hexdigest(), 'review': 'legacy-editorial'}
    save(target, payload)
    save(evidence_path, list(evidence.values()))
    print(f'{len(decisions)}/{len(index)} legacy pages reviewed; {changed} changed')


if __name__ == '__main__':
    main()
