"""Compose the reviewed changelog without rewriting UUIDs or issue links."""
import re
from hashlib import sha256
from text_schema import ROOT, SOURCE, load, save, fields, adapt


def main():
    directory = ROOT / 'dev-tools/translation'
    index = {row['id']: row['sha256'] for row in load(directory / 'adventure-source-index.json')}
    document = load(SOURCE / 'dnd-phandelver-below.pbso-adventures.en.json')['documents'][0]
    source = next(text for _, text in fields(document, 'Adventure')
                  if sha256(text.encode()).hexdigest() == index['0214'])
    labels = {}
    for name in ('actor-names', 'item-names', 'adventure-labels', 'trait-names'):
        labels.update(load(directory / f'{name}.json'))
    labels.update({'Acolyte': 'Acólito', 'Iarno': 'Iarno', 'Medusa': 'Medusa',
                   'Old Garrison': 'Antigua guarnición', 'Outlander': 'Forastero', 'area H4': 'área H4'})
    paragraphs = load(directory / 'adventure-changelog-214.json')
    consumed = 0

    def paragraph(match):
        nonlocal consumed
        original = match.group(2)
        links = []
        for link in re.finditer(r'(@UUID\[[^]]*\])\{([^}]*)\}', original):
            links.append(link[1] + '{' + labels[link[2]] + '}')
        translated = paragraphs[consumed]
        assert sorted(map(int, re.findall(r'\{(\d+)\}', translated))) == list(range(len(links)))
        translated = re.sub(r'\{(\d+)\}', lambda m: links[int(m[1])], translated)
        issues = re.search(r' \[<a href=.*\]$', original)
        if issues:
            translated += issues[0]
        consumed += 1
        return match[1] + translated + match[3]

    translated = re.sub(r'(<(?:p|h[1-6])\b[^>]*>)(.*?)(</(?:p|h[1-6])>)', paragraph, source, flags=re.S)
    assert consumed == len(paragraphs) == 138
    assert adapt(source, translated) is not None
    save(directory / 'adventure-texts-12.json', {'0214': translated})
    print(f'Composed {consumed} reviewed paragraphs')


if __name__ == '__main__':
    main()
