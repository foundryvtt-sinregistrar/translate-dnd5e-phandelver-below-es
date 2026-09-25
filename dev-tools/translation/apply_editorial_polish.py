"""Final explicit terminology pass; never rewrites UUIDs, formulas or HTML paths.

Run after the other apply tools. Legacy decisions retain their original baseline;
this pass records subsequent edits while preserving their review provenance.
"""
import re
from hashlib import sha256
from text_schema import ROOT, SOURCE, TECH, fields, get, put, load, save, technical, numbers
from check_reviewed import Attributes

DIRECTORY = ROOT / 'dev-tools/translation'
DECISIONS = load(DIRECTORY / 'editorial-polish.json')
ATTRIBUTES = load(DIRECTORY / 'html-attribute-labels.json')
PROTECTED = re.compile('(' + TECH.pattern + r'|<[^>]*>)')


def polish(text):
    text = text.replace('([[ and ]])', '([[ y ]])')
    text = text.replace('Activar la escena de la Mina Hardyhammer</h3><p>Cuando lleguen los jugadores, activa la escena @UUID[Scene.pbsoMap8p8000000]',
                        'Activar la escena del Campo de los Lamentos</h3><p>Cuando lleguen los jugadores, activa la escena @UUID[Scene.pbsoMap8p8000000]')
    parts = PROTECTED.split(text)
    for i in range(0, len(parts), 2):
        for old, new in DECISIONS:
            parts[i] = re.sub(r'(?<!\w)' + re.escape(old) + r'(?!\w)', lambda _: new, parts[i])
    for i in range(1, len(parts), 2):
        if not parts[i].startswith('<'):
            continue
        for tag, key, en, es in ATTRIBUTES:
            if re.match(r'<' + tag + r'\b', parts[i]):
                parts[i] = parts[i].replace(f'{key}="{en}"', f'{key}="{es}"')
    return ''.join(parts)


def main():
    evidence_path = DIRECTORY / 'reviewed-fields.json'
    evidence = {r['field']: r for r in load(evidence_path)}
    counts = {}
    staged = []
    for source_path in sorted(SOURCE.glob('*.en.json')):
        source = load(source_path)
        path = ROOT / f'compendium/{source["collection"]}.json'
        payload = load(path)
        changed = 0
        for doc in source['documents']:
            patch = payload['entries'][doc['_id']]
            for field, en in fields(doc, source['documentType']):
                address = '.'.join((source['collection'], doc['_id'], *field))
                target = field
                es = get(patch, target)
                if es is None and source['documentType'] == 'RollTable' and field[0] == 'results':
                    row = next(r for r in doc['results'] if r['_id'] == field[1])
                    target = ('results', '-'.join(map(str, row['range'])), *field[2:])
                    es = get(patch, target)
                assert isinstance(es, str), address
                result = polish(es)
                if 'pbsoT8vaulthoard' in field and field[-1] == 'description':
                    result = result.replace('510 pp', '510 ppt') if '510 ppt' not in result else result
                # Grammar changes specific to the three reviewed tunnel pages.
                if 'Actor.8pX2JhWUpTNNRBVx]{barbotadores}' in result:
                    result = result.replace('de las @UUID[Actor.8pX2JhWUpTNNRBVx]', 'de los @UUID[Actor.8pX2JhWUpTNNRBVx]')
                    result = result.replace('con las barbotadores', 'con los barbotadores').replace('derrotarlas a todas', 'derrotarlos a todos')
                    result = result.replace('las supervivientes se fusionan en una única', 'los supervivientes se fusionan en un único')
                    result = result.replace('La amasijo de carne', 'El amasijo de carne')
                if doc['_id'] in {'pbsoSpecialty000', 'pbsoSpecialtySol'} and field == ('description',):
                    result = result.replace('1d8', 'un d8')
                if result == es:
                    continue
                assert technical(en) == technical(result), (address, 'technical')
                assert numbers(en) == numbers(result), (address, 'numbers')
                assert Attributes(en).values == Attributes(result).values, (address, 'HTML attributes')
                previous = evidence.get(address)
                if previous:
                    assert previous['translationSha256'] == sha256(es.encode()).hexdigest(), address
                put(patch, target, result)
                evidence[address] = {**(previous or {'field': address, 'review': 'editorial-consistency'}),
                                     'sourceSha256': sha256(en.encode()).hexdigest(),
                                     'translationSha256': sha256(result.encode()).hexdigest(),
                                     'polish': 'editorial-polish.json'}
                changed += 1
        if changed:
            staged.append((path, payload))
        counts[source['collection']] = changed
    for path, value in staged:
        save(path, value)
    save(evidence_path, list(evidence.values()))
    # Keep manually authored dictionaries/prose consistent when reapplied later.
    # Baseline indices, legacy corrections and evidence are deliberately excluded.
    def walk(value):
        if isinstance(value, str): return polish(value)
        if isinstance(value, list): return [walk(v) for v in value]
        if isinstance(value, dict): return {k: walk(v) for k, v in value.items()}
        return value
    sources = set()
    for pattern in ['*-texts*.json', '*-names.json', '*-prefix*.json', 'adventure-labels.json',
                    'adventure-captions.json', 'adventure-changelog-214.json', 'actor-fields.json']:
        sources.update(DIRECTORY.glob(pattern))
    for path in sorted(sources):
        before = load(path)
        after = walk(before)
        if before != after: save(path, after)
    print(counts)


if __name__ == '__main__':
    main()
