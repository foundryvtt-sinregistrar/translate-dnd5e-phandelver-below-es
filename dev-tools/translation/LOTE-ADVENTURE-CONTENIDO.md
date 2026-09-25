# Contenido exclusivo de Adventure

## Índice de actores

Los 155 cuerpos de página quedan cubiertos. Las biografías proceden de textos
revisados completos, con sus evidencias SHA verificadas. Se admite únicamente la
equivalencia HTML `<hr>`/`<hr />`, además de la normalización técnica ya existente.
Las biografías vacías permanecen vacías; sus referencias sí se traducen. Remorhaz
usa su biografía completa sin sección envolvente. Las etiquetas de enlaces solo
se traducen si constan en el diccionario revisado. Cinco pruebas cubren las
variantes admitidas, las ambigüedades y el rechazo de texto desconocido.

## Originales exclusivos 0001–0150

El índice estable contiene 214 originales únicos inicialmente pendientes. Se
revisan los primeros 150, que abarcan encuentros, tesoros, efectos, objetos de
equipo, contenedores, descripciones breves y la biografía específica de Sildar.
La aplicación se limita a campos pendientes o ya propiedad de este lote.

Cobertura: **6.655/6.718** campos de Adventure; quedan **63**. Las tablas conservan
fórmulas, enlaces e identificadores, y los comandos de objetos mantienen sus
nombres originales. Se conservan también los enlaces antiguos `@Compendium`.
No se corrigen destinos de enlace dudosos sin verificarlos en Foundry.

Se ajusta el control de números para reconocer millares seguidos directamente de
moneda (`1,250gp` frente a `1.250 po`). Dos pruebas verifican esa equivalencia y
el rechazo de importes distintos, además de dados, alcances y decimales.

Cero errores en `check_reviewed.py`. Validación integral de Foundry pendiente.

## Cierre de cobertura: originales 0151–0214

Adventure alcanza **6.718/6.718 campos**, incluidas las 521 páginas con texto
original. Los 214 originales pendientes quedan resueltos: 213 mediante los
lotes de prosa y 0174 mediante la composición verificada del índice de actores.
Se completan ayudas, créditos, encuentros, capítulo 8 y cambios oficiales.
El historial 0214 se compone a partir de 138 apartados revisados, conservando
literalmente UUID y enlaces a incidencias.

Se corrige el cierre mal formado de `Reference[total-cover]` del Mordisco del
gusano púrpura. La excepción se limita a ese defecto exacto y las pruebas
siguen rechazando cambios en daño o cobertura. También se preservan destinos
UUID exactos cuando dos packs contienen el mismo ID: la adaptación entre packs
rechaza destinos ambiguos en lugar de sustituir uno por otro.

El acertijo de Valsyx se adapta al español manteniendo la secuencia de palabras
que permite resolverlo. Se conserva el contenido de las notas oficiales de
cambios como registro histórico, no como descripción del estado actual.

La cobertura completa no cierra por sí sola la revisión integral: quedan la
auditoría editorial del texto heredado y la validación de esta versión en Foundry.
