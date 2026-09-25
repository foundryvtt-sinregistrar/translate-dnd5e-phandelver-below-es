# Roadmap de revisión de Phandelver & Below

Actualizado: 25 de septiembre de 2026. Rama: `feature/dnd5e-6.0.3`.

**Revisión editorial terminada e importación integral comprobada.**
Se ha seguido el proceso de Tomb of Annihilation: referencias, fuentes actuales,
mapeos, glosario, piloto, lotes y auditoría. Resultado y límites en el
[informe final](translation/INFORME-REVISION.md).

| Fase | Resultado | Estado |
|---|---|---|
| 0. Referencias | PDF EN 225 + ES 204 páginas; extracción, OCR, bloques y huellas locales | Completada; OCR auxiliar, no transcripción certificada |
| 1. Fuentes actuales | Cinco packs, 406 documentos, exportación sin traducción en 14.368 / 6.0.3 | Completada |
| 2. Mapeos | IDs y campos de texto, actividades, avances, efectos, ActorDelta y copias | Completada; cero alteraciones protegidas |
| 3. Glosario | Nombres y términos unificados entre packs, índices y Adventure | Completada |
| 4. Piloto | Diarios y opciones importados; pruebas ampliadas a todos los tipos | Completada dentro de la validación integral |
| 5. Lotes editoriales | Objetos 165, bestiario 148, opciones 39, tablas 53; 521 textos de Adventure | Completada |
| 6. Auditoría integral | 10.855 campos; importación completa; 6.715 campos del mundo comprobados | Completada con nueve referencias heredadas documentadas |
| 7. Preparación de distribución | README, changelog, compatibilidad, ZIP y exclusión de fuentes privadas | Preparada; instalación independiente y publicación fuera del cierre editorial |

## Lotes cerrados

- Tablas de jugador y opciones de personaje.
- Objetos y sus variantes dentro de Adventure.
- Bestiario: 918 originales de prosa distintos y sus copias.
- Adventure: 214 textos exclusivos, índice de actores, títulos, pies,
  escenas, notas, fichas, carpetas, macros y tablas.
- Legado: 309 páginas leídas y contrastadas, desde la introducción hasta
  el capítulo 8; [detalle por lotes](translation/LOTE-ADVENTURE-LEGADO.md).
- Pasada final de terminología, unidades, monedas, atributos HTML y coherencia.
- Prueba real de importación: 163 actores, 253 objetos, 61 diarios, 35 escenas,
  12 tablas, 10 macros y 71 carpetas. Corrección de 45 nombres de fichas
  sustituidos por la sincronización de Babele.

## Criterios de cierre y excepciones

Los destinos UUID, fórmulas, comandos, imágenes, geometría y mecánicas se
conservan. Las nueve referencias no resueltas ya existen en el original y se
enumeran en el informe. Los efectos de dos tokens vinculados se verifican
en sus actores base después de la normalización de Foundry.

La versión local de Babele 2.9.1 incluye un registro moderno de convertidores.
La validación acredita ese entorno; no una instalación limpia de otra
compilación. La extracción aislada del ZIP comprueba su integridad, sin
confundirla con una instalación mediante el gestor de Foundry.

No quedan lotes editoriales abiertos en este alcance. Una futura publicación
requiere elegir versión/tag y validar el entorno de distribución independiente.
No se ha solicitado ni ejecutado push o release.

## Seguimiento reproducible

[Estado](translation/ESTADO-TRADUCCION.md) ·
[Fuentes](translation/FUENTES-ACTUALES.md) ·
[Glosario](translation/GLOSARIO.md) ·
[Validación](translation/VALIDACION.md) ·
[Extracción PDF](export/README.md).

Se conservan el diagnóstico y la lista de revisión históricos. No se
sobrescriben para hacerlos pasar por evidencia de la revisión actual.
