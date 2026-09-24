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
  resuelven. `compendium/`, `lang/`, `scripts/` y `module.json` no han cambiado.
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
Todavía no se ha ejecutado el piloto ni la validación de runtime de Tomb adaptada
a este módulo; no se heredan sus resultados.
