# Objetos: revisión del 25 de septiembre de 2026

Se han traducido los 377 campos de texto no vacíos de los 165 documentos de
`pbso-items`: nombres, 142 descripciones, textos de objetos no identificados,
mensajes de chat, condiciones de activación y textos de efectos. Los campos
originalmente vacíos siguen vacíos. Las copias con texto inglés idéntico en
Adventure y bestiario reciben la misma traducción por ID.

Los cuatro archivos `item-texts*.json` contienen las decisiones editoriales,
contrastadas con los originales exportados. No son salidas del motor automático.
`apply_reviewed_texts.py` comprueba tokens y números antes de aplicarlas y guarda
hashes de original y traducción en `reviewed-fields.json`. `check_reviewed.py`
verifica también los atributos HTML. Se conservan las unidades del original,
sin introducir conversiones de volumen, peso o distancia.

## Incidencias del original conservadas

- `pbsoStatueMucus0` enlaza `rule=damagevulnerability`, aunque el texto dice
  **resistencia** al daño psíquico. Se traduce correctamente el texto visible y
  se conserva el identificador del enlace. Corregir la referencia de reglas es
  una incidencia funcional del contenido original.
- El mensaje de chat de `OjkIqlW2UpgFcjZa` contiene la errata «against anyone the
  wearer». Se resuelve como «contra el portador», de acuerdo con su descripción.
- Hendedora y Garra no especifican el valor de su bonificador en la prosa. No se
  añade una cifra que el texto original no contiene.
- El Bastón de defensa contiene las invocaciones `[[/item Mage Armor]]` y
  `[[/item Shield]]`. Se conservan como instrucciones, no como texto traducible.
- La auditoría general señala `8,000` → `8.000` libras del hacha inamovible.
  Es un cambio de separador de millares, no de capacidad; la comprobación del
  lote normaliza ambos a 8000.

## Validación

Con Foundry 14.368, dnd5e 6.0.3 y la instalación local de Babele 2.9.1:

- 406 documentos pasan las comprobaciones de textos y validación estricta de
  sus modelos. Informe: `2026-09-24T23:23:51.178Z` (UTC).
- 5.976 cambios de texto y cero cambios en campos protegidos, contando también
  las traducciones auxiliares de otros módulos activos.
- Los pilotos anteriores de diario y trasfondo siguen siendo válidos.
- 17 pruebas Node cubren exportación, registro y convertidores.

La integración utiliza el convertidor de documentos de Babele para mantener las
traducciones auxiliares y reaplica los textos locales por ID después. Esto evita
que un nombre propio conservado, como Droop, sea reemplazado por el nombre de una
criatura genérica. Los mapeos requieren el registro de convertidores de la
instalación local de Babele 2.9.1; no se ha probado una distribución externa
limpia ni Babele 2.7.5. El mínimo declarado pasa a 2.9.1.

La revisión lingüística del paquete de objetos está completa. Esto no acredita
todavía la importación integral de Adventure, las automatizaciones de cada objeto
ni la revisión del bestiario; se comprueban en sus lotes respectivos.
