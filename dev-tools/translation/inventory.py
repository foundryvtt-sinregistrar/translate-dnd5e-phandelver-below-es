"""Inventory existing Babele payloads against the private historical export.

Presence is not editorial approval. Reports do not modify translations/worklists.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'dev-tools/export/_data'


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def strings(value, path=()):
    if isinstance(value, dict):
        for key, child in value.items():
            yield from strings(child, (*path, key))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from strings(child, (*path, str(index)))
    elif isinstance(value, str):
        yield path, value


def main():
    inventory = load(DATA / 'source/inventory.json')
    reports = []
    for pack in inventory['packs']:
        name = pack['id'] + '.json'
        source_path = DATA / 'source/translations' / name
        target_path = ROOT / 'compendium' / name
        source = load(source_path)['entries']
        target = load(target_path)['entries']
        original = dict(strings(source))
        translated = dict(strings(target))
        shared = original.keys() & translated.keys()
        report = {
            'pack': pack['id'], 'source_entries': len(source),
            'translation_entries': len(target),
            'missing_entry_ids': sorted(source.keys() - target.keys()),
            'unexpected_entry_ids': sorted(target.keys() - source.keys()),
            'source_string_leaves': len(original),
            'present_string_leaves': len(shared),
            'equal_string_leaves': sum(original[p] == translated[p] for p in shared),
            'missing_paths': [list(p) for p in sorted(original.keys() - translated.keys())],
            'unexpected_paths': [list(p) for p in sorted(translated.keys() - original.keys())],
            'source_sha256': hashlib.sha256(source_path.read_bytes()).hexdigest(),
            'translation_sha256': hashlib.sha256(target_path.read_bytes()).hexdigest(),
        }
        if pack['documentName'] == 'Adventure':
            adventure = next(iter(source.values()))
            draft = next(iter(target.values()), {})
            report['nested_source'] = {k: len(v) for k, v in adventure.items() if isinstance(v, dict)}
            report['nested_translation'] = {k: len(v) for k, v in draft.items() if isinstance(v, dict)}
            report['source_journal_pages'] = sum(len(j.get('pages', {})) for j in adventure.get('journals', {}).values())
            report['translation_journal_pages'] = sum(len(j.get('pages', {})) for j in draft.get('journals', {}).values())
        reports.append(report)
    result = {'baseline_generated_at': inventory['generatedAt'],
              'foundry': inventory['foundryVersion'], 'system': inventory['system'],
              'source_module': inventory['sourceModule'],
              'scope': 'Historical exported string leaves, including technical strings; not runtime or linguistic validation.',
              'packs': reports}
    (DATA / 'translation-inventory.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    lines = ['# Inventario de Phandelver & Below', '',
             'Generado con `python dev-tools/translation/inventory.py`.', '',
             f"Fuente histórica: {result['baseline_generated_at']}; Foundry {result['foundry']}, dnd5e {result['system']['version']}, aventura {result['source_module']['version']}.", '',
             '| Pack | Entradas fuente | Entradas actuales | Cadenas presentes / fuente | Cadenas iguales |',
             '|---|---:|---:|---:|---:|']
    for p in reports:
        lines.append(f"| {p['pack'].split('.')[-1]} | {p['source_entries']} | {p['translation_entries']} | {p['present_string_leaves']} / {p['source_string_leaves']} | {p['equal_string_leaves']} |")
    a = next(p for p in reports if 'nested_source' in p)
    lines += ['', '## Contenido de Adventure', '',
              '| Colección | Fuente | Traducción actual |', '|---|---:|---:|']
    for key, count in a['nested_source'].items():
        lines.append(f"| {key} | {count} | {a['nested_translation'].get(key, 0)} |")
    lines += [f"| Páginas de diario | {a['source_journal_pages']} | {a['translation_journal_pages']} |", '',
              '## Límites de este inventario', '',
              'Compara claves y rutas del export histórico; no certifica que las fuentes estén libres de traducciones ni que los mapeos se apliquen en Foundry. Los SHA-256 identifican los archivos actuales, no acreditan su origen.', '',
              'Las cadenas incluyen identificadores y otros valores técnicos. Una cadena presente o distinta del original no equivale a una traducción correcta; una cadena igual puede ser un nombre propio válido. Las claves anidadas mezclan nombres e IDs y requieren revisión contra documentos originales.', '',
              'El informe local `../export/_data/translation-inventory.json` conserva rutas ausentes, inesperadas y huellas de cada archivo. No se modifica el inventario histórico ni la lista de trabajo existente.', '']
    (ROOT / 'dev-tools/translation/INVENTARIO.md').write_text('\n'.join(lines), encoding='utf-8')
    print('\n'.join(lines[:13]))


if __name__ == '__main__':
    main()
