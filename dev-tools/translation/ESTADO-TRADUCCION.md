# Estado de la traducción

Actualizado: 25 de septiembre de 2026. Rama: `feature/dnd5e-6.0.3`.

**Revisión editorial terminada para los cinco packs y Adventure.**
Los 10.855/10.855 campos previstos tienen payload. Los controles de HTML,
números, monedas, sintaxis Foundry y evidencias por hash pasan sin errores.

| Contenido | Cobertura |
|---|---:|
| Objetos | 165/165 documentos; 377 campos |
| Bestiario | 148/148 documentos; 3.227 campos |
| Opciones de personaje | 39/39 documentos; 97 campos |
| Tablas de jugador | 53/53 documentos; 436 campos |
| Adventure | 1/1; 6.718 campos |
| Diarios y páginas | 61 diarios; 686 páginas; 521/521 textos |
| Interfaz propia PBSO | 31/31 claves |

Se completaron los 918 originales distintos del bestiario, los 214 textos
exclusivos de Adventure y la lectura bilingüe de las 309 páginas heredadas.
Las copias solo reutilizan traducciones con original coincidente.

En Foundry 14.368 / dnd5e 6.0.3 se validaron 406 documentos y se importó toda
la aventura en el mundo de pruebas `ddn5e-603-phandelver-below`, sin colisiones
previas de IDs de Adventure. La comparación posterior comprueba 6.715 campos
del mundo sin errores; otros tres pertenecen al importador. Las nueve referencias
sin destino heredadas del original se documentan en el [informe](INFORME-REVISION.md).

La prueba usa la instalación local de Babele identificada como 2.9.1, con su
registro moderno de convertidores. No acredita otras compilaciones con el mismo
número de versión. No se ha publicado una release ni hecho push.
