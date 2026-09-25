"""Align reviewed prose with the project names; never change technical tokens."""
import re
from text_schema import ROOT,load,save

REPLACEMENTS={
    'Cueva del Eco':'Cueva del Oleaje',
    'mephit de polvo':'mefit de polvo',
    'montículo errante':'broza movediza',
    'El montículo errante':'La broza movediza',
    'el montículo errante':'la broza movediza',
    'El perforador':'La barrena',
    'el perforador':'la barrena',
    'fomoriano':'fomoré',
    'Mirada pavorosa':'Mirada aterradora',
}

def main():
    pattern=re.compile('|'.join(map(re.escape,sorted(REPLACEMENTS,key=len,reverse=True))))
    for path in [*sorted((ROOT/'dev-tools/translation').glob('bestiary-texts-*.json')),
                 ROOT/'dev-tools/translation/combat-phrases.json']:
        data=load(path);changed=False
        for key,value in data.items():
            chunks=re.split(r'(<[^>]+>|\[\[.*?\]\]|@UUID\[[^]]+\]|&amp;Reference\[[^]]+\])',value)
            result=''.join(c if c.startswith(('<','[[','@UUID[','&amp;Reference[')) else
                pattern.sub(lambda m:REPLACEMENTS[m[0]],c) for c in chunks)
            if result!=value:data[key]=result;changed=True
        if changed:save(path,data);print(path.name)

if __name__=='__main__':main()
