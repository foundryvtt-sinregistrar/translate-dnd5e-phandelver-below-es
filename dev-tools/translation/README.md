# Procedimiento de revisión

1. Leer el [roadmap](../ROADMAP.md) y congelar una copia de la exportación histórica.
2. La fase 1 ya dispone de [fuentes actuales](FUENTES-ACTUALES.md). Para renovarlas,
   usar el exportador de documentos completos con la traducción desactivada y
   seguir la guía de exportación; no reemplazar el histórico.
3. Regenerar el diagnóstico local desde la raíz del módulo:

   ```powershell
   python dev-tools/export/validate_source_export.py
   python dev-tools/export/validate_current_export.py
   python dev-tools/translation/inventory_current.py
   ```

   `inventory.py` conserva el diagnóstico histórico por nombres; no ejecutarlo
   sobre el payload ya migrado a IDs. Para cobertura actual y protección de
   texto, ejecutar `python dev-tools/translation/audit_current.py`.

4. Consultar [referencias PDF](../export/README.md). Buscar primero el pasaje EN y
   luego el ES por título y contexto. Registrar por separado página física y
   número impreso; no aplicar un desplazamiento global entre idiomas.
5. Revisar un piloto antes de completar lotes. Contrastar la traducción actual,
   no reemplazarla automáticamente. Reutilizar solo equivalencias verificadas.
6. Mantener una lista de revisión con pack, ID principal, claves anidadas, campo,
   referencia EN/ES, incidencia, propuesta, decisión y evidencia de validación.
   Usar `pending`, `translated`, `reviewed`, `tested`; no inferir estados del
   número de cadenas presentes. Conservar la lista histórica `_data/adventure-worklist.csv`.
   `build_adventure_worklist.py` la sobrescribe: no ejecutarlo sobre trabajo revisado.
7. Cambiar únicamente los payloads revisados en `compendium/` y, cuando proceda,
   interfaz y convertidores. No copiar originales ni referencias a la distribución.
8. Cerrar cada lote con controles técnicos y lectura; cerrar la aventura con una
   importación completa en un mundo de pruebas limpio.

Los informes de `inventory.py` cuentan hojas de texto, también técnicas. Son un
diagnóstico estructural del export histórico, no una auditoría lingüística ni de
aplicación de Babele. El detalle de rutas y SHA-256 queda en
`../export/_data/translation-inventory.json`.
