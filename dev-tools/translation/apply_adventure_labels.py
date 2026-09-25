"""Apply reviewed Adventure labels, never scripts or document mechanics."""
import re
from hashlib import sha256
from collections import Counter
from text_schema import ROOT,SOURCE,load,save,fields,get,put,adapt

def labels():
    folder=ROOT/'dev-tools/translation'
    result={v:v for v in load(folder/'adventure-proper-names.json')}
    for file in ['actor-names.json','item-names.json','adventure-labels.json','adventure-captions.json']:
        result.update(load(folder/file))
    result['Iarno “Glasstaff” Albrek']=result['Iarno "Glasstaff" Albrek']
    return result

def translate(value,memory):
    if value in memory:return memory[value]
    if re.fullmatch(r'\d+\.\d+\.\d+',value):return value
    for en,es in [(' (DM)',' (DM)'),(' (Player)',' (jugadores)'),
                  (' (Players)',' (jugadores)'),(' (Player Version)',' (versión para jugadores)'),
                  (' (Unlabeled)',' (sin etiquetas)')]:
        if value.endswith(en) and value[:-len(en)] in memory:return memory[value[:-len(en)]]+es
    if '. Artist: ' in value:
        subject,artist=value.split('. Artist: ',1)
        if subject in memory:return memory[subject]+'. Ilustración: '+artist
    return None

def main():
    s=load(SOURCE/'dnd-phandelver-below.pbso-adventures.en.json')
    target=ROOT/f'compendium/{s["collection"]}.json';payload=load(target)
    evidence_path=ROOT/'dev-tools/translation/reviewed-fields.json'
    evidence={r['field']:r for r in load(evidence_path)};memory=labels();count=Counter();pending=set()
    for doc in s['documents']:
        patch=payload['entries'][doc['_id']]
        for path,en in fields(doc,'Adventure'):
            scene_annotation=path[0]=='scenes' and len(path)==5 and path[2] in ['notes','drawings'] and path[-1]=='text'
            if path[-1] not in ['name','navigation','caption'] and not scene_annotation:continue
            if get(patch,path) is not None:continue
            es=translate(en,memory)
            if es is None:pending.add(en);continue
            if adapt(en,es) is None:raise ValueError(path)
            put(patch,path,es);count[path[0]]+=1
            address='.'.join((s['collection'],doc['_id'],*path))
            evidence[address]={'field':address,'sourceSha256':sha256(en.encode()).hexdigest(),
                'translationSha256':sha256(es.encode()).hexdigest(),'review':'adventure-labels'}
    save(target,payload);save(evidence_path,list(evidence.values()))
    print(dict(count));print('Pending unique labels:',len(pending))
    for en in sorted(pending):print(en)

if __name__=='__main__':main()
