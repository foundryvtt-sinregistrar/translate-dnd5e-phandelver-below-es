"""Fill missing fields only from unambiguous, hash-verified identical originals."""
from collections import defaultdict,Counter
from hashlib import sha256
from text_schema import ROOT,SOURCE,load,save,fields,get,put,adapt
from apply_actor_index import biography_key

def main():
    evidence_path=ROOT/'dev-tools/translation/reviewed-fields.json'
    evidence={r['field']:r for r in load(evidence_path)}
    memory=defaultdict(set);packs=[]
    for path in sorted(SOURCE.glob('*.en.json')):
        source=load(path);target=ROOT/f'compendium/{source["collection"]}.json';payload=load(target)
        packs.append((source,target,payload))
        for doc in source['documents']:
            patch=payload['entries'].get(doc['_id'],{})
            for field,en in fields(doc,source['documentType']):
                address='.'.join((source['collection'],doc['_id'],*field));proof=evidence.get(address)
                if not proof:continue
                es=get(patch,field)
                if not isinstance(es,str) or proof['sourceSha256']!=sha256(en.encode()).hexdigest() or proof['translationSha256']!=sha256(es.encode()).hexdigest():
                    raise ValueError('Stale review: '+address)
                memory[(field[-1],biography_key(en))].add(es)
    counts=Counter()
    for source,target,payload in packs:
        for doc in source['documents']:
            patch=payload['entries'].setdefault(doc['_id'],{})
            for field,en in fields(doc,source['documentType']):
                if get(patch,field) is not None:continue
                candidates={adapt(en,es) for es in memory.get((field[-1],biography_key(en)),set())}-{None}
                if len(candidates)!=1:continue
                es=candidates.pop();put(patch,field,es)
                address='.'.join((source['collection'],doc['_id'],*field))
                evidence[address]={'field':address,'sourceSha256':sha256(en.encode()).hexdigest(),
                    'translationSha256':sha256(es.encode()).hexdigest(),'review':'verified-exact-memory'}
                counts[source['collection']]+=1
        if counts[source['collection']]:save(target,payload)
    save(evidence_path,list(evidence.values()));print(dict(counts))

if __name__=='__main__':main()
