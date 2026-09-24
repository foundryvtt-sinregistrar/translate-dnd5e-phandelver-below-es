# Revisión de objetos, bestiario y Adventure

## Inventario inicial del 25 de septiembre de 2026

La fuente sigue siendo la exportación original del 24 de septiembre para Foundry
14.368 y dnd5e 6.0.3. `text_schema.py` amplía el inventario a los textos de
actividades, efectos, objetos incrustados, escenas y deltas de tokens. Detecta
9.568 campos aún sin cubrir: 377 en objetos, 3.227 en bestiario, 5.963 en Adventure
y un requisito de las opciones de personaje.

`prepare_remaining.py` busca coincidencias del texto original en referencias
locales y conserva su procedencia. Las 1.783 coincidencias iniciales son
candidatos de reutilización, no aprobaciones editoriales. `draft_remaining.py`
prepara el resto con el motor OPUS local previamente instalado. Sus resultados
y caché permanecen en `_data`, fuera del módulo y del ZIP. Ninguno de estos
scripts publica automáticamente un borrador en `compendium`.

La inspección del borrador detecta errores como *Drow → Sueño*, términos de
reglas incorrectos y una conversión incorrecta de pintas a litros. Las comprobaciones
de números o enlaces por sí solas no acreditan calidad lingüística ni fidelidad.

## Aplicación segura de textos

`scripts/document-text.mjs` aplica una lista explícita de campos de texto por ID.
Incluye objetos, actores, actividades, efectos, escenas, tablas y nombres de
macros. Conserva los comandos de macros, scripts de regiones, tiradas, pesos,
enlaces, coordenadas, concesiones y demás datos funcionales. Las pruebas incluyen
parches que intentan modificar estos campos protegidos y verifican que no cambian
ni el resultado ni el original de entrada fuera de los textos permitidos.

Validación inicial: 16 pruebas Node correctas. Estos convertidores aún requieren
verificación de su integración en Babele cuando se añadan los mapeos y textos.

La revisión integral sigue abierta. La preparación de borradores y la cobertura
de nombres no equivalen a una revisión completa de descripciones ni de Adventure.
