# Registro de adopción

Proyecto: `translate-dnd5e-phandelver-below-es`. Rama: `chore/homogeneizacion-documentacion`.

Plantilla inicial: PHB `caf298ee2c8b78c27634c2e2f23baf87e44243fe`; base anterior a esta aplicación en el destino: `68cf25d7bf61875ce5f21266d8b3d042bc0c9ed7`. Base común ampliada: `4ab392ea3fbe0e3d7eb44f803a07fe631d15916e` (plantilla versión 2; perfiles y SHA-256). La suite común y el constructor proceden de esa revisión; el perfil de cada destino se conserva por separado.

## Archivos y adaptaciones

Documentación bilingüe, DEVELOPER, CHANGELOG, `.editorconfig`, `.gitattributes`, base de `.gitignore`, constructor y suite de 24 pruebas compartida. El perfil versionado conserva alias `translate-dnd5e-phandelver-below-es.zip`, canal `latest` y variante `standard`. Se mantiene la licencia existente; los avisos de DM/Tomb no sustituyen la decisión pendiente sobre sus aportaciones.

Se conservan exportador, importación Adventure, mappings y auditorías específicos. El constructor incorpora el contrato común de PHB en su ruta existente. Las suites adicionales siguen en `dev-tools/export/` y `dev-tools/translation/`; las pruebas que requieren originales se omiten explícitamente en un clon sin ellos. Consulta `dev-tools/translation/INFORME-REVISION.md` para la evidencia editorial y de importación previa.

## Sincronización

Antes de actualizar herramientas comunes, compara la base registrada con la nueva revisión de PHB y revisa las diferencias de cada archivo. Conserva este perfil, las suites propias y los adaptadores. No sobrescribas traducciones ni adaptes una licencia mediante una copia ciega. Los SHA-256 del inventario identifican los bytes de Git sin conversiones LF/CRLF.

## Validación y commits

El informe global registra los resultados definitivos, omisiones, inventario del ZIP y commits. Consulta `git log --oneline -- dev-tools/homogeneizacion/ADOPCION.md` para localizar la adopción. CI remota, pruebas funcionales en Foundry y publicación se verifican por separado; no se presentan como ejecutadas por una validación local.
