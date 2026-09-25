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

## Segundo lote de prosa: textos 0306–0500

Revisados 195 originales adicionales: ataques, efectos, conjuros y biografías
breves. Las frases repetidas de los ataques se componen desde un diccionario
revisado y una lista explícita de originales inspeccionados; no se sustituyen
atributos HTML ni comandos. Se conservan incluso las discrepancias numéricas
del original, como el daño medio indicado en algunos ataques de grick.

La cobertura llega a 2.615/3.227 campos del bestiario y 4.360/6.718 de Adventure.
`check_reviewed.py` confirma cero errores de evidencia y conservación técnica.
La validación dentro de Foundry de esta nueva prosa está pendiente; la sesión
citada anteriormente corresponde al lote de nombres y campos breves.

## Tercer lote de prosa: textos 0501–0600

Revisados otros 100 originales, incluidos conjuros, lanzamiento innato,
extracción de cerebros y efectos de estados. Se distinguen las variantes del
original: no se añaden requisitos de incapacitación o aturdimiento a un ataque
que no los tenga en su fuente. Las referencias relativas permanecen intactas.
Se ajustan menciones a la nomenclatura existente: Cueva del Oleaje, barrena
infernal, broza movediza y Mirada aterradora.

Cobertura propia: 2.758/3.227 campos del bestiario y 4.528/6.718 de Adventure.
Los controles de evidencia y conservación técnica vuelven a pasar sin errores.

## Cuarto lote de prosa: textos 0601–0720

Revisados 120 textos adicionales; la cobertura alcanza 2.937/3.227 campos del
bestiario y 6.044/6.718 de Adventure. La composición del índice de actores añade
34 páginas cuyo bloque de biografía coincide exactamente con una traducción
revisada. Preserva imágenes y UUID, traduce los encabezados de referencias y
rechaza biografías aproximadas, traducciones ambiguas o texto adicional no revisado.

Incidencias conservadas de la fuente, sin modificar reglas:

- 0603: la calavera llameante se regenera en una hora en la sección secreta,
  pero el resumen público habla de 1d6 días.
- 0617: el lanzamiento pertenece al espectro cinéreo, pero su resumen dice goblin.
- 0642: rejuvenecimiento del renacido indica 24 horas y después 1d6 días.
- 0668: el ataque del cúmulo usa Fuerza en la regla y Constitución en su resumen.
- 0703: los tentáculos aplican incapacitado en la regla y aturdido en el resumen.

Los errores tipográficos puramente editoriales, como la llave suelta tras
«troglodita» en 0680, sí se eliminan. Las variantes de datos y reglas no se
homogeneizan por compartir nombre. Pasa `check_reviewed.py`; la ejecución de
Foundry documentada en el lote de etiquetas corresponde todavía a 0001–0600.

## Quinto lote de prosa: textos 0721–0800

Otros 80 originales revisados: conjuros, agarres, enfermedades y biografías de
criaturas. Se mantienen los comandos de lanzamiento por nombre original y se
traducen sus etiquetas visibles cuando son enlaces UUID. Los cristales mentales
de objetos integrados en actores conservan sus restricciones de uso y su valor.

Cobertura propia: 3.053/3.227 campos del bestiario y 6.178/6.718 de Adventure.
El índice de actores contiene 43 cuerpos de página compuestos con biografías
revisadas. Cero errores en la comprobación de evidencias y estructura técnica.

## Sexto lote de prosa: textos 0801–0850

50 originales adicionales: posesión, engullir, enfermedades, conjuros de control
y transformación y biografías extensas. Se conservan las diferencias entre los
resúmenes y las reglas del original. Se corrige la concordancia de «mole sombría».

Cobertura propia: 3.130/3.227 campos del bestiario y 6.277/6.718 de Adventure.
El índice de actores alcanza 53 cuerpos de página compuestos con biografías
revisadas; otros 102 requieren revisión. Los 850 originales revisados pasan los
controles de números, comandos, enlaces y atributos HTML, sin errores de evidencia.
Estos lotes posteriores al texto 0600 siguen pendientes de validación en Foundry.

## Cierre de cobertura: textos 0851–0918

Revisados los 918 originales únicos, incluidas las biografías extensas y sus
variantes. Cobertura propia del bestiario: **3.227/3.227 campos**, sin campos
pendientes y sin errores de evidencia, números o estructura técnica.

Adventure alcanza 6.428/6.718 campos; su índice incorpora 94 cuerpos de página
compuestos con biografías verificadas. Quedan 61 variantes de ese índice y otros
contenidos exclusivos de Adventure. La cobertura no sustituye su revisión integral.

Las variantes de slaads, mutados, zombis y drows se componen comprobando la igualdad
exacta de los bloques ingleses compartidos y traduciendo sus introducciones y
enlaces específicos. Se conserva en 0865 la diferencia del original entre la regla
de Mirada confusa y su resumen, que añade una repetición al final del turno.
En 0898 solo se repara la negrita cortada a mitad de una frase, sin alterar reglas.
La prueba completa de este cierre en Foundry queda pendiente.
