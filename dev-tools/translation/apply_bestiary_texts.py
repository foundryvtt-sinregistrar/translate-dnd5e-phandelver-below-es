"""Apply indexed, manually reviewed prose; verify the entire source index first."""
from collections import Counter,defaultdict
from hashlib import sha256
from text_schema import ROOT,SOURCE,fields,get,put,load,save,normalize,adapt

def main():
    source=load(SOURCE/'dnd-phandelver-below.pbso-bestiary.en.json')
    values=sorted({en for d in source['documents'] for p,en in fields(d,'Actor')
                   if p[-1] in ['description','biography']},key=lambda x:(len(x),x))
    index=[{'id':f'{i:04d}','sha256':sha256(en.encode()).hexdigest()} for i,en in enumerate(values,1)]
    if index!=load(ROOT/'dev-tools/translation/bestiary-source-index.json'):
        raise ValueError('Source index changed; review the new baseline before applying prose')
    originals={row['id']:value for row,value in zip(index,values)}
    reviewed={}
    for path in sorted((ROOT/'dev-tools/translation').glob('bestiary-texts-*.json')):
        for key,es in load(path).items():
            if key in reviewed:raise ValueError(f'Duplicate review ID: {key}')
            reviewed[key]=es
    memory=defaultdict(set)
    for key,es in reviewed.items():
        en=originals[key]
        if adapt(en,es) is None:raise ValueError(f'Technical/numeric mismatch: {key}')
        memory[normalize(en)].add(es)
    evidence_path=ROOT/'dev-tools/translation/reviewed-fields.json';evidence={r['field']:r for r in load(evidence_path)}
    count=Counter()
    for source_path in sorted(SOURCE.glob('*.en.json')):
        source=load(source_path);target=ROOT/f'compendium/{source["collection"]}.json';payload=load(target)
        for doc in source['documents']:
            patch=payload['entries'].setdefault(doc['_id'],{})
            for field,en in fields(doc,source['documentType']):
                if field[-1] not in ['description','biography','text']:continue
                choices={adapt(en,es) for es in memory.get(normalize(en),set())}-{None}
                if len(choices)!=1:continue
                es=choices.pop();address='.'.join((source['collection'],doc['_id'],*field));current=get(patch,field)
                if current is not None and evidence.get(address,{}).get('review')!='bestiary-prose':continue
                if current==es:continue
                put(patch,field,es);count[source['collection']]+=1
                evidence[address]={'field':address,'sourceSha256':sha256(en.encode()).hexdigest(),
                    'translationSha256':sha256(es.encode()).hexdigest(),'review':'bestiary-prose'}
        if count[source['collection']]:save(target,payload)
    save(evidence_path,list(evidence.values()));print(f'{len(reviewed)}/{len(index)} reviewed source texts');print(dict(count))

if __name__=='__main__':main()
