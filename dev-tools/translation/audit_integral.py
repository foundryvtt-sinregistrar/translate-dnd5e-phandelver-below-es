"""Validate every allowlisted field, including Adventure copies and ActorDelta."""
from collections import Counter
import re
from text_schema import ROOT, DATA, SOURCE, TECH, fields, get, load, save, technical, numbers
from check_reviewed import Attributes


def currency(text, language):
    text = re.sub(r'\[/award[^\]]*\]', '', text)
    text = re.sub(r'<[^>]+>', ' ', TECH.sub(' ', text))
    text = re.sub(r'\b\d{1,3}(?:[,.]\d{3})+', lambda m: re.sub('[,.]', '', m[0]), text)
    codes = {'gp':'po','sp':'pp','pp':'ppt','ep':'pe','cp':'pc'} if language == 'en' else {c:c for c in ['po','ppt','pp','pe','pc']}
    return Counter((n, codes[c]) for n,c in re.findall(r'\b(\d+)\s*('+'|'.join(codes)+r')\b', text))


def main():
    coverage=[]; errors=[]; unchanged=[]
    for path in sorted(SOURCE.glob('*.en.json')):
        source=load(path); payload=load(ROOT/f'compendium/{source["collection"]}.json')
        total=present=0
        for doc in source['documents']:
            patch=payload['entries'].get(doc['_id'], {})
            for field,en in fields(doc,source['documentType']):
                address='.'.join((source['collection'],doc['_id'],*field))
                es=get(patch,field)
                if es is None and source['documentType']=='RollTable' and field[0]=='results':
                    row=next(r for r in doc['results'] if r['_id']==field[1])
                    es=get(patch,('results','-'.join(map(str,row['range'])),*field[2:]))
                total+=1
                if not isinstance(es,str): errors.append({'field':address,'kind':'missing'});continue
                present+=1
                for kind,fn in [('technical',technical),('numbers',numbers),('html',lambda s:Attributes(s).values)]:
                    if fn(en)!=fn(es):errors.append({'field':address,'kind':kind})
                if currency(en,'en')!=currency(es,'es'):errors.append({'field':address,'kind':'currency'})
                visible=re.sub(r'<[^>]+>',' ',TECH.sub(' ',en)).strip()
                if es==en and len(visible)>60:unchanged.append({'field':address,'text':visible})
        coverage.append({'collection':source['collection'],'total':total,'present':present})
    report={'source':SOURCE.name,'coverage':coverage,'errors':errors,'unchangedLongText':unchanged}
    save(DATA/'integral-audit.json',report)
    print({'fields':sum(r['total'] for r in coverage),'present':sum(r['present'] for r in coverage),
           'errors':len(errors),'unchangedLongText':len(unchanged)})
    if errors:raise SystemExit(str(errors))


if __name__=='__main__':main()
