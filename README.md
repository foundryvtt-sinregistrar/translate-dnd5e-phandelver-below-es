# Phandelver y más allá: El obelisco fragmentado — Traducción al español

**Versión actual — Foundry v14**

![Foundry v14](https://img.shields.io/badge/Foundry-v14-green)
[![Release v1.14.2](https://img.shields.io/badge/release-v1.14.2-blue)](https://github.com/foundryvtt-sinregistrar/translate-dnd5e-phandelver-below-es/releases/tag/v1.14.2)
![dnd5e 6.0.3](https://img.shields.io/badge/dnd5e-6.0.3-blue)
![Babele 2.9.1 required](https://img.shields.io/badge/Babele-2.9.1_required-orange)
![Phandelver required](https://img.shields.io/badge/Phandelver-required-orange)

[![Última versión](https://img.shields.io/github/v/release/foundryvtt-sinregistrar/translate-dnd5e-phandelver-below-es?label=release)](https://github.com/foundryvtt-sinregistrar/translate-dnd5e-phandelver-below-es/releases/latest)
[![Descargas de la última versión](https://img.shields.io/github/downloads/foundryvtt-sinregistrar/translate-dnd5e-phandelver-below-es/latest/total?label=descargas%20%C3%BAltima%20release)](https://github.com/foundryvtt-sinregistrar/translate-dnd5e-phandelver-below-es/releases/latest)

[![Descargas totales](https://img.shields.io/github/downloads/foundryvtt-sinregistrar/translate-dnd5e-phandelver-below-es/total?label=descargas%20totales)](https://github.com/foundryvtt-sinregistrar/translate-dnd5e-phandelver-below-es/releases)


**Español** | [English](README.en.md)

Traducción para Foundry VTT mediante Babele. Identificador: `translate-dnd5e-phandelver-below-es`.

## Estado

Versión: **1.14.2**. Revisión editorial documentada como completada: 165 objetos, 148 criaturas, 39 opciones de personaje, 53 tablas y Adventure, incluidas 521 páginas con texto; 10.855 campos previstos. El informe del 25 de septiembre de 2026 acredita una importación completa con Foundry 14.368, dnd5e 6.0.3, Babele local 2.9.1 y aventura 3.1.0. Conserva nueve referencias sin destino presentes en el original. Esta homogeneización no repite esa prueba ni acredita otras compilaciones de Babele.

Consulta [CHANGELOG.md](CHANGELOG.md).

Comprobación del 28 de septiembre de 2026 en Foundry 14.368, dnd5e 6.0.3 y Babele 2.9.1: lectura de 406 documentos en 5 compendios, comprobación de nombres y campos de texto explícitos e importación y revisión visual de una muestra. No es una revisión lingüística ni funcional exhaustiva; permanecen algunas etiquetas inglesas del contenido original.

## Requisitos

Versiones declaradas en el manifiesto; «—» indica que no se declara ese límite.

| Dependencia | Mínima | Verificada |
|---|---|---|
| Foundry VTT | 13 | 14.368 |
| dnd5e | 5.3.1 | 6.0.3 |
| babele | 2.9.1 | 2.9.1 |
| dnd-phandelver-below | 3.1.0 | 3.1.0 |

Instala y activa las dependencias, adquiriendo por separado los productos oficiales cuando sean necesarios.

## Instalación

En la configuración de Foundry, abre **Add-on Modules → Install Module** y utiliza este manifiesto:

```text
https://github.com/foundryvtt-sinregistrar/translate-dnd5e-phandelver-below-es/releases/latest/download/module.json
```

Para instalar manualmente, descarga `translate-dnd5e-phandelver-below-es.zip` de las [releases](https://github.com/foundryvtt-sinregistrar/translate-dnd5e-phandelver-below-es/releases). Con Foundry detenido, extrae la carpeta `translate-dnd5e-phandelver-below-es` en `Data/modules/`; el manifiesto debe quedar en `Data/modules/translate-dnd5e-phandelver-below-es/module.json`.

## Activación

1. Abre un mundo dnd5e.
2. Activa Babele, sus dependencias, los productos oficiales requeridos y esta traducción.
3. Selecciona **Español** y recarga el mundo.
4. Abre un compendio traducido para comprobar el resultado.

El registro es automático para `es` y sus variantes regionales. Otros idiomas no activan la traducción española.

## Actualización

Actualiza desde Foundry o sustituye la carpeta con el ZIP publicado y Foundry detenido. Recarga el mundo. Las copias ya importadas no se sincronizan automáticamente: revisa las diferencias antes de sustituir documentos con cambios propios.

## Contenido incluido

- `dnd-phandelver-below.pbso-adventures.json`.
- `dnd-phandelver-below.pbso-bestiary.json`.
- `dnd-phandelver-below.pbso-items.json`.
- `dnd-phandelver-below.pbso-player-options.json`.
- `dnd-phandelver-below.pbso-player-tables.json`.

## Limitaciones

La cobertura textual y las pruebas automáticas no acreditan todas las automatizaciones de una partida. Conserva las limitaciones indicadas en Estado. Las copias importadas no se actualizan automáticamente. Las nuevas URLs de release necesitan una publicación con sus adjuntos; mientras no estén disponibles, utiliza un ZIP validado. No se distribuyen fuentes privadas, PDF, OCR ni exportaciones oficiales completas.

## Soporte y contribuciones

Comunica errores en las [incidencias](https://github.com/foundryvtt-sinregistrar/translate-dnd5e-phandelver-below-es/issues), indicando versiones, compendio/documento afectado, pasos, resultado esperado y observado, y si se trata de una copia importada.

## Desarrollo

La [guía de desarrollo](https://github.com/foundryvtt-sinregistrar/translate-dnd5e-phandelver-below-es/blob/main/DEVELOPER.md) está disponible en el repositorio y se excluye del ZIP instalable.

## Licencia y créditos

Consulta la licencia y sus condiciones en [LICENSE.md](LICENSE.md). Se conserva la licencia MIT existente.

Traducción no oficial, sin afiliación con Wizards of the Coast ni Foundry VTT. Los materiales del producto oficial pertenecen a sus respectivos titulares. Autor del módulo: [foundryvtt-sinregistrar](https://github.com/foundryvtt-sinregistrar).
