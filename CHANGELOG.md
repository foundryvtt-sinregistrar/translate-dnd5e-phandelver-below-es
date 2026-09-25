# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added

- Complete Spanish item and bestiary packs, including activities, effects and Adventure copies.
- Full Adventure text coverage: 521 text pages, scene labels, tokens, notes, folders and actor index.
- Field-level review evidence and integral audits for all 10,855 expected text fields.
- Actual-world import validation, with original-source broken references documented separately.
- Spanish adventure presentation, cover caption and all 31 PBSO interface strings.
- Spanish names for all 39 player options, 32 descriptions and 25 advancement labels.
- Imported background pilot and label-only advancement converter preserving keyed and legacy collections.
- Reproducible coverage, runtime and protected-field audits with review reports.

### Changed

- Verified Foundry compatibility updated to 14.368 and dnd5e to 6.0.3 after runtime and full import checks.
- Terminology, narrative clues, original measurement units and currency denominations reviewed throughout.
- Adventure journal, page and folder translations use original document IDs.
- Release ZIP and manifest are built from the same Git ref and checked for private files.

### Fixed

- Preserve Adventure-specific token names after Babele's import synchronization.
- Reapply explicit item and actor translations after fallback, including unchanged proper names.
- Babele registration waits for language settings and applies only to Spanish locales.
- Converter loading is guaranteed by an explicit import from the entry module.

---

## [1.14.0] - 2026-08-29

### Added

- Initial module structure.
- Babele registration for the five Phandelver & Below compendiums.
- Translation templates for adventures, actors, items, player options, and roll tables.
- GitHub Actions release workflow.
- Foundry source-export utility and translation workflow documentation.
- Spanish navigation names for the adventure, folders, and journal sections.
- Initial translated journal pages for running and starting the adventure.
- Complete Spanish translation of all 53 background tables.

### Changed

- Updated metadata and compatibility for Foundry VTT 14.363, dnd5e 5.3.3, Babele 2.7.5, and Phandelver & Below 3.1.0.
- Standardized release packaging and documentation with the other Spanish translation modules.

---

## Version Links

[Unreleased]: https://github.com/foundryvtt-sinregistrar/translate-dnd5e-phandelver-below-es/compare/v1.14.0...HEAD
[1.14.0]: https://github.com/foundryvtt-sinregistrar/translate-dnd5e-phandelver-below-es/releases/tag/v1.14.0
