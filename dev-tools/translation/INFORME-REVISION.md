# Informe final de revisión de Phandelver

Fecha: 25 de septiembre de 2026. Rama: `feature/dnd5e-6.0.3`.

## Resultado

Revisión editorial completada: objetos, bestiario, opciones, tablas y Adventure.
Todos los **10.855 campos de texto previstos** tienen payload propio y pasan
los controles de sintaxis Foundry, atributos HTML, cifras y monedas. Las
**521 páginas con texto** están traducidas; las 686 páginas totales incluyen
ilustraciones y atlas.

Prueba realizada con Foundry **14.368**, dnd5e **6.0.3**, aventura **3.1.0**
y la instalación local de Babele **2.9.1**. No equivale a haber jugado todos
los encuentros ni a certificar todas las versiones de dependencias.

## Cobertura y revisión editorial

| Pack | Documentos | Campos cubiertos |
|---|---:|---:|
| Objetos | 165 | 377/377 |
| Bestiario | 148 | 3.227/3.227 |
| Opciones | 39 | 97/97 |
| Tablas de jugador | 53 | 436/436 |
| Adventure | 1 | 6.718/6.718 |

Completados los 918 textos originales distintos del bestiario, los 214 textos
exclusivos de Adventure, las 155 biografías del índice de actores y la lectura
bilingüe de las 309 páginas heredadas. Los registros `reviewed-fields.json`,
`legacy-source-index.json` y los lotes conservan evidencias y huellas.
Véase [revisión del legado](LOTE-ADVENTURE-LEGADO.md).

Se corrigieron omisiones, terminología, etiquetas inglesas, concordancia,
pistas narrativas y unidades. Se conservaron las unidades originales para
evitar conversiones aproximadas. También se revisaron monedas: 510 monedas
de platino no son 510 de plata. Nombres, escenas, fichas, diarios e índices
comparten las decisiones del [glosario](GLOSARIO.md).

## Integración y pruebas

- Registro Babele limitado a español y variantes; identidad por ID.
- Convertidores para objetos, actores, actividades, avances, efectos, escenas,
  tokens, ActorDelta, notas, regiones, niveles, diarios, carpetas, tablas y macros.
  Solo modifican campos de texto permitidos.
- **19 pruebas Node y 14 pruebas Python superadas** al cerrar los lotes.
- **406 documentos** traducidos y validados con el esquema de Foundry: cero errores.
- Comparación contra originales: 10.288 cambios en campos de texto y 13.424
  metadatos Babele, **cero cambios en campos protegidos**. Incluye respaldo
  de otros módulos activos; la cobertura propia se mide aparte.
- Auditoría integral: **10.855/10.855**, cero errores y cero textos largos
  idénticos al inglés. La lectura editorial se acredita con los lotes.
- Importación completa mediante el importador normal, sin conversión opcional
  de monstruos o conjuros a 2024, en `ddn5e-603-phandelver-below`.
  El inventario previo no tenía colisiones con IDs de Adventure.
- Importados: **163 actores, 253 objetos, 61 diarios, 35 escenas, 12 tablas,
  10 macros y 71 carpetas**. Portada y mapa regional mostrados en español.
- Auditoría del mundo importado: **6.715 campos**, cero diferencias pendientes.
  Hay 70 normalizaciones de HTML y cuatro campos de efectos de tokens vinculados
  que Foundry conserva en el actor base. Se comprueba expresamente su presencia.
- La prueba real descubrió que Babele sustituía **45 nombres de fichas** por
  nombres genéricos. `adventure-import.mjs` reaplica los nombres del Adventure
  al finalizar su importación, solo en escenas importadas y en español.
  Reimportación de escenas y auditoría superadas.

## Incidencias heredadas de la fuente

Comprobadas **1.404 referencias distintas** mediante la API de Foundry;
**nueve no resuelven**. El UUID exacto de cada una ya está en el original
inglés exportado. Se conservan los destinos y se registran como excepciones;
no se presenta el resultado como «cero enlaces rotos».

| Referencia | Ubicación / incidencia |
|---|---|
| `Actor.pbsoOshundoTheAl.Item.zWwYUY62Yv5v2jJ2` | Illithinoch: conjuro de Oshundo ausente con ese ID |
| `Compendium.dnd-phandelver-below.pbso-player-options.Item.IgJkSnLiLJOWH7eK` | Changelog histórico: copia retirada de Acólito |
| `Item.HvIOrPJ87fdNqIzV` y `Item.nV7BWCPPsRMHCor1` | Conjuros de Shalfi con IDs de mundo no incluidos |
| `JournalEntry.pbsoCh7illithino.oo9ELp7kXbqSA9KS` | Tabla del cristal: falta el segmento JournalEntryPage |
| `JournalEntry.pbsoCh7illithino.Yc2CgRktnHDElf1R` | Misma tabla y problema |
| `JournalEntry.pbsoCh7illithino.YfeV9foQJa7ZSvOQ` | Misma tabla y problema |
| `JournalEntry.pbsoChapter60000.JournalEntryPage.ehkrLPV6v2RkToDl` | Gema P11: página de la cripta en otro diario |
| `Scene.pbsoMap8p8000000.Token.b4cwGPSHDsoHDPBx.Actor.pbsoNycaloth0000.Item.88M2yMUcv2ugVZE3` | Campo de los Lamentos: ataque enlazado a un objeto sintético ausente |

Los lotes también documentan contradicciones del original: Greska/Grista,
numeración de la forja de Zorzula y referencia de vulnerabilidad cuya prosa
describe resistencia. No se cambia una regla o destino técnico para ocultar
una errata del original.

## Fuentes, distribución y límites

Originales: `source-current/2026-09-24T19-12-21-788Z`, sin traducción.
PDF locales: inglés de 225 páginas y español de 204, con extracción y OCR de
las 429 páginas. El PDF español es una referencia auxiliar de carácter oficial
no acreditado; el inglés determina contenido, cifras y sentido.

Evidencia privada en `dev-tools/export/_data/`: `integral-audit.json`,
`translation-audit.json`, `runtime-validation.json`, `runtime-diff.json`,
`import-validation.json` e `import-audit.json`. Originales y PDF no se
incluyen en Git ni en la distribución.

Compatibilidad verificada: Foundry 14.368 / dnd5e 6.0.3. La instalación local
de Babele usa `converterRegistry.named('document')`; no se ha probado una
instalación limpia independiente de Babele oficial. El ZIP se comprueba por
contenido y extracción aislada; eso no sustituye una instalación mediante
el gestor de Foundry. No se ha hecho push, tag ni release.

## Repetir la validación

Consultar [VALIDACION.md](VALIDACION.md). Ejecutar auditorías estáticas y
`validate-runtime.mjs` en Foundry. Tras importar Adventure, ejecutar
`validate-import.mjs` y `audit_import.py`. La macro final de revisión solo
inspecciona el mundo y guarda informes; no reimporta documentos.
