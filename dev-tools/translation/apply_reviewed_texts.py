"""Publish manually reviewed item fields and exact-source copies, with hashes."""
from collections import Counter, defaultdict
from hashlib import sha256
from text_schema import ROOT, SOURCE, fields, get, put, load, save, normalize, adapt
from configure_mappings import configure


def leaves(obj, path=()):
    for key,value in obj.items():
        if isinstance(value,dict): yield from leaves(value,path+(key,))
        else: yield path+(key,),value


def main():
    source=load(SOURCE/'dnd-phandelver-below.pbso-items.en.json')
    originals={doc['_id']:dict(fields(doc,'Item')) for doc in source['documents']}
    reviewed={}
    for path in sorted((ROOT/'dev-tools/translation').glob('item-texts*.json')):
        for doc,patch in load(path).items():
            if doc in reviewed:raise ValueError(f'Duplicate reviewed item: {doc}')
            reviewed[doc]=patch
    memory=defaultdict(set)
    for doc,patch in reviewed.items():
        for path,es in leaves(patch):
            en=originals[doc][path]
            if adapt(en,es) is None:raise ValueError(f'Technical/numeric mismatch: {doc}.{path}')
            memory[(path[-1],normalize(en))].add(es)
    # This requirement was missed by the earlier root-item-only coverage audit.
    memory[('requirements','Acolyte')].add('Acólito')
    evidence_path=ROOT/'dev-tools/translation/reviewed-fields.json'
    evidence={x['field']:x for x in load(evidence_path)}
    count=Counter()
    for source_path in sorted(SOURCE.glob('*.en.json')):
        data=load(source_path);target=ROOT/f'compendium/{data["collection"]}.json';payload=load(target)
        for doc in data['documents']:
            patch=payload['entries'].setdefault(doc['_id'],{})
            for path,en in fields(doc,data['documentType']):
                candidates={adapt(en,es) for es in memory.get((path[-1],normalize(en)),set())}-{None}
                if len(candidates)!=1:continue
                value=candidates.pop()
                current=get(patch,path)
                address='.'.join((data['collection'],doc['_id'],*path))
                if current is not None and current!=value and address not in evidence:
                    continue  # Do not silently replace an earlier editorial decision.
                if current==value:continue
                put(patch,path,value);count[data['collection']]+=1
                evidence[address]={'field':address,'sourceSha256':sha256(en.encode()).hexdigest(),
                    'translationSha256':sha256(value.encode()).hexdigest(),'review':'item-texts-exact-source'}
        if data['documentType']=='Item':
            payload['mapping'].update({'requirements':'system.requirements','descriptionChat':'system.description.chat',
                'unidentifiedName':'system.unidentified.name','unidentifiedDescription':'system.unidentified.description',
                'activities':{'path':'system.activities','converter':'phandelverActivities'},
                'effects':{'path':'effects','converter':'phandelverEffects'}})
        if data['documentType']=='Actor':
            payload['mapping']['items']={'path':'items','converter':'phandelverItems'}
            payload['mapping']['effects']={'path':'effects','converter':'phandelverEffects'}
        if count[data['collection']] or data['documentType'] in ['Item','Actor']:save(target,payload)
    configure()
    save(evidence_path,list(evidence.values()));print(dict(count))


if __name__=='__main__':main()
