"""Compose Actor Index pages from reviewed exact biographies and reference labels."""
import re
from collections import defaultdict
from hashlib import sha256
from text_schema import ROOT,SOURCE,DATA,load,save,fields,get,put,normalize,adapt
from apply_adventure_labels import labels

HEADINGS={
    'References':'Referencias','Changelog':'Registro de cambios',
    'A Dangerous Journey':'Un viaje peligroso','Beyond a Lightless Star':'Más allá de un sol muerto',
    "Conyberry and Agatha's Lair":'Conyberry y la guarida de Agatha','Far Realm Rifts':'Grietas del Reino Lejano',
    'Paths of Peril':'Senderos peligrosos','Phandalin Missions':'Misiones en Phandalin',
    'Redbrand Ruffians Confrontation':'Enfrentamiento con los Redbrands','Rifts in Reality':'Grietas en la realidad',
    'Stolen Shards Encounters':'Encuentros de los fragmentos robados',"The Spider's Web":'La Telaraña',
    'Trouble in Phandalin':'Problemas en Phandalin','Welcome to Phandalin':'Bienvenido a Phandalin',
}

def biography_key(value):
    # HTML void-element spelling is the sole extra equivalence permitted here.
    return normalize(re.sub(r'<hr\s*/?>', '<hr>', value))

def compose(raw,memory,names):
    match=re.search(r'<section class="bio">(.*?)</section>',raw,re.S)
    if not match:
        # Remorhaz has a portrait followed by an unwrapped, complete biography.
        match=re.fullmatch(r'<figure\b[^>]*><img\b[^>]*></figure>(<p>.*)',raw,re.S)
    if not match:return None,'missing-bio-section'
    if match[1] in ('','<p></p>'):
        candidates={match[1]}
    else:
        candidates={adapt(match[1],value) for value in memory.get(biography_key(match[1]),set())}-{None}
    if len(candidates)!=1:return None,'biography-not-reviewed-exactly'
    bio=candidates.pop()
    def outer(value):
        result=[]
        for part in re.split(r'(<[^>]+>|@UUID\[[^]]+\](?:\{[^}]+\})?)',value):
            if part.startswith(('<','@UUID[')):
                if part.startswith('@UUID[') and '{' in part:
                    key=part.split('{',1)[1][:-1]
                    if key not in names:return None
                    part=part.split('{',1)[0]+'{'+names[key]+'}'
                result.append(part);continue
            clean=part.strip()
            if not clean:result.append(part);continue
            suffix=':' if clean.endswith(':') else ''
            key=clean[:-1] if suffix else clean
            if key not in names:return None
            result.append(part.replace(clean,names[key]+suffix))
        return ''.join(result)
    before,after=outer(raw[:match.start(1)]),outer(raw[match.end(1):])
    if before is None or after is None:return None,'unreviewed-reference-text'
    result=before+bio+after
    if adapt(raw,result) is None:raise ValueError('Index page technical mismatch')
    return result,None

def main():
    evidence_path=ROOT/'dev-tools/translation/reviewed-fields.json'
    evidence={r['field']:r for r in load(evidence_path)}
    memory=defaultdict(set)
    for path in SOURCE.glob('*.en.json'):
        s=load(path);payload=load(ROOT/f'compendium/{s["collection"]}.json')
        for doc in s['documents']:
            patch=payload['entries'].get(doc['_id'],{})
            for field,en in fields(doc,s['documentType']):
                if field[-1]!='biography':continue
                address='.'.join((s['collection'],doc['_id'],*field));es=get(patch,field);proof=evidence.get(address)
                if es is None or not proof:continue
                if proof['sourceSha256']!=sha256(en.encode()).hexdigest() or proof['translationSha256']!=sha256(es.encode()).hexdigest():
                    raise ValueError('Stale biography evidence: '+address)
                memory[biography_key(en)].add(es)
    s=load(SOURCE/'dnd-phandelver-below.pbso-adventures.en.json');doc=s['documents'][0]
    target=ROOT/f'compendium/{s["collection"]}.json';payload=load(target);patch=payload['entries'][doc['_id']]
    names={**labels(),**HEADINGS};pending=[];count=0
    journal=next(j for j in doc['journal'] if j['_id']=='pbsoActorIndex00')
    for page in journal['pages']:
        field=('journals',journal['_id'],'pages',page['_id'],'text');raw=page.get('text',{}).get('content','')
        if not raw:continue
        address='.'.join((s['collection'],doc['_id'],*field));current=get(patch,field)
        if current is not None and evidence.get(address,{}).get('review')!='actor-index-exact-biography':continue
        es,reason=compose(raw,memory,names)
        if es is None:pending.append({'id':page['_id'],'name':page['name'],'reason':reason});continue
        if current==es:continue
        put(patch,field,es);count+=1
        evidence[address]={'field':address,'sourceSha256':sha256(raw.encode()).hexdigest(),
            'translationSha256':sha256(es.encode()).hexdigest(),'review':'actor-index-exact-biography'}
    save(target,payload);save(evidence_path,list(evidence.values()));save(DATA/'actor-index-pending.json',pending)
    print(f'Actor Index: {count} pages applied; {len(pending)} awaiting exact review')

if __name__=='__main__':main()
