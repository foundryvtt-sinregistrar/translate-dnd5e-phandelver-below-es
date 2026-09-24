"""Prepare offline drafts under ignored _data; never write distributable payloads."""
import html
import json
import re
import sys
import time
from pathlib import Path
from text_schema import ROOT, DATA, load, save, technical, numbers

RUNTIME = ROOT.parent/'translate-dnd5e-dm-2024-es/tmp'
sys.path.insert(0,str(RUNTIME/'translation-runtime'))
TOKEN = re.compile(r'(<[^>]+>|@[A-Za-z][A-Za-z0-9]*\[[^\]]+\](?:\{[^}]*\})?|\[\[[\s\S]*?\]\](?:\{[^}]*\})?|&(?:amp;)?[Rr]eference\[[^\]]+\](?:\{[^}]*\})?|https?://[^\s<>]+)')


def pieces(text):
    for token in TOKEN.split(text):
        if not token:continue
        if TOKEN.fullmatch(token):
            label=re.fullmatch(r'(.*\])\{([^}]*)\}',token,re.S)
            if label:
                yield 'literal',label[1]+'{'
                yield from pieces(label[2])
                yield 'literal','}'
            elif token.startswith('[[') and ' # ' in token:
                head,label=token[:-2].split(' # ',1)
                yield 'literal',head+' # '
                yield from pieces(label)
                yield 'literal',']]'
            else:yield 'literal',token
        else:
            leading=token[:len(token)-len(token.lstrip())]
            trailing=token[len(token.rstrip()):]
            if leading:yield 'literal',leading
            core=html.unescape(token.strip())
            chunks=[]
            for sentence in re.split(r'(?<=[.!?])\s+(?=[A-Z])',core):
                words=sentence.split(' ')
                chunks.extend(' '.join(words[i:i+85]) for i in range(0,len(words),85))
            for i,chunk in enumerate(chunks):
                if i:yield 'literal',' '
                if chunk:yield 'text',chunk
            if trailing and core:yield 'literal',trailing


def main():
    import ctranslate2
    import sentencepiece
    queue=load(DATA/'remaining-fields.json')
    cache_path=DATA/'remaining-segments.jsonl'
    cache={}
    if cache_path.exists():
        for line in cache_path.read_text(encoding='utf-8').splitlines():
            row=json.loads(line);cache[row['source']]=row['translation']
    jobs=[];unique=set()
    for row in queue:
        if 'candidate' in row:continue
        parts=list(pieces(row['source']))
        jobs.append((row,parts))
        unique.update(value for kind,value in parts if kind=='text' and re.search('[A-Za-z]',value))
    todo=sorted(unique-cache.keys(),key=lambda x:(len(x),x))
    print(f'{len(jobs)} fields; {len(todo)} uncached segments',flush=True)
    model=RUNTIME/'opus-en-es'
    src=sentencepiece.SentencePieceProcessor(model_file=str(model/'source.spm'))
    tgt=sentencepiece.SentencePieceProcessor(model_file=str(model/'target.spm'))
    engine=ctranslate2.Translator(str(model/'ct2'),device='cpu',compute_type='int8',inter_threads=2,intra_threads=4)
    started=time.monotonic()
    with cache_path.open('a',encoding='utf-8') as output:
        for start in range(0,len(todo),64):
            batch=todo[start:start+64]
            translated=engine.translate_batch([src.encode(x,out_type=str) for x in batch],beam_size=2,
                max_batch_size=64,max_input_length=0,max_decoding_length=512)
            for en,result in zip(batch,translated):
                es=tgt.decode(result.hypotheses[0]);cache[en]=es
                output.write(json.dumps({'source':en,'translation':es},ensure_ascii=False)+'\n')
            output.flush()
            print(f'{min(start+64,len(todo))}/{len(todo)} segments; {time.monotonic()-started:.0f}s',flush=True)
    for row,parts in jobs:
        markup=bool(TOKEN.search(row['source']))
        row['candidate']=''.join(value if kind=='literal' else
            html.escape(cache.get(value,value),quote=False) if markup else cache.get(value,value) for kind,value in parts)
        row['status']='candidate-local-draft'
        row['checks']={'syntax':technical(row['source'])==technical(row['candidate']),
                       'numbers':numbers(row['source'])==numbers(row['candidate'])}
    save(DATA/'remaining-draft.json',queue)
    print('Private drafts saved; no live translations changed.',flush=True)


if __name__=='__main__': main()
