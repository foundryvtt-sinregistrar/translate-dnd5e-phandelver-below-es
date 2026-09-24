"""Verify committed review evidence against current originals and live payloads."""
from collections import Counter
from hashlib import sha256
from text_schema import ROOT, SOURCE, fields, get, load, technical, numbers
from html.parser import HTMLParser

class Attributes(HTMLParser):
    def __init__(self,text):
        super().__init__();self.values=[];self.feed(text)
    def handle_starttag(self,tag,attrs):
        if attrs:self.values.append((tag,sorted(attrs)))

def main():
    originals={};translations={};coverage=[]
    for path in sorted(SOURCE.glob('*.en.json')):
        source=load(path);payload=load(ROOT/f'compendium/{source["collection"]}.json')
        total=present=0
        for doc in source['documents']:
            for field,en in fields(doc,source['documentType']):
                address='.'.join((source['collection'],doc['_id'],*field))
                es=get(payload['entries'].get(doc['_id'],{}),field)
                if source['documentType']=='RollTable' and field[0]=='results' and es is None:
                    result=next(r for r in doc['results'] if r['_id']==field[1])
                    es=get(payload['entries'].get(doc['_id'],{}),('results','-'.join(map(str,result['range'])),*field[2:]))
                originals[address]=en;translations[address]=es
                total+=1;present+=isinstance(es,str)
        coverage.append({'collection':source['collection'],'fields':total,'present':present,'missing':total-present})
    errors=[]
    for row in load(ROOT/'dev-tools/translation/reviewed-fields.json'):
        address=row['field'];en=originals[address];es=translations[address]
        if not isinstance(es,str):errors.append((address,'missing'));continue
        if sha256(en.encode()).hexdigest()!=row['sourceSha256']:errors.append((address,'source changed'))
        if sha256(es.encode()).hexdigest()!=row['translationSha256']:errors.append((address,'translation changed'))
        if technical(en)!=technical(es):errors.append((address,'technical tokens'))
        if numbers(en)!=numbers(es):errors.append((address,'numbers'))
        if Attributes(en).values!=Attributes(es).values:errors.append((address,'HTML attributes'))
    for row in coverage:print(row)
    print(f'Review evidence errors: {len(errors)}')
    if errors:raise SystemExit(str(errors))

if __name__=='__main__':main()
