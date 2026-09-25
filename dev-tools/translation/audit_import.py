"""Compare actual world documents with the pre-import translated Adventure."""
import re
from text_schema import DATA, SOURCE, fields, load, save


def canonical(text):
    if not isinstance(text, str): return text
    return re.sub(r'<(hr|br|img)([^>]*?)\s*/>', r'<\1\2>', text)


def main():
    original = load(next(SOURCE.glob('*adventures.en.json')))['documents'][0]
    expected = load(DATA/'pbso-adventures.runtime.json')['documents'][0]
    actual = load(DATA/'adventure-imported.runtime.json')['documents'][0]
    runtime = load(DATA/'import-validation.json')
    if runtime['status'] != 'imported' or runtime['missing']:
        raise SystemExit('Incomplete world import')
    before, after = dict(fields(expected,'Adventure')), dict(fields(actual,'Adventure'))
    errors, normalized, inherited, compared = [], [], [], 0
    for path, _ in fields(original,'Adventure'):
        # Adventure's own title/caption/description are importer UI, not world documents.
        if len(path) == 1: continue
        compared += 1
        a, b = before[path], after.get(path)
        if a == b: continue
        if canonical(a) == canonical(b):
            normalized.append({'field':path,'reason':'HTML void-element serialization'})
            continue
        # Core v14 merges linked-token effects into the base actor and removes ActorDelta.
        if len(path)==8 and path[:2]==('scenes','pbsoRedbrandsHid') and path[4:6]==('delta','effects'):
            token=next(t for s in actual['scenes'] if s['_id']==path[1] for t in s['tokens'] if t['_id']==path[3])
            actor=next(a for a in actual['actors'] if a['_id']==token['actorId'])
            effect=next((e for e in actor['effects'] if e['_id']==path[6]),None)
            if token['actorLink'] and not (token.get('delta') or {}).get('effects') and effect and path[6] in ['dnd5eunconscious','dnd5einvisible00']:
                base=('actors',actor['_id'],'effects',path[6],path[7])
                if canonical(after.get(base))==canonical(before.get(base)) and after.get(base):
                    normalized.append({'field':path,'reason':'Linked-token effect retained on base actor','base':base})
                    continue
        errors.append({'field':path,'expected':a,'actual':b})
    source_fields=fields(original,'Adventure')
    for row in runtime['unresolved']:
        occurrences=[p for p,v in source_fields if row['uuid'] in v]
        if occurrences: inherited.append({**row,'sourceFields':occurrences})
        else: errors.append({'kind':'introduced-unresolved-reference',**row})
    report={'date':runtime['date'],'comparedWorldFields':compared,'errors':errors,
            'normalizations':normalized,'referenceCount':runtime['referenceCount'],
            'inheritedUnresolvedReferences':inherited,'counts':runtime['counts']}
    save(DATA/'import-audit.json',report)
    print({k:len(v) if isinstance(v,list) else v for k,v in report.items() if k!='counts'})
    if errors: raise SystemExit('Import differences require review')


if __name__=='__main__':main()
