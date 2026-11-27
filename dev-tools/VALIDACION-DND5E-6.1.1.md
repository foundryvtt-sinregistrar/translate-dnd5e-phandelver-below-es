# Validación de Phandelver con D&D5e 6.1.1

Fecha: 2026-11-27. Rama local: `compat/dnd5e-6.1.1`.

## Entorno y aislamiento

Foundry VTT 14.370, dnd5e 6.1.1, Babele 2.9.1, producto oficial 3.1.0 y
traducción 1.14.3 con los cambios locales de esta rama. Idioma: español.
Se usó el importador nativo en el mundo `qa-dnd5e611-adventures`, copia de
`dnd5e-606` realizada con el original detenido. Antes de importar no había
colisiones de IDs. El original no recibió las importaciones.

## Resultado de importación y persistencia

| Tipo | Esperados | Importados y conservados tras recargar |
| --- | ---: | ---: |
| Actores | 163 | 163 |
| Objetos | 253 | 253 |
| Diarios | 61 | 61 |
| Escenas | 35 | 35 |
| Tablas | 12 | 12 |
| Macros | 10 | 10 |
| Carpetas | 71 | 71 |

Sin documentos ausentes, errores de esquema, diferencias de nombres guardados,
etiquetas de ficha alteradas o actores de ficha sin destino. Los nombres
mostrados para objetos no identificados difieren legítimamente de su nombre
identificado; se compararon los datos persistidos de `toObject()`.

Se importó todo sin conversión opcional a monstruos ni conjuros 2024. Para
repetir la prueba del arreglo se retiraron solo los actores y escenas de esta
aventura en QA; el importador volvió a crearlos y actualizó el resto de sus
documentos. El original y sus IDs de base quedaron fuera de la limpieza.

Comparados 6.725 campos de texto contra el Adventure traducido antes de
importar: 71 normalizaciones de HTML y cuatro campos de efectos de fichas
vinculadas que Foundry conserva en el Actor base. Los efectos Inconsciente e
Invisible siguen presentes. La descripción base de Invisible conserva su
`@Embed` a las reglas del sistema, cuyo destino resuelve; no se reemplaza por
la descripción redundante del ActorDelta descartado. No hay otras diferencias.

Se abrió el diario Bienvenido a Phandalin y la escena inicial traducida. Los
recursos de imagen comprobados de Guarida de los Redbrand y Klarg devolvieron
HTTP 200. Esto es una muestra visual, no una revisión de todas las imágenes.

## Corrección de nombres de fichas

La primera importación reprodujo 45 etiquetas sustituidas por la sincronización
asíncrona de Babele, por ejemplo Mirna Dendrar → Plebeyo. `importAdventure`
dispara escrituras de Token sin esperarlas; durante `postImport` el nombre
todavía puede coincidir con el original y la restauración anterior lo omite.
Incluso sin esa condición, Foundry descarta actualizaciones sin diferencias.

El cambio mínimo en `scripts/adventure-import.mjs` escribe los nombres
originales de todas las fichas conocidas en las escenas importadas, usando
`updateEmbeddedDocuments` con `diff:false`. Solo escribe `_id` y `name`.
Conserva las restricciones existentes por aventura e idioma. Tras recrear
actores y escenas, reimportar mediante la interfaz y recargar, quedan cero
etiquetas distintas del Adventure traducido.

## Referencias y límites

Comprobadas 1.404 referencias distintas mediante `fromUuid`: nueve no resuelven
y coinciden con las nueve incidencias de la fuente ya documentadas en
[el informe anterior](translation/INFORME-REVISION.md). No hay notas de mapa
sin destino. No se presenta la aventura como libre de erratas del original.

Pruebas locales: 20 Node, 24 Python de construcción y 14 Python de herramientas
de traducción; todas superadas. La regresión nueva reproduce una sincronización
pendiente cuando el nombre actual aún coincide y exige `diff:false`.

La evidencia privada está en `export/_data/qa-611-import.json`,
`qa-611-field-diff.json` y `qa-611-references.json`, excluidos de Git.
No se distribuyen los documentos premium ni sus instantáneas.

## Reanudación

- Importación completa y persistencia: PASS, con las excepciones heredadas indicadas.
- `verified` pasa a 6.1.1; la versión publicada no cambia.
- Los documentos importados permanecen en la copia QA para revisión.
- No se han probado todas las automatizaciones de juego ni las conversiones opcionales 2024.
- Validación preparada para integración local en main; sin push, tag ni release.
