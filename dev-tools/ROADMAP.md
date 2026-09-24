# Roadmap de revisión de Phandelver & Below

Actualizado: 24 de septiembre de 2026.

Se sigue el orden de Tomb of Annihilation: fuentes e inventario, mapeos,
glosario, piloto, lotes editoriales, auditoría e importación completa y publicación.
Aquí se parte de una **traducción parcial existente**, no de un borrador integral.

**Fase 1 completada:** originales exportados y validados desde Foundry 14.368 /
dnd5e 6.0.3. Véase [fuentes actuales](translation/FUENTES-ACTUALES.md).
Siguiente paso: fase 2, mapeos y resolución de claves por ID; no se ha iniciado
todavía la corrección editorial de los lotes.

## Punto de partida comprobado

- [Inventario reproducible](translation/INVENTARIO.md): 406 documentos principales
  en la exportación histórica. Las 53 tablas tienen entradas; opciones (39),
  objetos (165) y bestiario (148) tienen `entries` vacíos en la traducción.
- Adventure contiene 61 diarios y 686 páginas en la fuente histórica; la
  traducción incluye 61 diarios y 310 páginas. La presencia de una página no
  certifica que estén traducidos todos sus campos ni que su texto sea correcto.
- Faltan las colecciones de escenas, macros, tablas, objetos y actores de
  Adventure en el payload actual. También deben revisarse descripción y caption.
- El validador de IDs principales pasa para la exportación del 27 de agosto:
  Foundry 14.363, dnd5e 5.3.3, aventura 3.1.0. No prueba pureza del original,
  IDs anidados, cobertura editorial ni compatibilidad con la instalación actual.
- Entorno confirmado en ejecución: Foundry 14.368, dnd5e 6.0.3,
  Babele 2.9.1 y aventura 3.1.0. La nueva exportación conserva los 406 IDs
  principales; Adventure contiene 71 carpetas, frente a 15 nombres distintos
  en el export histórico. Sus 61 diarios tienen 45 nombres distintos.
- Referencias: inglés de 225 páginas y español de 204, con la estructura de
  Tomb adaptada a `export/_data/references/`. Véase [la guía](export/README.md).
- La lista histórica tiene 686 filas `pending`; se conserva sin sobrescribir.

## Fases y criterios de cierre

| Fase | Trabajo | Criterio de cierre | Estado |
|---|---|---|---|
| 0. Referencias y diagnóstico | Extraer ambos PDF, conservar texto nativo, OCR, bloques, huellas y páginas dudosas; inventariar traducción existente | Manifiestos completos y sin errores; informe inicial reproducible | Preparado; extracción automática, no transcripción revisada |
| 1. Fuentes actuales | Exportar los cinco packs originales con traducción desactivada, inventariar Adventure y registrar versiones y SHA-256 | Originales sin marcas de traducción; recuentos y claves contrastados con la API de Foundry | Completada; línea base 2026-09-24T19-12-21-788Z |
| 2. Mapeos | Revisar esquemas y convertidores Babele para documentos y copias anidadas | Cada campo visible del piloto se aplica sin alterar mecánicas | Pendiente |
| 3. Glosario | Alinear EN/ES por título y contexto; decidir nombres, lugares y términos | Decisiones con pasaje EN, pasaje ES, ubicación Foundry y estado | Pendiente; criterios preparados |
| 4. Piloto | Revisar una página, actor con objetos/actividades/efectos, objeto, tabla y escena con nota y token | Apertura directa e importación correctas; enlaces, tablas y tiradas funcionales | Pendiente |
| 5. Revisión por lotes | Corregir contenido existente y completar huecos; registrar evidencia por campo/página | Cada lote pasa de pendiente a revisado y después a probado | Pendiente |
| 6. Auditoría integral | Cobertura, inglés residual, HTML, UUID, embeds, números, fórmulas y consistencia entre copias | Incidencias cerradas o excepciones justificadas; importación completa en mundo limpio | Pendiente |
| 7. Publicación | Ajustar compatibilidad solo con pruebas; revisar README, changelog, ZIP y workflow | Instalación del ZIP e importación verificadas; fuentes privadas fuera del paquete | Pendiente |

## Orden de revisión

Primero tablas de trasfondo, opciones de personaje, objetos y bestiario. Después
Adventure, reutilizando únicamente textos cuyo original coincida y conservando
las variantes locales. Las copias de actores/objetos en Adventure se comprueban
por separado de los packs independientes.

Los números siguientes son **páginas impresas inglesas del índice**, contrastadas
visualmente en la página física 5. No son rangos físicos ni equivalencias españolas.
La lista por página Foundry debe enlazar las dos referencias de forma independiente.

| Lote | Referencia inglesa | Inicio impreso | Alcance |
|---|---|---:|---|
| Introducción | Welcome to Phandalin | 5 | Resumen, trasfondos, ganchos e influencia del Reino Lejano |
| Capítulo 1 | A Dangerous Journey | 15 | Viaje, emboscada y escondite Cragmaw |
| Capítulo 2 | Trouble in Phandalin | 27 | Población, PNJ y escondite de los Redbrands |
| Capítulo 3 | The Spider's Web | 47 | Localizaciones regionales y castillo Cragmaw |
| Capítulo 4 | Wave Echo Cave | 65 | Cueva, encuentros, tesoros y desenlace |
| Capítulo 5 | Paths of Peril | 77 | Fragmentos robados, Zorzula e Indigo Sanctum |
| Capítulo 6 | The Shattered Obelisk | 103 | Talhundereth, cripta y Gibbet Crossing |
| Capítulo 7 | Rifts in Reality | 139 | Túneles, Illithinoch y brechas |
| Capítulo 8 | Beyond a Lightless Star | 169 | Briny Maze, Ilvaash y epílogo |
| Apéndices | Bestiary / Magic Items / Story Tracker | 203 / 217 / 221 | Concordancia con fichas, objetos y seguimiento |
| Material Foundry | Sin correspondencia obligatoria en PDF | — | Créditos, ayuda, changelog, índices, macros, atlas e ilustraciones |

## Riesgos concretos que debe cubrir la revisión

1. El exportador nuevo sustituye `game.babele.extract` por documentos completos,
   rechaza el módulo de traducción activo, packs traducidos y marcas de Babele.
   `validate_current_export.py` valida huellas, IDs anidados y recuentos; el
   validador histórico se conserva para comparar el material anterior.
2. Las claves anidadas mezclan nombres e IDs. Resolver duplicados sin convertir
   indiscriminadamente nombres a IDs ni romper los mapeos existentes.
3. El registro actual usa el idioma activo y su variante base. Verificar que no
   aplique el español cuando el mundo esté en inglés.
4. Auditar token names, notas, carpetas, ActorDelta, actividades, efectos, tablas
   y texto de interfaz. Mantener comandos de macros, scripts, imágenes, geometría,
   fórmulas, IDs y destinos de enlaces intactos.
5. Ninguna heurística de inglés residual sustituye la lectura editorial. Separar
   nombres propios, contenido técnico y texto narrativo realmente sin traducir.
6. Los PDF difieren en extensión y pueden contener OCR defectuoso. No asumir que
   la referencia española sea oficial o completa; documentar omisiones y usar
   el original inglés para resolver sentido, cifras y contenido.
7. El ZIP actual usa `git archive`: comprobar `.gitattributes` y contenido real
   del paquete para excluir herramientas y cualquier fuente privada antes de publicar.

## Seguimiento

Consultar [estado](translation/ESTADO-TRADUCCION.md),
[procedimiento](translation/README.md), [glosario](translation/GLOSARIO.md) y
[validación](translation/VALIDACION.md). La exportación se ha ejecutado en Foundry;
todavía no se han probado traducciones, importación completa ni publicación.
