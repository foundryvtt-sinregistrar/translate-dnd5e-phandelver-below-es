# 🇪🇸 Phandelver y Más Allá — Español (Babele)

Traducción al español para Foundry VTT del módulo oficial **Phandelver & Below: The Shattered Obelisk**.

## Requisitos

- Foundry VTT 13 o 14
- Sistema dnd5e 5.3.1 o superior
- Babele 2.9.1 o superior, con registro de convertidores compatible
- Módulo oficial `dnd-phandelver-below` 3.1.0 o superior

## Instalación

En Foundry VTT, abre **Add-on Modules**, selecciona **Install Module** y utiliza este manifiesto:

```text
https://raw.githubusercontent.com/foundryvtt-sinregistrar/translate-dnd5e-phandelver-below-es/main/module.json
```

También puedes descargar el ZIP de la [última versión](https://github.com/foundryvtt-sinregistrar/translate-dnd5e-phandelver-below-es/releases/latest). Instala este módulo y sus dependencias, actívalos en el mundo y selecciona Español como idioma de Foundry VTT.

## Estado

Revisión editorial completada: **165 objetos, 148 criaturas, 39 opciones de personaje, 53 tablas y Adventure**, incluidas sus **521 páginas con texto**. Se cubren los 10.855 campos de texto previstos en los originales actuales.

La revisión del 25 de septiembre de 2026 comprobó la traducción y la importación
completa en Foundry 14.368 / dnd5e 6.0.3, con la instalación local de Babele 2.9.1
y aventura 3.1.0. Las auditorías no detectan cambios en mecánicas ni pérdidas
de texto. Hay nueve referencias sin destino ya presentes en la aventura original.
La prueba no acredita otras compilaciones de Babele ni una release publicada. Consulta el
[informe de revisión](dev-tools/translation/INFORME-REVISION.md) en el repositorio.

## Desarrollo

Las traducciones se almacenan en `compendium/`, usando el identificador original de cada documento dentro de `entries`.

La versión sigue el esquema `MAJOR.FOUNDRY.PATCH`. En `1.14.0`, el segundo componente indica compatibilidad con Foundry VTT 14.

Consulta [DEVELOPER.md](DEVELOPER.md) para el flujo de exportación, traducción, validación y publicación.

Este proyecto no está afiliado ni respaldado por Wizards of the Coast o Foundry Gaming. Requiere el módulo comercial oficial y no redistribuye sus archivos fuente, ilustraciones ni bases de datos.
