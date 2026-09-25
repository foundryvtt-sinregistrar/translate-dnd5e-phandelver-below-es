"""Apply reviewed short actor fields to root and Adventure actors by ID."""
from collections import Counter
from hashlib import sha256
from text_schema import ROOT, SOURCE, fields, get, put, load, save, adapt
from configure_mappings import configure

def main():
    glossary=load(ROOT/'dev-tools/translation/actor-fields.json')
    path=ROOT/'dev-tools/translation/reviewed-fields.json';evidence={r['field']:r for r in load(path)}
    count=Counter();missing=set()
    for suffix in ['bestiary','adventures']:
        source=load(SOURCE/f'dnd-phandelver-below.pbso-{suffix}.en.json')
        target=ROOT/f'compendium/{source["collection"]}.json';payload=load(target)
        for doc in source['documents']:
            patch=payload['entries'][doc['_id']]
            for field,en in fields(doc,source['documentType']):
                if field[-1] not in glossary:continue
                if get(patch,field) is not None:continue
                es=glossary[field[-1]].get(en)
                if es is None:missing.add((field[-1],en));continue
                if adapt(en,es) is None:raise ValueError((field,en))
                put(patch,field,es);address='.'.join((source['collection'],doc['_id'],*field))
                evidence[address]={'field':address,'sourceSha256':sha256(en.encode()).hexdigest(),
                    'translationSha256':sha256(es.encode()).hexdigest(),'review':'actor-short-fields'}
                count[suffix]+=1
        save(target,payload)
    save(path,list(evidence.values()));configure();print(dict(count));print('Unreviewed variants:',sorted(missing))

if __name__=='__main__':main()
