# Validación en Foundry — 28 de septiembre de 2026

Proyecto: `translate-dnd5e-phandelver-below-es`. Versión preparada: **1.14.2**.

Entorno: Foundry **14.368**, dnd5e **6.0.3**, Babele **2.9.1**, idioma `es`, mundo de pruebas `dnd5e-603-testing` en `http://localhost:31490/game`.

Se activaron los siete módulos de traducción y sus productos oficiales. Versiones oficiales observadas: DMG 2.0.0, MM 1.4.0, PHB 2.2.0, Phandelver 3.1.0, Tasha 4.0.0 y Tomb 2.0.0. Estas observaciones no cambian automáticamente los mínimos declarados de compatibilidad.

## Resultado y alcance

- 406 documentos cargados de 5 compendios.
- 406 nombres almacenados contrastados con sus traducciones; se comprobó también el índice.
- 863 campos de texto con mapping explícito contrastados, además de los nombres.
- Cero diferencias pendientes dentro de ese alcance tras distinguir campos almacenados y derivados.
- Una muestra importada y abierta visualmente: **Daga enjoyada** (`Compendium.dnd-phandelver-below.pbso-items.Item.0E565kQUBmndJ1a2`).
- Nombre, descripción y campos mecánicos seleccionados conservados en la copia importada: tipo, nivel, rareza, peso y daño base cuando existen.

La muestra queda identificada en la carpeta de objetos `QA - Homogeneizacion 2026-09-28`; no se sobrescribieron documentos existentes. No se modificaron compendios oficiales, traducciones fuente ni reglas. La macro de QA y los informes JSON completos son evidencia local, excluida de la distribución.

El validador específico comprobó 406 documentos y sus campos anidados sin errores. Se revisó la presentación del importador de Adventure en español. No se repitió la importación integral de la aventura en esta sesión; la evidencia de ese proceso del 25 de septiembre se conserva por separado.

## Límites

Los nombres de objetos no identificados pueden diferir del nombre real almacenado. Se observaron etiquetas inglesas de clase/subclase en algunas fichas, nombres alternativos ingleses y créditos añadidos por el sistema. Se conservan y no se presentan como una traducción íntegra revisada.

La evidencia acredita lectura de compendios e importación y presentación de muestras. No acredita todas las combinaciones de módulos, una campaña completa, combate exhaustivo, importaciones integrales nuevas ni el mecanismo de actualización desde versiones antiguas. La disponibilidad de las URLs públicas y los adjuntos se comprueba después de publicar.
