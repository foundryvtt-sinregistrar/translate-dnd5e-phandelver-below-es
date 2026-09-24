# Revisión de mapeos: fase 2

## Puntos implementados y comprobados

1. Registro de idioma: `babele.init` y `setup`; solo español y sus variantes.
   No consulta ajustes antes de que existan. Pruebas `en`, `fr`, `es`, `es-ES`.
2. Identidad de Adventure: 61 diarios, 310 páginas traducidas y 71 carpetas
   pasan a claves `_id`. La reconstrucción de las claves históricas usa el
   algoritmo de nombres/IDs del exportador y verifica los textos ingleses de
   todas las páginas contra los originales actuales antes de modificar nada.
3. Convertidores de carpetas y diarios con campos permitidos explícitos:
   nombres, texto y pies de imagen. No aceptan cambios de IDs, recursos gráficos,
   scripts, orden, permisos, fórmulas ni campos mecánicos. No buscan traducciones
   de diarios por nombre en otros packs. Mantienen las páginas todavía sin traducir.

La migración no revisa ni genera prosa. Las carpetas que compartían nombre
conservan la misma traducción existente, ahora con identidad independiente.
El script aborta ante páginas inglesas cambiadas o campos no contemplados;
una segunda ejecución no vuelve a migrar las claves.

```powershell
python dev-tools/translation/migrate_adventure_ids.py
python dev-tools/translation/inventory_current.py
node --test dev-tools/export/test-export.mjs dev-tools/translation/test-registration.mjs dev-tools/translation/test-adventure-text.mjs
```

Resultado: 11 pruebas superadas, incluida aplicación sobre las fuentes privadas
reales. La prueba restaura solo los campos de texto previstos y compara toda la
estructura resultante con los originales para detectar modificaciones extra.
Si faltan los originales locales, esa prueba se omite explícitamente.

## Pendiente para cerrar la fase

- Integración de diarios y carpetas comprobada con Babele 2.9.1; diario piloto
  importado y abierto. Importación completa de carpetas todavía pendiente.
- Completar la matriz de campos y pruebas para actores, objetos, actividades,
  avances, efectos, tablas, escenas, tokens y ActorDelta; estos convertidores no
  pretenden cubrir colecciones para las que aún no existe traducción.
- Ejecutar el piloto de la fase 4 y comprobar las copias importadas.

No se ha elevado `compatibility.verified` por superar pruebas unitarias.
La fase 2 permanece en curso para los tipos todavía sin payload propio.
`INVENTARIO.md` conserva el diagnóstico anterior a esta migración; su comparación
por nombres no debe regenerarse sobre claves por ID. Usar `inventory_current.py`.

## Matriz de alcance actual

| Colección / campo | Aplicación | Resultado |
|---|---|---|
| Adventure: name, description, caption | Mapeo estándar Babele | Comprobado en runtime y presentación visible |
| Adventure: folders.name | Convertidor propio por ID | 71 nombres comprobados |
| Adventure: journal.name, pages.name/text/image.caption | Convertidor propio por ID | Aplicación y conservación estructural comprobadas; diario piloto importado |
| RollTable: name, description, results.description | Mapeo estándar; resultados por rango | 53 tablas comprobadas contra payload |
| Actor: nombre, biografía, token, objetos, actividades y efectos | Sin payload propio | Cobertura pendiente; otros módulos pueden aportar traducciones de respaldo |
| Item: nombre, descripción, actividades, avances y efectos | Sin payload propio | Cobertura pendiente |
| Scene: nombre, notas, tokens y ActorDelta | Sin payload propio | Cobertura pendiente |
| Macro: nombre y descripción | Sin payload propio | Cobertura pendiente; no traducir comandos |
| Interfaz PBSO | `lang/es.json` | 31 claves, parámetros y etiquetas conservados |

`audit_runtime.py` compara las salidas Babele guardadas contra las fuentes.
Permite solo rutas de texto expresamente enumeradas y metadatos Babele; en
esta ejecución encontró cero cambios fuera de ellas. Se incluyen traducciones
de respaldo de otros módulos activos: no atribuirlas al payload de Phandelver.
