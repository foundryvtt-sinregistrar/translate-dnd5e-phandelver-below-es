# Referencias PDF y exportaciones de Phandelver

Se adopta la estructura de Tomb of Annihilation manteniendo la carpeta privada
existente **`_data/`**, sin mover ni sobrescribir las extracciones históricas.
Los PDF, las fuentes y las extracciones no se distribuyen ni se añaden a Git.

## Estructura

```text
export/
  prepare_pdf_references.py
  _data/
    pdf/                         # PDF originales y extracción histórica
    source/                      # exportación histórica de Foundry
    source-current/<fecha>/       # documentos originales actuales y manifiesto
    adventure-worklist.csv       # lista histórica; conservar su progreso
    translation-inventory.json   # diagnóstico regenerable
    references/
      manifest.json
      en/
        manifest.json
        bookmarks.json
        text.txt
        pages.jsonl
        pages/
          0001.txt
          0001.native.txt
          0001.blocks.json
          0001.json
          0001.tsv.gz
      es/                        # misma estructura
      qa/                        # muestras visuales locales
```

- `text.txt`: texto completo con separadores `PDF PAGE`.
- `pages/NNNN.txt`: texto seleccionado de la página física, en UTF-8.
- `pages.jsonl`: texto y métricas de cada página, en orden.
- `*.native.txt`: capa de texto original, conservada para contraste.
- `*.blocks.json`: bloques nativos y coordenadas; no son los bloques del OCR.
- `*.tsv.gz`: palabras, coordenadas y confianza del OCR a 300 ppp.
- `*.json`: método, firma de caché, recuentos y señales de revisión por página.
- `bookmarks.json`: marcadores disponibles; puede estar vacío.
- Manifiestos: fuente, idioma, SHA-256, herramientas, modelos, cobertura,
  errores, páginas con OCR y páginas que requieren revisión (`review_pages`).

## Fuentes y límites

La fuente inglesa `Phandelver and Below The Shattered Obelisk pdf.pdf` tiene
225 páginas físicas. La española `Phandelver y Más Allá - El Obelisco
Despedazado.pdf` tiene 204. **No hay alineación automática entre idiomas.**
No se ha comprobado la integridad editorial ni el carácter oficial del PDF español.

La capa nativa inglesa contiene palabras pegadas, encabezados omitidos y ruido
en el índice. La española tiene muchas páginas sin texto nativo. Se usa OCR en
ambos libros completos y se conserva la capa original, siguiendo la práctica
de Tomb cuando una capa aparentemente extraíble resulta poco fiable.

La extracción es una referencia automática. El OCR puede omitir capitulares,
mezclar columnas, confundir símbolos y alterar cifras o tablas. `review_pages`
señala páginas con menos de 20 palabras, caracteres dañados o confianza media
inferior a 75; no detecta todos los errores. Mapas e ilustraciones también pueden
aparecer en esa lista. Cotejar cualquier fragmento dudoso con el PDF visible.

Muestras contrastadas visualmente durante la preparación:

- EN, página física 5: índice de tres columnas. El OCR mejora las palabras
  pegadas, pero aún mezcla algunas entradas y cifras. Usar la imagen del índice
  para los inicios de capítulos recogidos en el roadmap.
- EN, página física 7 (impresa 5): el OCR omite la capitular inicial y parte del
  título ornamental; el cuerpo resulta consultable. No copiarlo sin cotejo.
- ES, página física 100 (impresa 101): texto en dos columnas con recuadro.
  El OCR recupera el cuerpo, pero lee `T13` como `113` e intercala el pie de página.
- ES, página física 204: contraportada, no una página narrativa de la aventura.

Estas observaciones son incidencias conocidas incluso si la confianza media no
activa `review_pages`. No se ha revisado visualmente cada una de las 429 páginas.

Las referencias a `0005.txt` usan posiciones físicas desde 1, no numeración
impresa. El roadmap recoge inicios impresos del índice inglés verificado
visualmente; localizar cada correspondencia española por encabezado y contexto.

## Consulta

Desde la raíz del módulo:

```powershell
rg -n -i 'Phandalin|Ilvaash|Talhundereth' dev-tools/export/_data/references/en/pages dev-tools/export/_data/references/es/pages -g '*.txt' -g '!*.native.txt'
Get-Content dev-tools/export/_data/references/en/pages/0007.txt -Encoding UTF8
Get-Content dev-tools/export/_data/references/es/manifest.json -Encoding UTF8
```

Buscar el original inglés, contrastar la referencia española y trasladar solo
el texto revisado a los campos de Foundry. Conservar IDs, UUID, etiquetas,
fórmulas y recursos del módulo; el PDF no sustituye la estructura del compendio.

## Regeneración

Requiere Python 3.11 o posterior, PyMuPDF, Tesseract y modelos `eng` y `spa`.
Se usa la dependencia local `dev-tools/.python`, los modelos de
`dev-tools/.tessdata` y `C:/Program Files/Tesseract-OCR/tesseract.exe`.

```powershell
python -m pip install --target dev-tools/.python pymupdf
python dev-tools/export/prepare_pdf_references.py --ocr-all en es
```

Admite `--workers 4` y `--tessdata RUTA`. La caché por página se invalida al
cambiar PDF, script, herramientas, modelos u opción de OCR. El acceso a PyMuPDF
se serializa; solo el trabajo de OCR se ejecuta simultáneamente. Reanudar con el
mismo comando. Comprobar que **ambos** manifiestos indican `status: complete`,
`completed_pages == page_count` y `errors: []`.

Resultado verificado el 24 de septiembre de 2026: EN 225/225, ES 204/204,
OCR en las 429 páginas y cero errores de procesamiento. Los manifiestos señalan
25 páginas inglesas y 19 españolas para revisión adicional.

`extract_pdf_text.py`, `ocr_pdf.py` y los archivos `pdf/extracted-pages.json` y
`pdf/ocr-pages.json` se conservan como herramientas/datos históricos. Para la
revisión nueva se consulta `references/`; no se mezclan sus numeraciones o estados.

## Fuentes de Foundry

La exportación actual se conserva en `_data/source/`. Validación e inventario:

```powershell
python dev-tools/export/validate_source_export.py
python dev-tools/translation/inventory.py
```

### Exportación actual (Foundry 14.368 / dnd5e 6.0.3)

`export-source.js` ahora carga `export-compendiums.mjs`. Ejecutar como GM desde
una macro Script, con la aventura oficial activa y la traducción de Phandelver
desactivada tras recargar. No es necesario cambiar el idioma del mundo.

```js
const {exportCompendiums} = await import("/modules/translate-dnd5e-phandelver-below-es/dev-tools/export/export-compendiums.mjs");
await exportCompendiums();
```

Se requiere la carpeta local `_data/source-current/` (crear si no existe).
Cada ejecución crea una subcarpeta fechada y escribe cinco `*.en.json` con los
documentos completos; `inventory.json` se escribe al final. No usa extracción
Babele, no modifica los packs oficiales y conserva `_data/source/`.
Rechaza versiones distintas de las del entorno de revisión, IDs ausentes o
duplicados, marcas de traducción y mapeos de packs ya traducidos.

Babele puede seguir activo por dependencias: se comprueban los cinco packs y
sus documentos. Eso no equivale a desactivar todas las traducciones del mundo.
Restaurar el módulo de Phandelver y recargar al terminar.

```powershell
python dev-tools/export/validate_current_export.py
python dev-tools/translation/inventory_current.py
node --test dev-tools/export/test-export.mjs
```

El validador selecciona la última exportación con manifiesto, o acepta una ruta
explícita. Comprueba SHA-256, tipos, versiones, IDs anidados, marcas y recuentos.
No demuestra por sí solo fidelidad editorial o compatibilidad de las traducciones.
La línea base aceptada es `source-current/2026-09-24T19-12-21-788Z/`.
Consultar [el informe de fuentes actuales](../translation/FUENTES-ACTUALES.md).
