# Validación

## Comprobado en esta preparación

- El validador existente acepta los IDs principales de los cinco packs históricos:
  53 tablas, 39 opciones, 165 objetos, 148 actores y una aventura.
- El inventario compara claves y rutas con la traducción y calcula SHA-256.
- La extracción PDF registra cobertura, métodos, versiones y páginas dudosas.
  `status: complete` y `errors: []` prueban finalización, no exactitud del OCR.
- Resultado final: EN 225/225 y ES 204/204, todas con OCR, sin errores de
  procesamiento. Hay 25 páginas inglesas y 19 españolas señaladas para revisión.
  Se verificaron las 429 filas JSONL contra los textos por página, la presencia
  de originales y bloques, los TSV comprimidos y los SHA-256 de ambos PDF.
- Los ocho JSON de compendios, idiomas y manifiesto son válidos; los dos scripts
  nuevos pasan el análisis de sintaxis y los enlaces locales de documentación
  resuelven. Posteriormente se migraron claves y se corrigió el registro de Babele.
- Las referencias y datos privados se mantienen bajo `_data`, excluido de Git.

## Controles pendientes antes de cerrar la revisión

La fase 1 se cerró con la exportación `2026-09-24T19-12-21-788Z`: cinco hashes
correctos, 406 documentos, IDs principales sin cambios, IDs anidados comprobados,
61 diarios, 686 páginas y 71 carpetas internas. El exportador rechazó en ejecución
la traducción activa antes de escribir fuentes. Cuatro pruebas Node cubren marcas
anidadas, IDs por colección, referencias de efectos y referencias de diarios en escenas.
La primera exportación con el error de recuento se conserva y es rechazada por
el validador. Esto no certifica todavía los mapeos ni la traducción.

- Mantener la línea base de originales validada al actualizar versiones.
- Cobertura de campos visibles, sin confundir hojas técnicas con texto traducible.
- HTML, enlaces `@UUID`, `@Embed`, tiradas, parámetros y etiquetas intactos.
- Números, unidades y reglas fieles al original; nombres y terminología consistentes.
- Scripts, fórmulas, geometría, rutas de imágenes y mecánicas sin cambios accidentales.
- Esquemas actuales de Foundry/dnd5e y convertidores Babele probados.
- Compendio directo y copia importada; actores con objetos, actividades y efectos;
  escenas con notas, tokens y ActorDelta; tablas, carpetas e interfaz.
- Prueba en español e inglés; una variante regional de español cuando corresponda.
- Importación completa en mundo limpio, sin sobrescribir el mundo existente.
- ZIP instalado y revisado; fuentes, PDF, OCR y herramientas fuera de la distribución.

Registrar cada prueba con fecha, versiones, documento, resultado e incidencia.
## Integración ejecutada el 24 de septiembre de 2026

`validate-runtime.mjs` procesó los 406 documentos con Babele 2.9.1, Foundry
14.368 y dnd5e 6.0.3: cero errores de aplicación y validación estricta del
esquema. Comprueba los nombres, carpetas, páginas y resultados de tablas
presentes en el payload; los packs sin traducción también pasan el esquema,
pero esto no los convierte en contenido traducido.

El piloto creó el diario «Bienvenido a Phandalin» en «Phandelver - Revision»
y comprobó que el texto importado coincide con el payload. Se abrió su hoja
y se observaron los títulos españoles. No se importó la aventura completa.
El informe detallado local está en `../export/_data/runtime-validation.json`.

La primera ejecución detectó convertidores sin registrar. El módulo de entrada
ahora importa explícitamente `converters.js`; tras recargar, la prueba pasó.
Las once pruebas Node del exportador, registro y conversores también pasan.

La ejecución posterior a las correcciones de presentación e interfaz volvió
a validar 406 documentos sin errores. `audit_runtime.py` comparó la salida
Babele sin normalizaciones del constructor de Foundry: 4901 campos de texto
cambiados y cero diferencias fuera de las rutas permitidas y metadatos Babele.
El informe registra los módulos activos porque parte del resultado procede de
sus traducciones de respaldo, no del payload de este proyecto.

Las 31 cadenas de interfaz conservan claves, parámetros y etiquetas HTML del
original instalado. Las opciones de importación se observaron en español.
El ZIP se comprobó con lista permitida de miembros y JSON válido; una prueba
aislada confirmó que construir una referencia anterior usa su versión y su
manifiesto, excluye datos privados y rechaza un tag incoherente con la versión.
