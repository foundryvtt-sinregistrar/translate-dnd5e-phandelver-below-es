# Translation workflow

## 1. Export the source compendiums

Enable the following modules in a private Foundry VTT world:

- `babele`
- `dnd-phandelver-below`
- `translate-dnd5e-phandelver-below-es`

Sign in as GM, open the browser developer console, and execute the complete contents of:

```text
dev-tools/export/export-source.js
```

The script downloads `phandelver-below-source-export.zip`. Extract it into:

```text
dev-tools/export/_data/source/
```

This directory is intentionally ignored by Git. It can contain copyrighted source material and must not be committed or redistributed.

The export contains:

- `inventory.json`: IDs, names, types, folders, versions, and translation status.
- `translations/*.json`: Babele-compatible starter files populated with the original translatable fields.

Validate the extracted export before translating:

```powershell
python dev-tools/export/validate_source_export.py
```

The validation must finish with `OK`. If it reports names instead of document IDs as unexpected keys, repeat the export with the current `export-source.js`.

## 2. Work in pack order

Extract the private PDF into a page-addressable JSON index when the reference PDF changes:

```powershell
python dev-tools/export/extract_pdf_text.py
```

The generated `extracted-pages.json` remains under the ignored `_data` directory.

For scanned PDFs, run the resumable Spanish OCR instead:

```powershell
python dev-tools/export/ocr_pdf.py
```

OCR progress is saved after every page in `_data/pdf/ocr-pages.json`. Existing pages are skipped automatically when the command is run again.

Generate the private page-level worklist after exporting the source Adventure:

```powershell
python dev-tools/export/build_adventure_worklist.py
```

Fill `pdf_page_start`, `pdf_page_end`, `status`, and `notes` in `_data/adventure-worklist.csv` while mapping and reviewing journal pages.

Translate and validate packs in this order:

1. `pbso-player-tables`
2. `pbso-player-options`
3. `pbso-items`
4. `pbso-bestiary`
5. `pbso-adventures`

The Adventure pack is last because it contains nested Foundry documents and has the largest integration surface.

## 3. Translation rules

- Keep top-level entry keys unchanged. They are Foundry document IDs, which prevents collisions between documents with duplicate names.
- Keep nested identity fields and IDs unchanged.
- Preserve `@UUID[...]`, `@Embed[...]`, inline rolls, formulas, macros, image paths, and HTML structure.
- Translate visible names, descriptions, biographies, journal text, captions, and table-result text.
- Use the Spanish PDF as the terminology and narrative source.
- Record progress in the private `inventory.json` using `pending`, `translated`, `reviewed`, or `tested`.

## 4. Promote reviewed translations

After completing and reviewing one exported file, copy only its translated Babele payload into `compendium/`. Never copy the private inventory or raw source material into the distributable module.

## 5. Validate in Foundry

For every pack:

1. Reload the world in Spanish.
2. Open documents directly from the compendium.
3. Import representative documents into the world.
4. Check names, HTML, embedded items, activities, effects, links, and rolls.
5. For the Adventure pack, import into a clean test world and inspect journals, scenes, actors, items, tables, notes, and UUID links.

## 6. Release checks

- Validate every JSON file.
- Confirm that no `_data/`, PDF, source export, or temporary file is tracked.
- Build the ZIP from a clean Git commit.
- Install the generated ZIP in a clean Foundry data directory before publishing.
