"""Apply manually reviewed Adventure originals using stable source hashes."""
from hashlib import sha256
from collections import defaultdict,Counter
from text_schema import ROOT,SOURCE,load,save,fields,get,put,normalize,adapt

def main():
    source=load(SOURCE/'dnd-phandelver-below.pbso-adventures.en.json');doc=source['documents'][0]
    originals={sha256(en.encode()).hexdigest():en for _,en in fields(doc,'Adventure')}
    index=load(ROOT/'dev-tools/translation/adventure-source-index.json')
    by_id={r['id']:originals[r['sha256']] for r in index}
    reviewed={}
    for path in sorted((ROOT/'dev-tools/translation').glob('adventure-texts-*.json')):
        for key,es in load(path).items():
            if key in reviewed:raise ValueError('Duplicate review: '+key)
            reviewed[key]=es
    memory=defaultdict(set)
    for key,es in reviewed.items():
        en=by_id[key]
        if adapt(en,es) is None:raise ValueError('Technical/numeric mismatch: '+key)
        memory[normalize(en)].add(es)
    ep=ROOT/'dev-tools/translation/reviewed-fields.json';evidence={r['field']:r for r in load(ep)}
    target=ROOT/f'compendium/{source["collection"]}.json';payload=load(target);patch=payload['entries'][doc['_id']]
    count=Counter()
    for field,en in fields(doc,'Adventure'):
        address='.'.join((source['collection'],doc['_id'],*field));current=get(patch,field)
        if current is not None and evidence.get(address,{}).get('review')!='adventure-prose':continue
        candidates={adapt(en,es) for es in memory.get(normalize(en),set())}-{None}
        if len(candidates)!=1:continue
        es=candidates.pop()
        if current==es:continue
        put(patch,field,es);count[field[0]]+=1
        evidence[address]={'field':address,'sourceSha256':sha256(en.encode()).hexdigest(),
            'translationSha256':sha256(es.encode()).hexdigest(),'review':'adventure-prose'}
    save(target,payload);save(ep,list(evidence.values()))
    print(f'{len(reviewed)}/{len(index)} Adventure originals reviewed; applied: {dict(count)}')

if __name__=='__main__':main()
