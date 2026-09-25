# Lote de opciones de personaje

Fuente: `source-current/2026-09-24T19-12-21-788Z`, pack
`dnd-phandelver-below.pbso-player-options`. Entorno: Foundry 14.368 / dnd5e 6.0.3.

Se han traducido las 39 entradas: once trasfondos, doce rasgos y dieciséis
objetos de apoyo. Incluyen 32 descripciones y 25 nombres personalizados de
avances. Las siete entradas sin descripción tampoco la tienen en el original.
Los 26 avances con nombre vacío siguen usando la etiqueta generada por el sistema.

La fuente de contenido y reglas es el documento exportado de Foundry. Los PDF
de la aventura no contienen necesariamente estas descripciones completas de
trasfondos; no se les atribuye una equivalencia de página inexistente. Las
búsquedas de los títulos Shelter of the Faithful y Guild Membership y sus
equivalentes españoles no localizaron pasajes en los textos extraídos.

## Criterios y comprobaciones

- Traducción de nombres y prosa, sin añadir reglas ausentes del original.
- UUID, referencias, etiquetas y atributos HTML protegidos conservados.
- Cifras idénticas tras normalizar separadores. Se mantienen los 50 pies de
  cuerda del Marinero; no se cambia el peso, alcance ni unidades de sus objetos.
- Cuota del gremio de 5 po al mes; Viajero proporciona sustento al personaje y
  hasta otras cinco personas. Se mantienen las condiciones y limitaciones de
  hospitalidad, ayuda del templo y pasaje gratuito.
- Los avances de dnd5e 6 son una colección por ID. El convertidor propio
  `phandelverAdvancementNames` permite exclusivamente el nombre. Conserva concesiones,
  elecciones, UUID, tipos, niveles, cantidades y configuración.
  También conserva el formato antiguo en lista y su campo `title`; esta
  compatibilidad de estructura tiene pruebas unitarias, no una prueba completa
  de ejecución sobre versiones anteriores de Foundry/dnd5e.
- Se corrigió al traducir el encabezado partido `S<strong>kill Proficiencies`
  del Artesano gremial: ahora se muestra «Competencias en habilidades».
- La auditoría estática del pack no encuentra diferencias en sintaxis protegida,
  atributos ni cifras. El validador de runtime comprueba descripción y avances
  por ID, además del nombre.

Se importó Charlatán en la carpeta de objetos «Phandelver - Revision». La hoja
muestra prosa, habilidades y enlace al rasgo en español. Se comprobaron nombres
y avances guardados; la única diferencia de descripción es la normalización
de tres etiquetas `<hr />` a `<hr>` que realiza Foundry. El validador acepta
solo esa equivalencia concreta y registra los fallos de piloto, evitando que
se reutilice como válido un informe anterior.

## Incidencias heredadas de los originales

| Documento | Hallazgo | Tratamiento |
|---|---|---|
| Sabio / `pbsoSage00000000` | Ideal, vínculo y defecto enlazan tablas del Forastero | Se conservan los tres UUID; pendiente decidir una corrección funcional separada |
| Forastero / `pbsoOutlander000` | La descripción enlaza Viajero, pero sus avances no incluyen una concesión de ese rasgo | No se añade una concesión desde el payload de traducción |
| Pack de opciones | Contiene once documentos de tipo background; la presentación oficial anuncia doce trasfondos | Se documenta la diferencia sin inventar un duodécimo documento |

Estas incidencias no son fallos introducidos por la traducción y siguen abiertas.
La prueba de un trasfondo importado no sustituye la comprobación de todas las
concesiones al añadirlo a un personaje ni la importación completa de Adventure.
