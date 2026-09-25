"""Compose only the explicitly inspected attack paragraphs using reviewed phrases."""
import re
from text_schema import ROOT,DATA,load,save

REVIEWED_IDS=[308,309,310,311,312,314,315,316,317,319,320,321,322,323,324,325,326,
              328,329,330,331,332,333,334,335,338,340,341,342,343,344,345,346,347,
              348,350,351,352,354,355,357,365,366,367,371,373,375,379,380,381,382,384,
              385,386,388,389,390,391,392,393,414,417,419,420,425,
              426,427,429,431,432,434,436,437,440,441,442,443,444,445,446,448,
              449,450,452,454,455,456,457,458,460,461,462,463,465,476,477,481,
              482,493,495,502,505,506,509,511,512,513,517,520,523,524,526]

def main():
    source={r['id']:r['source'] for r in load(DATA/'bestiary-review-index.json')}
    phrases=load(ROOT/'dev-tools/translation/combat-phrases.json')
    pattern=re.compile('|'.join(re.escape(en) for en in sorted(phrases,key=len,reverse=True)))
    result={}
    for number in REVIEWED_IDS:
        key=f'{number:04d}';en=source[key]
        # Restrict substitutions to text nodes; markup and commands are untouched.
        tokens=re.split(r'(<[^>]+>|\[\[.*?\]\])',en)
        result[key]=''.join(t if t.startswith(('<','[[')) else pattern.sub(lambda m:phrases[m[0]],t) for t in tokens)
        result[key]=result[key].replace('a impactar,</strong>,','a impactar</strong>, alcance').replace('</em><strong>','</em> <strong>')
    save(ROOT/'dev-tools/translation/bestiary-texts-05.json',result)
    print(f'{len(result)} inspected attack texts composed')

if __name__=='__main__':main()
