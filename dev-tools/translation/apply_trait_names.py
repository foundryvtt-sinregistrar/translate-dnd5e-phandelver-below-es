"""Translate reviewed names of embedded items, activities and effects."""
from collections import Counter
from hashlib import sha256
from text_schema import ROOT,SOURCE,fields,get,put,load,save

def main():
    names=load(ROOT/'dev-tools/translation/trait-names.json')
    names.update(load(ROOT/'dev-tools/translation/item-names.json'))
    path=ROOT/'dev-tools/translation/reviewed-fields.json';evidence={r['field']:r for r in load(path)}
    count=Counter();missing=set()
    for suffix in ['bestiary','adventures']:
        source=load(SOURCE/f'dnd-phandelver-below.pbso-{suffix}.en.json')
        target=ROOT/f'compendium/{source["collection"]}.json';payload=load(target)
        for doc in source['documents']:
            patch=payload['entries'][doc['_id']]
            for field,en in fields(doc,source['documentType']):
                if field[-1]!='name' or not any(part in field for part in ['items','effects','activities']):continue
                if get(patch,field) is not None:continue
                if en not in names:missing.add(en);continue
                es=names[en];put(patch,field,es);address='.'.join((source['collection'],doc['_id'],*field))
                evidence[address]={'field':address,'sourceSha256':sha256(en.encode()).hexdigest(),
                    'translationSha256':sha256(es.encode()).hexdigest(),'review':'embedded-name-glossary'}
                count[suffix]+=1
        save(target,payload)
    save(path,list(evidence.values()));print(dict(count));print('Unreviewed variants:',sorted(missing))

if __name__=='__main__':main()
