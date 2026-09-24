# Informe de revisión de Phandelver

Fecha: 24 de septiembre de 2026. Rama: `feature/dnd5e-6.0.3`.

## Resultado

La revisión técnica del contenido existente ha permitido corregir el registro
y la carga de convertidores, eliminar ambigüedades de identidad y completar la
presentación e interfaz del módulo. La aplicación de los cinco packs supera la
validación en Foundry **14.368**, dnd5e **6.0.3**, Babele **2.9.1** y aventura
oficial **3.1.0**.

**La revisión integral del roadmap no está terminada y la traducción sigue
siendo parcial.** Este informe no certifica una lectura editorial completa,
importación integral ni instalación de una versión publicada. No se eleva
`compatibility.verified` hasta completar esas pruebas.

## Cambios realizados

- Registro español con `babele.init`/`setup`, incluidas variantes regionales.
- Diarios, páginas y carpetas migrados a IDs; resolución independiente de
  entradas con nombres repetidos. Convertidores limitados a campos de texto.
- Importación explícita de convertidores desde el módulo de entrada, corrigiendo
  el fallo detectado en la primera ejecución de Foundry.
- Descripción de Adventure, pie de imagen y pie de portada traducidos.
- Las 31 cadenas de interfaz PBSO traducidas, conservando todos los parámetros
  de sustitución y etiquetas HTML.
- Auditoría reproducible de cobertura, sintaxis Foundry, atributos HTML y cifras;
  comparación completa de resultados de Babele con los originales.
- Generación del ZIP y manifiesto desde el mismo commit; validación de miembros,
  rutas, JSON y correspondencia de versión del tag. El workflow utiliza el
  manifiesto generado y pasa la referencia mediante una variable de entorno.

## Cobertura comprobada

| Contenido propio del proyecto | Resultado |
|---|---:|
| Tablas de jugador | 53/53 entradas; 374 resultados |
| Opciones de jugador | 39/39 entradas; 32 descripciones y 25 nombres de avances |
| Objetos | 0/165 entradas |
| Bestiario | 0/148 entradas |
| Carpetas de Adventure | 71/71 nombres |
| Diarios de Adventure | 61/61 nombres |
| Páginas con alguna traducción | 310/686 |
| Páginas con texto traducido | 309/521 con texto original |
| Textos pendientes | 212 |
| Interfaz propia PBSO | 31/31 claves |

La presencia de una entrada no significa que todos sus campos estén traducidos
o que la prosa esté revisada. Las páginas restantes incluyen ilustraciones.
La [cobertura por diario](COBERTURA-ACTUAL.md) permite localizar los huecos sin
confundir páginas de imagen con textos narrativos.

## Evidencia de validación

1. Trece pruebas Node superadas: pureza y recuentos de exportación, idioma y
   conservación de estructura al aplicar convertidores sobre originales reales.
2. Runtime: 406 documentos procesados y validados con esquema estricto, cero
   errores. Comprueba los campos presentes en los payloads contra su resultado.
3. Diario «Bienvenido a Phandalin» creado en «Phandelver - Revision», texto piloto
   contrastado y hoja abierta. Presentación y opciones de importación observadas
   en español. No se importó la aventura completa.
4. Comparación de salida Babele: campos de texto traducidos y cero cambios
   fuera de las rutas de texto permitidas y metadatos Babele. Las cantidades
   incluyen traducciones de respaldo de otros módulos activos. Su lista queda
   registrada en el informe local; no son cobertura propia de Phandelver.
5. Auditoría estática: cero diferencias en las expresiones Foundry reconocidas.
   Un aviso de atributos HTML corresponde a cinco etiquetas de monedas
   traducidas. De 106 avisos numéricos tras normalizar separadores, seis están
   contrastados y documentados; cien páginas con unidades siguen pendientes.
   Véase [revisión numérica](REVISION-NUMERICA.md).
6. ZIP comprobado con lista permitida de miembros. Sin PDF, OCR, originales,
   herramientas ni configuración de GitHub. Se generan ZIP versionado, ZIP
   estable y `dist/module.json`; no se han publicado ni instalado.
   Una prueba aislada con dos commits confirmó la selección del manifiesto de
   una referencia anterior y el rechazo de un tag con versión incoherente.

Los informes detallados se guardan localmente en `../export/_data/`:
`runtime-validation.json`, `runtime-diff.json` y `translation-audit.json`.
Las fuentes se mantienen en `source-current/2026-09-24T19-12-21-788Z`.
Los originales y PDF no se incorporan a Git ni a la distribución.

## Pendientes para cerrar el roadmap

| Prioridad | Pendiente | Criterio de cierre |
|---|---|---|
| Alta | Objetos y bestiario sin payload propio | Traducir por ID y validar actividades, avances, efectos y copias de Adventure |
| Alta | 212 textos y títulos/pies de imagen ausentes | Completar por lotes con evidencia EN/ES y revisión contextual |
| Alta | Revisión editorial de la prosa existente | Leer cada lote; resolver terminología, omisiones y conversiones numéricas |
| Alta | Piloto de actor, tabla y escena; concesiones de trasfondos | Apertura e importación, notas, tokens, ActorDelta y aplicación a un personaje comprobados |
| Alta | Importación completa en mundo limpio | Verificar referencias, tiradas, imágenes y copias sin sobrescribir una campaña |
| Media | Glosario | Resolver divergencia «Cueva del Oleaje» / «Cueva del Eco de las Olas» y extender la concordancia |
| Media | Instalación del ZIP | Probar paquete instalado; ajustar compatibilidad y preparar versión cuando proceda |

El PDF español es una referencia de contraste, no una autoridad acreditada.
Sus títulos y extensión difieren del original; no se sustituyen textos por OCR
sin verificar su correspondencia. El [glosario](GLOSARIO.md) registra las primeras
concordancias y la divergencia encontrada.

## Repetir las comprobaciones

Desde la raíz del repositorio:

```powershell
python dev-tools/export/validate_current_export.py
node --test dev-tools/export/test-export.mjs dev-tools/translation/test-registration.mjs dev-tools/translation/test-adventure-text.mjs dev-tools/translation/test-item-text.mjs
python dev-tools/translation/audit_current.py
python dev-tools/translation/audit_runtime.py
python dev-tools/buildScripts/build_release.py --ref HEAD
```

Antes de `audit_runtime.py`, ejecutar en Foundry la macro «Phandelver - Validar
revision», que importa `validate-runtime.mjs`. `pilot:true` crea el diario si
no existe y valida su texto; si se modifica el piloto, una discrepancia debe
investigarse, no sobrescribirse silenciosamente. Recargar Foundry tras cambios
de traducción o scripts. La construcción normal exige un árbol Git limpio.

## Continuación: opciones de personaje

El [lote de opciones](LOTE-OPCIONES.md) completa nombres y descripciones del
pack y nombres personalizados de avances. Charlatán se importó como objeto piloto
y se contrastaron descripción y avances. Se documentan tres discrepancias del
original: enlaces de Sabio a tablas del Forastero, ausencia de concesión de
Viajero en el Forastero y once trasfondos en el pack frente a los doce anunciados.
Estas incidencias funcionales permanecen abiertas y no se alteran desde la traducción.
