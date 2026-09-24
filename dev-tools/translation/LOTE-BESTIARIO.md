# Bestiario: revisión en curso

## Identidad, campos breves y etiquetas

Revisados los nombres y prototipos de las 148 criaturas, sus alineamientos,
hábitats personalizados, subtipos, idiomas y sentidos especiales. Se han revisado
también los nombres de los objetos, rasgos, conjuros, actividades y efectos
incrustados. Se aplican por ID, con comprobación de hashes y tokens.

El diccionario de rasgos incluye las variantes adicionales de Adventure. Las 163
identidades de sus actores están cubiertas, incluidos los personajes que
comparten un ID con una criatura genérica del bestiario. Se conserva, por ejemplo,
Lowarnizel en Adventure y Dragón amatista joven en el bestiario. No se usan los
IDs de distintos paquetes como prueba de igualdad de los textos.

La revisión de contexto corrigió «Freeze» a «Congelación»: es la vulnerabilidad
al frío del elemental de agua, no una instrucción de inmovilidad. Los requisitos
heredados «Bat» del horror ganchudo y «Octopus» del pulpo se traducen literalmente;
no se cambia su funcionamiento ni se deducen requisitos nuevos.

Validación de este lote: `2026-09-24T23:34:42.692Z` UTC, Foundry 14.368,
dnd5e 6.0.3 y Babele local 2.9.1. Pasan los 406 documentos; 7.844 cambios de texto,
cero cambios protegidos. Los textos pendientes pueden seguir recibiendo
traducciones auxiliares de otros módulos; estas no se contabilizan como revisión
editorial de este proyecto.

Tras este lote, la cobertura propia es 1.998/3.227 campos del bestiario y
3.589/6.718 campos de Adventure. Quedan por revisar 1.099 descripciones y 130
biografías del bestiario. Son 913 textos originales distintos aún sin cubrir.
El siguiente lote se centra en esos textos, con propagación solo por coincidencia
del original. La revisión integral permanece abierta.

## Primer lote de prosa: textos 0001–0305

Revisados 305 originales distintos de un índice estable de 918 descripciones y
biografías. El índice incluye cinco textos ya cubiertos por el lote de objetos.
Los hashes del índice se contrastan íntegramente antes de aplicar cualquier lote;
un cambio de la fuente detiene la aplicación. Las traducciones están en
`bestiary-texts-01.json` a `bestiary-texts-04.json`.

Este lote cubre ataques múltiples, sentidos, resistencias, estados, equipo y
primeras biografías breves. Conserva los comandos `[[/item ...]]`, los marcadores
`{creature}`, las referencias de condiciones, las secciones secretas y la
atribución a Forgotten Adventures. No interpreta un mismo ID compartido entre
paquetes como prueba suficiente para reutilizar una descripción.

Tras aplicar el lote: 2.372/3.227 campos del bestiario y 4.071/6.718 de Adventure.
Todos los hashes de los campos revisados, números, tokens y atributos HTML pasan
`check_reviewed.py`. Esta cifra sigue siendo cobertura parcial; faltan las
descripciones extensas y la mayor parte de las biografías.
