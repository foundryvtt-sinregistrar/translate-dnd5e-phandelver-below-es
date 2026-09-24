# Fuentes actuales: fase 1

Exportación: `2026-09-24T19-12-21-788Z`.

Foundry 14.368, dnd5e 6.0.3, aventura 3.1.0.

La traducción de Phandelver estaba desactivada. Babele permaneció activo
por dependencias de otros módulos; ningún pack objetivo tenía un mapeo
traducido y ningún documento o carpeta contenía marcas de Babele.
Se conservan documentos completos, IDs originales y SHA-256 por pack.

| Pack | Documentos | IDs añadidos | IDs retirados |
|---|---:|---:|---:|
| pbso-player-tables | 53 | 0 | 0 |
| pbso-player-options | 39 | 0 | 0 |
| pbso-items | 165 | 0 | 0 |
| pbso-bestiary | 148 | 0 | 0 |
| pbso-adventures | 1 | 0 | 0 |

## Adventure: colecciones reales

| Colección | Documentos | Nombres distintos |
|---|---:|---:|
| actors | 163 | 163 |
| items | 253 | 228 |
| journal | 61 | 45 |
| scenes | 35 | 35 |
| tables | 12 | 12 |
| macros | 10 | 10 |
| folders | 71 | 15 |

## Traducción actual por ID

- Carpetas: 71 entradas.
- Diarios: 61 entradas.
- Páginas: 310 entradas.
- Presencia estructural; no equivale a revisión editorial ni prueba de integración.

Páginas de diario: 686.

## Consecuencias para la revisión

- La estabilidad de IDs principales no demuestra que los textos o esquemas sean idénticos.
- El export histórico conservaba 15 claves de carpetas por nombre; los originales completos
  contienen 71 carpetas. Mantener IDs al diseñar el convertidor de carpetas.
- Los 61 diarios tienen títulos repetidos: resolver por ID y contexto las claves antiguas
  antes de reutilizar traducciones. No colapsar atlas o ilustraciones con el mismo nombre.
- Separar objetos independientes de los 253 objetos directos de Adventure y del equipo
  incrustado en actores. Las cifras acumuladas del manifiesto incluyen este equipo.
- El recuento ignora referencias escalares como `Scene.journal`; no son diarios anidados.
- Las actividades y avances proceden de documentos serializados en el entorno actual.
  La migración y aplicación de traducciones se comprobarán en el piloto, no se dan por probadas.

La exportación del primer intento (`2026-09-24T19-11-27-351Z`) se conserva como evidencia
de un error de recuento de referencias de escena; no debe usarse como línea base.
El validador la rechaza. La exportación indicada arriba es la línea base aceptada.

Comandos: `python dev-tools/export/validate_current_export.py` y
`python dev-tools/translation/inventory_current.py`.
