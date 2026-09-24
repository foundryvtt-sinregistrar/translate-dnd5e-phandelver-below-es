"""Apply the explicitly reviewed root-name dictionaries, never machine drafts."""
from collections import Counter
from hashlib import sha256
from text_schema import ROOT, SOURCE, fields, get, put, load, save


def main():
    names = {kind:load(ROOT/f'dev-tools/translation/{kind}-names.json') for kind in ['item','actor']}
    count=Counter()
    evidence=[]
    def apply(doc,patch,kind,address):
        dictionary=names[kind]
        for path,en in fields(doc,'Item' if kind=='item' else 'Actor'):
            # Root identity only: an embedded trait with the same name may mean something else.
            if path not in [('name',),('tokenName',)]: continue
            if en not in dictionary or get(patch,path) is not None: continue
            value=dictionary[en];put(patch,path,value);count[kind]+=1
            evidence.append({'field':'.'.join((*address,*path)),
                'sourceSha256':sha256(en.encode()).hexdigest(),
                'translationSha256':sha256(value.encode()).hexdigest(),
                'review':'root-name-dictionary'})

    for suffix,kind in [('items','item'),('bestiary','actor')]:
        source=load(SOURCE/f'dnd-phandelver-below.pbso-{suffix}.en.json')
        target=ROOT/f'compendium/{source["collection"]}.json';payload=load(target)
        missing={doc['name'] for doc in source['documents']}-names[kind].keys()
        if missing:raise ValueError(f'Missing reviewed names: {sorted(missing)}')
        for doc in source['documents']:
            apply(doc,payload['entries'].setdefault(doc['_id'],{}),kind,(source['collection'],doc['_id']))
        save(target,payload)
    source=load(SOURCE/'dnd-phandelver-below.pbso-adventures.en.json')
    target=ROOT/f'compendium/{source["collection"]}.json';payload=load(target)
    for adventure in source['documents']:
        root=payload['entries'][adventure['_id']]
        for group,kind,converter in [('items','item','phandelverItems'),('actors','actor','phandelverActors')]:
            payload['mapping'][group]={'path':group,'converter':converter}
            for doc in adventure[group]:
                if doc['name'] in names[kind]:
                    apply(doc,root.setdefault(group,{}).setdefault(doc['_id'],{}),kind,
                        (source['collection'],adventure['_id'],group,doc['_id']))
    save(target,payload)
    # Evidence is cumulative, so rerunning this script is idempotent.
    path=ROOT/'dev-tools/translation/reviewed-fields.json'
    previous={x['field']:x for x in load(path)} if path.exists() else {}
    previous.update({x['field']:x for x in evidence});save(path,list(previous.values()))
    print(dict(count))


if __name__=='__main__': main()
