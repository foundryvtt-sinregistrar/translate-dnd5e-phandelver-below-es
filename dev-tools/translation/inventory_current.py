"""Report current original documents and compare IDs with the historical export."""
from collections import Counter
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'dev-tools/export'))
from validate_current_export import BASE, validate


def main():
    candidates = sorted(BASE.glob('*/inventory.json'))
    if not candidates:
        raise SystemExit('No current export; run the Foundry exporter first.')
    directory = candidates[-1].parent
    manifest = validate(directory)
    data = ROOT / 'dev-tools/export/_data'
    historical = json.loads((data / 'source/inventory.json').read_text(encoding='utf-8'))
    old_packs = {p['id']: p for p in historical['packs']}
    lines = ['# Fuentes actuales: fase 1', '',
             f"Exportación: `{directory.name}`.", '',
             'Foundry 14.368, dnd5e 6.0.3, aventura ' + manifest['source']['version'] + '.', '',
             'La traducción de Phandelver estaba desactivada. Babele permaneció activo',
             'por dependencias de otros módulos; ningún pack objetivo tenía un mapeo',
             'traducido y ningún documento o carpeta contenía marcas de Babele.',
             'Se conservan documentos completos, IDs originales y SHA-256 por pack.', '',
             '| Pack | Documentos | IDs añadidos | IDs retirados |', '|---|---:|---:|---:|']
    reports = []
    adventure = None
    for pack in manifest['packs']:
        payload = json.loads((directory / pack['filename']).read_text(encoding='utf-8'))
        current = {d['_id'] for d in payload['documents']}
        old = {d['id'] for d in old_packs[pack['collection']]['documents']}
        report = {'pack': pack['collection'], 'added_ids': sorted(current-old), 'removed_ids': sorted(old-current)}
        reports.append(report)
        lines.append(f"| {pack['collection'].split('.')[-1]} | {len(current)} | {len(current-old)} | {len(old-current)} |")
        if pack['documentType'] == 'Adventure':
            adventure = payload['documents'][0]
    lines += ['', '## Adventure: colecciones reales', '', '| Colección | Documentos | Nombres distintos |', '|---|---:|---:|']
    nested = {}
    for key in ('actors', 'items', 'journal', 'scenes', 'tables', 'macros', 'folders'):
        docs = adventure.get(key, [])
        names = Counter(d.get('name') for d in docs)
        nested[key] = {'count': len(docs), 'distinct_names': len(names),
                       'duplicate_names': {n: c for n, c in names.items() if c > 1}}
        lines.append(f'| {key} | {len(docs)} | {len(names)} |')
    pages = [p for j in adventure['journal'] for p in j['pages']]
    lines += ['', f'Páginas de diario: {len(pages)}.', '',
              '## Consecuencias para la revisión', '',
              '- La estabilidad de IDs principales no demuestra que los textos o esquemas sean idénticos.',
              '- El export histórico conservaba 15 claves de carpetas por nombre; los originales completos',
              '  contienen 71 carpetas. Mantener IDs al diseñar el convertidor de carpetas.',
              '- Los 61 diarios tienen títulos repetidos: resolver por ID y contexto las claves antiguas',
              '  antes de reutilizar traducciones. No colapsar atlas o ilustraciones con el mismo nombre.',
              '- Separar objetos independientes de los 253 objetos directos de Adventure y del equipo',
              '  incrustado en actores. Las cifras acumuladas del manifiesto incluyen este equipo.',
              '- El recuento ignora referencias escalares como `Scene.journal`; no son diarios anidados.',
              '- Las actividades y avances proceden de documentos serializados en el entorno actual.',
              '  La migración y aplicación de traducciones se comprobarán en el piloto, no se dan por probadas.', '',
              'La exportación del primer intento (`2026-09-24T19-11-27-351Z`) se conserva como evidencia',
              'de un error de recuento de referencias de escena; no debe usarse como línea base.',
              'El validador la rechaza. La exportación indicada arriba es la línea base aceptada.', '',
              'Comandos: `python dev-tools/export/validate_current_export.py` y',
              '`python dev-tools/translation/inventory_current.py`.', '']
    report = {'export': directory.name, 'packs': reports, 'nested': nested, 'journal_pages': len(pages)}
    (data / 'source-comparison.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    (ROOT / 'dev-tools/translation/FUENTES-ACTUALES.md').write_text('\n'.join(lines), encoding='utf-8')
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
