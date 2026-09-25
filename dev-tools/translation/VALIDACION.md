# Validación de la revisión

Cierre: 25 de septiembre de 2026. Véase el [informe](INFORME-REVISION.md).

## Comprobaciones locales

Desde la raíz del proyecto, con Python 3 y Node disponibles:

```powershell
python dev-tools/export/validate_current_export.py
python -m unittest discover -s dev-tools/translation -p test_*.py
node --test dev-tools/export/test-export.mjs dev-tools/translation/test-registration.mjs dev-tools/translation/test-item-text.mjs dev-tools/translation/test-adventure-text.mjs dev-tools/translation/test-document-text.mjs dev-tools/translation/test-adventure-import.mjs
python dev-tools/translation/check_reviewed.py
python dev-tools/translation/audit_integral.py
python dev-tools/translation/audit_current.py
python dev-tools/translation/audit_runtime.py
python dev-tools/translation/audit_import.py
```

Resultados: 19 pruebas Node, 14 Python; 10.855 campos cubiertos; cero errores
de evidencia, números, monedas, HTML o sintaxis técnica. La auditoría de salida
Babele acredita cero cambios fuera de campos de texto y metadatos permitidos.

## Foundry

Entorno probado: 14.368 / dnd5e 6.0.3 / PBSO 3.1.0 / Babele local 2.9.1.
Con sesión GM, el validador puede ejecutarse desde una macro Script:

```javascript
const {validateRuntime} = await import("/modules/translate-dnd5e-phandelver-below-es/dev-tools/translation/validate-runtime.mjs");
await validateRuntime({pilot:false});
```

Valida los 406 documentos y guarda salida e informe en `export/_data/`.
No sustituye una importación. La prueba integral se realizó en el mundo de
desarrollo, con preflight de IDs sin colisiones, sin conversión opcional a 2024.
No ejecutar una nueva importación sobre una campaña con cambios sin revisarlos.

Tras importar mediante la interfaz:

```javascript
const {validateImport} = await import("/modules/translate-dnd5e-phandelver-below-es/dev-tools/translation/validate-import.mjs");
await validateImport();
```

Después ejecutar `audit_import.py`. Compara los 6.715 campos de documentos
del mundo con el resultado traducido esperado. Solo admite normalizaciones
HTML precisas y efectos de tokens vinculados presentes en el actor base.
Clasifica los UUID no resueltos contra el original; una referencia nueva sin
destino hace fallar la auditoría.

Resultado: cero documentos ausentes, cero diferencias pendientes, 1.404
referencias comprobadas y nueve no resueltas ya presentes en el original.
Los detalles están en `import-audit.json`.

## Distribución

```powershell
python dev-tools/buildScripts/build_release.py --ref HEAD
```

Requiere árbol limpio. Verifica miembros permitidos, rutas, JSON y manifiesto
del mismo commit. Los originales, PDF, OCR y herramientas quedan excluidos.
Extraer el ZIP en `dist/install-check/` permite comprobar recursos e imports
relativos. No equivale a instalarlo mediante el gestor de Foundry ni a probar
una compilación independiente de Babele.
