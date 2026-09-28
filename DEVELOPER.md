# Guía de desarrollo

Proyecto: `translate-dnd5e-phandelver-below-es`, versión de trabajo **1.14.2**. Instalación: [README.md](README.md) y [README.en.md](README.en.md).

## Entorno y compatibilidad

`module.json` es la referencia de identidad, requisitos, versión y entradas de ejecución. Ambos README reproducen sus mínimos y versiones verificadas. CI utiliza Ubuntu, Node 24 y Python 3.11. Las comprobaciones locales de homogeneización usan Node 24.17.0 y Python 3.14.6; no constituyen una matriz exhaustiva.

## Preparación y edición

Parte de `develop` tras comprobar su relación con `main` y sus remotos. Conserva cambios locales ajenos; no fuerces referencias ni reutilices etiquetas publicadas. Registra las adaptaciones en [ADOPCION.md](dev-tools/homogeneizacion/ADOPCION.md).

`.editorconfig` define UTF-8, LF, dos espacios para JSON/YAML y cuatro para JS/Python; conserva espacios finales de Markdown. `.gitattributes` normaliza en Git y controla la exportación. No reformatees masivamente traducciones. Conserva IDs, UUID, claves, fórmulas, números mecánicos, rutas y estructura HTML; traduce solo los textos previstos por mappings y convertidores.

## Estructura y registro

- `compendium/`: 5 JSON de traducción Babele.
- `lang/`: archivos declarados en el manifiesto.
- `scripts/`: registro, convertidores y comportamiento específico del módulo.
- `tests/`: comprobaciones portables y del constructor; no se distribuyen.
- `dev-tools/`: fuentes de desarrollo, auditorías, perfil y herramientas; no se distribuye.
- `dist/`: artefactos generados, ignorados por Git.

El registro utiliza `babele.init` y espera a `setup` para leer `core.language`; aplica español y variantes regionales. Los documentos ya importados no se sincronizan automáticamente.

Convertidores registrados: `phandelverFoldersById`, `phandelverJournalsById`, `phandelverAdvancementNames`, `converters`.

## Fuentes y particularidades

Se conservan exportador, importación Adventure, mappings y auditorías específicos. El constructor incorpora el contrato común de PHB en su ruta existente. Las suites adicionales siguen en `dev-tools/export/` y `dev-tools/translation/`; las pruebas que requieren originales se omiten explícitamente en un clon sin ellos. Consulta `dev-tools/translation/INFORME-REVISION.md` para la evidencia editorial y de importación previa.

Las fuentes completas, PDF, OCR, modelos y exportaciones del producto oficial son locales. No copies sus bases de datos al paquete ni las añadas al índice. Versiona únicamente las herramientas, mappings y evidencias que corresponda compartir.

- [dev-tools/export/README.md](dev-tools/export/README.md).
- [dev-tools/translation/README.md](dev-tools/translation/README.md).
- [dev-tools/translation/INFORME-REVISION.md](dev-tools/translation/INFORME-REVISION.md).
- [dev-tools/translation/ESTADO-TRADUCCION.md](dev-tools/translation/ESTADO-TRADUCCION.md).

## Validación portable

Desde la raíz del proyecto:

```sh
node --test dev-tools/export/test-export.mjs dev-tools/translation/test-*.mjs
python -B -m unittest discover -s tests -p 'test_*.py' -v
python -B -m unittest discover -s dev-tools/translation -p 'test_*.py' -v
git diff --check
```

Comprueba también un clon aislado: los módulos hermanos y las fuentes privadas del workspace pueden ocultar dependencias. Las omisiones por fuentes ausentes deben aparecer en el resultado y no equivalen a pruebas superadas. No ejecutes generadores como parte de la validación.

Para pruebas funcionales, registra versiones de Foundry, dnd5e, Babele y producto oficial; abre e importa documentos representativos en un mundo de prueba. Revisa enlaces, imágenes, tablas y automatizaciones. No declares una verificación completa basándote solo en JSON válido o cobertura de traducción.

## Construcción

Con el árbol limpio y los cambios confirmados:

```sh
python -B dev-tools/buildScripts/build_release.py --dist dist --ref HEAD
```

El constructor lee manifiesto, perfil y contenido del mismo commit. Genera un ZIP versionado, `translate-dnd5e-phandelver-below-es.zip`, `module.json` y `SHA256SUMS.txt`; el manifiesto externo es idéntico al del ZIP. Comprueba JSON, rutas, documentos obligatorios y lista de admitidos antes de sustituir salidas existentes. `--allow-dirty` permite inspeccionar contenido confirmado sin incorporar cambios locales.

`dev-tools/buildScripts/release-profile.json` declara el nombre del ZIP, el canal `latest` y la variante `standard`. En modo release, `--ref vVERSION` o `--ref SHA --release-tag vVERSION` exige correspondencia de tag, commit, versión, changelog y URLs. Los hashes cubren ambos ZIP y el manifiesto. Pruebas, herramientas, contadores, fuentes privadas y archivos de IDE quedan fuera del paquete.

## CI y publicación

`validate.yml` ejecuta las suites y construye el commit de la ejecución en PR y pushes a ramas. `release.yml` llama a esa misma validación al subir tags `v*`, descarga sus artefactos y comprueba hashes antes de crear el borrador. Solo el job publicador recibe permiso de escritura. No basta con tener workflows locales: hay que comprobar su ejecución en GitHub después del push y configurar por separado las protecciones de rama.

Prepara una versión nueva: actualiza versión y URL de descarga en `module.json`, ambos README y CHANGELOG. Conserva las etiquetas anteriores y traslada `[Unreleased]` a la versión fechada. Valida el commit en la rama de preparación y etiqueta ese commit, sin adelantar `main`. Revisa y publica los adjuntos, comprueba sus URLs y solo después integra el contenido publicado en `main`. Las instalaciones antiguas pueden seguir consultando el manifiesto de main; prueba también su actualización al canal elegido.

El canal estable `latest` necesita el adjunto `module.json` de una release estable. DM conserva expresamente su canal preliminar y manifiesto en main. Estos cambios locales no publican archivos, no alteran releases antiguas y no autorizan a reutilizar la versión actual para otra publicación.

## Etiquetas históricas

No se detectaron discrepancias de versión en las etiquetas locales consultadas.

Esta comparación corresponde a Git local, no certifica los artefactos publicados. Las discrepancias se conservan para trazabilidad; prepara una etiqueta nueva y coherente en la siguiente publicación.

## Diagnóstico

Si aparece inglés, revisa dependencias activas, idioma y recarga. Si solo falla una copia importada, compárala con el compendio actual. Si falla el build por árbol sucio, confirma los cambios o utiliza `--allow-dirty` únicamente para una inspección del commit. Si falla un contrato de tag o URL, corrige una nueva versión; no reescribas un tag publicado.
