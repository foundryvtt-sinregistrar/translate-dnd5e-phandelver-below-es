# Translation workflow

## Current review plan (September 2026)

Follow [the review roadmap](dev-tools/ROADMAP.md),
[the current inventory](dev-tools/translation/INVENTARIO.md), and
[the bilingual PDF reference guide](dev-tools/export/README.md).
The existing translation is partial. Phase 1 is complete on Foundry 14.368 /
dnd5e 6.0.3; see [current sources](dev-tools/translation/FUENTES-ACTUALES.md).
Use `python dev-tools/export/prepare_pdf_references.py --ocr-all en es` for PDF
references. Preserve the existing worklist: its legacy builder overwrites it.

## Versioning

Releases use `MAJOR.FOUNDRY.PATCH`:

- `MAJOR`: structural or content milestone;
- `FOUNDRY`: supported Foundry VTT major version;
- `PATCH`: incremental corrections for that compatibility line.

Therefore, `1.14.0` is the first release milestone for Foundry VTT 14.

## 1. Export the source compendiums

Follow [the current export guide](dev-tools/export/README.md). As GM, keep the
official adventure active, disable this translation and reload, then execute
`dev-tools/export/export-source.js` in a Script macro. The exporter uses full
Foundry documents, rejects translated sources, and writes a dated directory
under `dev-tools/export/_data/source-current/`. Restore the translation afterwards.
It preserves the historical `dev-tools/export/_data/source/` directory.

```powershell
python dev-tools/export/validate_current_export.py
python dev-tools/translation/inventory_current.py
```

The files are private and ignored by Git. Do not copy full original documents
into `compendium/`; that directory only accepts reviewed Babele translation payloads.
The old `validate_source_export.py` checks the historical export only.

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

## 7. Release process

1. Move the completed entries from `[Unreleased]` to a dated version in `CHANGELOG.md`.
2. Set the same version in `module.json`.
3. Run the source-export validator and validate every tracked JSON file.
4. Commit the release preparation on `develop`.
5. Fast-forward `main` to the validated `develop` commit and push both branches.
6. Create and push the annotated tag `vMAJOR.FOUNDRY.PATCH` from `main`.
7. Confirm that the GitHub Actions release workflow builds the ZIP and uploads both the stable archive and `module.json`.
8. Inspect the generated draft release and publish it after verifying its assets and manifest URLs.
