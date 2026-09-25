/** Run as a Foundry Script macro as GM. See README.md for prerequisites.
 * Historical _data/source/ files are preserved. No Babele extraction is used.
 */
(async () => {
  const {exportCompendiums} = await import(
    "/modules/translate-dnd5e-phandelver-below-es/dev-tools/export/export-compendiums.mjs"
  );
  await exportCompendiums();
})();
