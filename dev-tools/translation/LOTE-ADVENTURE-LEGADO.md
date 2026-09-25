# Revisión editorial de Adventure heredado

El inventario estable contiene 309 páginas previamente traducidas, distintas
del contenido nuevo. `legacy-source-index.json` identifica cada campo y fija
las huellas del original y de la traducción anterior. Las decisiones explícitas
de `legacy-corrections-*.json` se aplican solo a esos textos; una lista vacía
significa que la lectura comparada no ha requerido cambios.

## Introducción y capítulo 1: 0001–0024

Leídas y contrastadas las 24 páginas completas: introducción, reglas opcionales,
ganchos, ruta a Phandalin, emboscada y todas las salas de la Guarida Cragmaw.
Se corrigen «Arpistas», la descripción de Nezznar como estratega y el nombre
del gancho «Nos vemos en Phandalin». Se uniforman etiquetas de interfaz y la
referencia a la Cripta de Talhund.

Se restauran pies y millas del original en las páginas revisadas, sin convertir
ningún dato mecánico de las fichas ni los mapas. Esto evita combinar en una misma
aventura el criterio métrico heredado con las unidades de objetos y bestiario.
Se restituyen también una mención de H3 y cifras escritas en letra, para que
las comprobaciones numéricas sean estrictas y reproducibles.

Los atributos accesibles de las monedas y la imagen del reparto de recompensas
se consideran texto traducible mediante una lista exacta EN/ES por etiqueta y
atributo. No se relaja la protección de rutas, clases ni otros atributos.

Las 24 páginas pasan huellas, números, comandos y atributos HTML. Se registran
como `legacy-editorial` en `reviewed-fields.json`. Quedan 285 páginas de este
inventario para lectura comparada; no deben considerarse revisadas por tener texto.
