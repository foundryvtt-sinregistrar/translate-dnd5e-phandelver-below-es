# Mapeos comprobados

Cierre: 25 de septiembre de 2026.

El registro se realiza en `babele.init` y `setup`, solo para español y sus
variantes. Las claves son IDs originales; no se colapsan diarios, carpetas o
páginas con nombres repetidos.

| Contenido | Campos de texto |
|---|---|
| Adventure | Nombre, descripción y pie; colecciones anidadas |
| Diarios y páginas | Nombre, contenido y pie de imagen |
| Carpetas | Nombre por ID |
| Objetos | Nombre, descripción, requisitos, texto no identificado, chat, actividades, avances y efectos |
| Actores | Nombre, biografía, ficha, alineamiento, hábitat, tipo, sentidos, idiomas y objetos |
| Escenas | Nombre, navegación, notas, dibujos, fichas, ActorDelta, niveles y regiones |
| Tablas | Nombre, descripción, etiquetas y descripciones de resultados |
| Macros | Nombre; comandos conservados |
| Interfaz | 31 claves PBSO con parámetros intactos |

`document-fallback.mjs` conserva el respaldo de Babele y reaplica los valores
explícitos por ID, incluidos nombres propios iguales al original inglés.
Los avances admiten el esquema actual por ID y el anterior por lista.

`adventure-import.mjs` usa el callback `postImport` de Foundry 14 para conservar
los nombres propios de las fichas tras la sincronización de Babele. Solo actúa
en español, sobre PBSO y las escenas incluidas en la importación; no recorre
otras escenas del mundo ni cambia ajustes de Babele.

Las pruebas comprueban identidad, orden, recursos gráficos, enlaces, fórmulas,
comandos, permisos y mecánicas. La salida real de Babele sobre 406 documentos
tiene cero cambios fuera de texto permitido y metadatos de traducción.
Adventure importado: 6.715 campos del mundo comprobados sin diferencias
pendientes; normalizaciones precisas documentadas en el informe.

El diagnóstico histórico `INVENTARIO.md` se conserva. Para comprobar el
payload actual usar `check_reviewed.py`, `audit_integral.py` y
`audit_current.py`; para la importación, `audit_import.py`.

La implementación se ha probado con la instalación local de Babele 2.9.1
que expone `converterRegistry.named('document')`. No se deduce compatibilidad
con otra compilación únicamente porque declare el mismo número de versión.
