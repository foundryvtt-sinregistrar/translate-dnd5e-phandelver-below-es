"""Audit existing translation coverage and protected Foundry syntax by ID."""
from collections import Counter
import json
import re
from pathlib import Path
import sys
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'dev-tools/export/_data'
sys.path.insert(0,str(ROOT/'dev-tools/export'))
from validate_current_export import BASE, validate

TOKEN = re.compile(r'@[A-Za-z]+\[[^\]]+\]|\[\[[\s\S]*?\]\]|&(?:amp;)?[Rr]eference\[[^\]]+\]')
def tokens(text):
    return Counter(re.sub(r'\s*#.*(?=\]\]$)', '', t) for t in TOKEN.findall(text))
def plain(text):
    return re.sub(r'<[^>]+>', ' ', TOKEN.sub(' ',text))
def numbers(text, language):
    value = plain(text)
    # Normalize thousands separators without confusing decimal measures.
    separator = ',' if language == 'en' else r'[ \u00a0\u202f]'
    value = re.sub(r'(?<!\d)(\d{1,3})(?:'+separator+r'\d{3})+(?!\d)',
                   lambda m: re.sub(r'[, \u00a0\u202f]', '', m[0]), value)
    if language == 'es':
        value = re.sub(r'(?<=\d),(?=\d)', '.', value)
    return Counter(re.findall(r'\d+(?:\.\d+)?', value))

class ProtectedHTML(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.attributes = Counter()
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in {'href', 'src', 'id'} or key.startswith('data-'):
                self.attributes[(tag, key, value)] += 1

def protected_html(text):
    return Counter({repr(k):v for k,v in ProtectedHTML(text).attributes.items()})
def load(path):
    return json.loads(path.read_text(encoding='utf-8'))

def main():
    directory = sorted(BASE.glob('*/inventory.json'))[-1].parent
    manifest = validate(directory)
    issues=[]; coverage=[]; page_rows=[]
    def compare(path,en,es):
        if not isinstance(es,str): return
        for kind, old, new in [('syntax',tokens(en),tokens(es)),
                               ('html_attributes',protected_html(en),protected_html(es)),
                               ('numbers',numbers(en,'en'),numbers(es,'es'))]:
            if old != new:
                issue={'kind':kind,'path':path,'removed':dict(old-new),'added':dict(new-old)}
                if kind == 'numbers':
                    issue['contains_units'] = bool(re.search(r'\b(feet|foot|mile|miles|pounds?|inches)\b',plain(en),re.I))
                issues.append(issue)
        if '\ufffd' in es or re.search(r'Ã[\u0080-\u00bf]|Â[\u0080-\u00bf]',es):
            issues.append({'kind':'encoding','path':path})
    for pack in manifest['packs']:
        source=load(directory/pack['filename'])['documents']
        payload=load(ROOT/'compendium'/f"{pack['collection']}.json")
        entries=payload['entries']
        coverage.append({'pack':pack['collection'],'source_documents':len(source),'translation_entries':len(entries)})
        for doc in source:
            tr=entries.get(doc['_id'],{});prefix=f"{pack['collection']}/{doc['_id']}"
            if 'name' in tr:compare(prefix+'/name',doc['name'],tr['name'])
            if pack['documentType']=='Adventure':
                for field in ['description','caption']:
                    if field in tr:compare(prefix+'/'+field,doc.get(field,''),tr[field])
                for journal in doc['journal']:
                    translated=tr.get('journals',{}).get(journal['_id'],{})
                    for page in journal['pages']:
                        pp=translated.get('pages',{}).get(page['_id'],{})
                        en=(page.get('text') or {}).get('content','') or ''
                        path=f"{prefix}/journals/{journal['_id']}/pages/{page['_id']}"
                        page_rows.append({'journal_id':journal['_id'],'journal':journal['name'], 'page_id':page['_id'],
                            'page':page['name'],'type':page['type'],'source_characters':len(en),'has_name':'name' in pp,
                            'has_text':bool(pp.get('text')),'source_has_text':bool(en),
                            'text_equal':pp.get('text')==en if en else False})
                        if 'text' in pp:compare(path+'/text',en,pp['text'])
            if pack['documentType']=='RollTable':
                for result in doc['results']:
                    row=tr.get('results',{}).get(result['_id'],tr.get('results',{}).get('-'.join(map(str,result['range'])),{}))
                    if 'description' in row:compare(f"{prefix}/results/{result['_id']}/description",result.get('description',''),row['description'])
    report={'source':directory.name,'coverage':coverage,'pages':page_rows,'issues':issues,
            'issue_counts':dict(Counter(x['kind'] for x in issues)),
            'limits':'Numbers and syntax differences are review candidates, not automatically translation errors.'}
    (DATA/'translation-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# Cobertura actual por diario', '',
           'Generado con `python dev-tools/translation/audit_current.py`.', '',
           f"Fuente: `{directory.name}`. La presencia de texto no certifica revisión editorial.", '',
           '| Diario original / ID | Páginas | Con texto original | Con texto traducido | Texto pendiente |',
           '|---|---:|---:|---:|---:|']
    for journal_id in dict.fromkeys(p['journal_id'] for p in page_rows):
        rows=[p for p in page_rows if p['journal_id']==journal_id]
        source_text=sum(p['source_has_text'] for p in rows)
        translated_text=sum(p['has_text'] for p in rows)
        missing=sum(p['source_has_text'] and not p['has_text'] for p in rows)
        lines.append(f"| {rows[0]['journal']} (`{journal_id}`) | {len(rows)} | {source_text} | {translated_text} | {missing} |")
    lines += ['', 'Los detalles por ID y las incidencias están en `../export/_data/translation-audit.json`.',
              'Los avisos numéricos no se corrigen automáticamente: pueden reflejar unidades o diferencias reales.', '']
    (ROOT/'dev-tools/translation/COBERTURA-ACTUAL.md').write_text('\n'.join(lines),encoding='utf-8')
    print(json.dumps({'coverage':coverage,'pages':len(page_rows),'with_original_text':sum(p['source_has_text'] for p in page_rows),
        'with_translated_text':sum(p['has_text'] for p in page_rows),'issues':report['issue_counts']},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
