"""Build a private field queue and exact-match reuse candidates, never approve prose."""
from collections import defaultdict, Counter
from hashlib import sha256
from text_schema import ROOT, DATA, SOURCE, fields, get, load, save, normalize, adapt


def main():
    memory = defaultdict(dict)
    def add(en, es, origin):
        if isinstance(es,str) and en.strip() and normalize(en) != normalize(es):
            memory[normalize(en)][es] = origin

    for path in sorted((ROOT.parent/'translate-dnd5e-dm-2024-es/dev-tools/export/data').glob('*.reference.json')):
        data = load(path)
        name = data['collection'].split('.')[-1]
        kind = 'Actor' if 'actor' in name else 'Item' if 'equipment' in name else 'RollTable' if 'table' in name else 'JournalEntry'
        for pair in data['documents']:
            translated = dict(fields(pair['translated'],kind))
            for key,en in fields(pair['original'],kind):
                add(en,translated.get(key),str(path))

    tomb = ROOT.parent/'translate-dnd5e-tomb-annihilation-es'
    reviewed = {row['field']:row for row in load(tomb/'dev-tools/export/data/reviewed-fields.json')}
    for path in sorted((tomb/'dev-tools/export/data').glob('*.en.json')):
        data = load(path)
        translated = load(tomb/'compendium'/path.name.replace('.en.json','.json'))['entries']
        for doc in data['documents']:
            for key,en in fields(doc,data['documentType']):
                es = get(translated.get(doc['_id'],{}),key)
                address = '.'.join((data['collection'],doc['_id'],*key))
                evidence = reviewed.get(address,{})
                if isinstance(es,str) and evidence.get('sourceSha256') == sha256(en.encode()).hexdigest() and evidence.get('translationSha256') == sha256(es.encode()).hexdigest():
                    add(en,es,address)

    # Existing project texts have priority when the source field is identical.
    own = {}
    for path in sorted(SOURCE.glob('*.en.json')):
        data = load(path); translation = load(ROOT/'compendium'/path.name.replace('.en.json','.json'))
        for doc in data['documents']:
            for key,en in fields(doc,data['documentType']):
                es = get(translation['entries'].get(doc['_id'],{}),key)
                if isinstance(es,str) and normalize(en) != normalize(es):
                    own.setdefault(normalize(en),{})[es] = '.'.join((data['collection'],doc['_id'],*key))
    memory.update(own)

    queue = []; totals = Counter()
    for path in sorted(SOURCE.glob('*.en.json')):
        data = load(path); translation = load(ROOT/'compendium'/path.name.replace('.en.json','.json'))
        for doc in data['documents']:
            patch = translation['entries'].get(doc['_id'],{})
            for key,en in fields(doc,data['documentType']):
                if not en.strip(): continue
                current = get(patch,key)
                if current is None and data['documentType']=='RollTable' and key[0]=='results':
                    row=next(r for r in doc['results'] if r['_id']==key[1])
                    current=get(patch,('results','-'.join(map(str,row['range'])),*key[2:]))
                if current is not None: totals['existing']+=1;continue
                candidates = {}
                for es, origin in memory.get(normalize(en),{}).items():
                    value = adapt(en,es)
                    if value is not None:candidates[value]=origin
                row = {'collection':data['collection'],'document':doc['_id'],'path':list(key),
                       'source':en,'sourceSha256':sha256(en.encode()).hexdigest(),'status':'pending'}
                if len(candidates)==1:
                    row['candidate'],row['candidateOrigin']=next(iter(candidates.items()))
                    row['status']='candidate-reuse'
                elif candidates:row['alternatives']=candidates
                queue.append(row);totals[row['status']]+=1
    save(DATA/'remaining-fields.json',queue)
    print(dict(totals))
    print(dict(Counter(row['collection'] for row in queue)))


if __name__=='__main__': main()
