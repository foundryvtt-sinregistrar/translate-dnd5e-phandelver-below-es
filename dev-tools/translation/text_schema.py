"""Reuse local bilingual fields only when their original English text matches.

No network calls. References retain the destination compendium's UUIDs.
Existing reviewed translations always win. Unmatched fields remain pending.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'dev-tools/export/_data'
SOURCE = DATA / 'source-current/2026-09-24T19-12-21-788Z'
UUID = re.compile(r'Compendium\.[^.\s\]]+\.[^.\s\]]+\.[^\]\s]+')
TECH = re.compile(r'@[A-Za-z][A-Za-z0-9]*\[[^\]]+\]|\[\[[\s\S]*?\]\]|&(?:amp;)?[Rr]eference\[[^\]]+\]')
def repair_known_markup(text):
    # Original Adventure purple-worm Bite has a closing brace instead of ].
    return text.replace('&amp;Reference[total-cover}{total cover}', '&amp;Reference[total-cover]{total cover}')

def technical(text):
    text = repair_known_markup(text)
    return sorted(re.sub(r'\s*#\s*[^\]]+(?=\]\]$)', '', x) for x in TECH.findall(text))
def numbers(text):
    text = repair_known_markup(text)
    text = re.sub(r'<[^>]+>', ' ', TECH.sub(' ', text))
    text = re.sub(r'\b\d{1,3}(?:[,.]\d{3})+(?!\d)', lambda m:re.sub('[,.]', '', m[0]), text)
    return sorted(re.findall(r'\d+', text))
def canonical_uuid(s):
    return re.sub(r'^Compendium\.[^.]+\.[^.]+\.', 'Compendium.*.', s)
def normalize(s):
    s = UUID.sub(lambda m: canonical_uuid(m[0]), s)
    return re.sub(r'\s+', ' ', s.strip()).replace('’', "'")
def adapt(source, translated):
    exact = {m[0] for m in UUID.finditer(source)}
    destinations = defaultdict(set)
    for uuid in exact:
        destinations[canonical_uuid(uuid)].add(uuid)
    for m in UUID.finditer(translated):
        if m[0] not in exact and len(destinations.get(canonical_uuid(m[0]), ())) != 1: return None
    result = UUID.sub(lambda m: m[0] if m[0] in exact else next(iter(destinations[canonical_uuid(m[0])])), translated)
    if technical(source) != technical(result) or numbers(source) != numbers(result): return None
    return result
def base_fields(doc, kind, prefix=()):
    def emit(path, value):
        if isinstance(value, str): return [(prefix + path, value)]
        return []
    out = emit(('name',), doc.get('name'))
    system = doc.get('system', {})
    if kind == 'Item':
        out += emit(('requirements',), system.get('requirements'))
        out += emit(('description',), system.get('description', {}).get('value'))
        out += emit(('descriptionChat',), system.get('description', {}).get('chat'))
        out += emit(('unidentifiedName',), system.get('unidentified', {}).get('name'))
        out += emit(('unidentifiedDescription',), system.get('unidentified', {}).get('description'))
        for aid, activity in system.get('activities', {}).items():
            out += emit(('activities', aid, 'name'), activity.get('name'))
            for group, keys in {'activation': ['condition'], 'description': ['chatFlavor', 'value'], 'range': ['special'], 'roll': ['name']}.items():
                for key in keys: out += emit(('activities', aid, group, key), get(activity, (group, key)))
            out += emit(('activities', aid, 'target', 'affects', 'special'), get(activity, ('target', 'affects', 'special')))
    if kind == 'Actor':
        for field,path in {'alignment':('details','alignment'), 'habitat':('details','habitat','custom'), 'creatureType':('details','type','custom'), 'creatureSubtype':('details','type','subtype'), 'languages':('traits','languages','custom'), 'senses':('attributes','senses','special'), 'biographyPublic':('details','biography','public')}.items():
            out += emit((field,), get(system,path))
        out += emit(('tokenName',), doc.get('prototypeToken', {}).get('name'))
        out += emit(('biography',), system.get('details', {}).get('biography', {}).get('value'))
        for item in doc.get('items', []): out += fields(item, 'Item', prefix + ('items', item['_id']))
    if kind == 'JournalEntry':
        for page in doc.get('pages', []):
            out += emit(('pages', page['_id'], 'name'), page.get('name'))
            out += emit(('pages', page['_id'], 'text'), page.get('text', {}).get('content'))
            out += emit(('pages', page['_id'], 'caption'), page.get('image', {}).get('caption'))
    if kind == 'RollTable':
        out += emit(('description',), doc.get('description'))
        for result in doc.get('results', []):
            for key in ['name', 'description']: out += emit(('results', result['_id'], key), result.get(key))
    if kind == 'Scene':
        out += emit(('navigation',), doc.get('navName'))
        for group, key in [('notes', 'text'), ('drawings', 'text'), ('tokens', 'name'), ('regions', 'name')]:
            for child in doc.get(group, []): out += emit((group, child['_id'], key), child.get(key))
    for effect in doc.get('effects', []):
        for key in ['name', 'description']: out += emit(('effects', effect['_id'], key), effect.get(key))
    return out
def get(obj, path):
    for key in path:
        if not isinstance(obj, dict): return None
        obj = obj.get(key)
    return obj
def put(obj, path, value):
    for key in path[:-1]: obj = obj.setdefault(key, {})
    obj[path[-1]] = value
def load(path): return json.loads(path.read_text(encoding='utf8'))
def save(path, value): path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf8')

COLLECTIONS = {'actors': 'Actor', 'items': 'Item', 'journal': 'JournalEntry',
               'scenes': 'Scene', 'tables': 'RollTable', 'macros': 'Macro',
               'playlists': 'Playlist', 'cards': 'Cards'}


def fields(doc, kind, prefix=()):
    out = base_fields(doc, kind, prefix)
    def emit(path, value):
        if isinstance(value, str) and value.strip(): out.append((prefix + path, value))
    if kind == 'Adventure':
        for key in ['description', 'caption']: emit((key,), doc.get(key))
        for key, child_kind in COLLECTIONS.items():
            target = 'journals' if key == 'journal' else key
            for child in doc.get(key, []):
                out += fields(child, child_kind, prefix + (target, child['_id']))
        for folder in doc.get('folders', []): emit(('folders', folder['_id']), folder.get('name'))
    if kind == 'Item':
        advancement = doc.get('system', {}).get('advancement', {})
        for aid, advance in (advancement.items() if isinstance(advancement, dict) else ((x['_id'], x) for x in advancement)):
            for key in ['name', 'hint']: emit(('advancement', aid, key), advance.get(key))
    if kind == 'Scene':
        for token in doc.get('tokens', []):
            if token.get('delta'):
                out += fields(token['delta'], 'Actor', prefix + ('tokens', token['_id'], 'delta'))
        for level in doc.get('levels', []): emit(('levels', level['_id'], 'name'), level.get('name'))
        for region in doc.get('regions', []):
            for behavior in region.get('behaviors', []):
                base = ('regions', region['_id'], 'behaviors', behavior['_id'])
                emit(base + ('name',), behavior.get('name'))
                if behavior.get('type') == 'displayScrollingText': emit(base + ('text',), get(behavior, ('system', 'text')))
                if behavior.get('type') == 'teleportToken':
                    for key in ['revealed', 'unrevealed']:
                        emit(base + (key+'Dialog',), get(behavior, ('system', 'dialog', key)))
    return [(p, s) for p, s in out if s.strip()]
