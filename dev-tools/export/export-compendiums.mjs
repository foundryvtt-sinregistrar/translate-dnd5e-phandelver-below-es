/** Run exportCompendiums() from a Foundry script macro, as GM. */
export const SOURCE = "dnd-phandelver-below";
export const PACKS = ["pbso-player-tables", "pbso-player-options", "pbso-items", "pbso-bestiary", "pbso-adventures"];
export const DESTINATION = "modules/translate-dnd5e-phandelver-below-es/dev-tools/export/_data/source-current";
export const TARGET = "translate-dnd5e-phandelver-below-es";

export function assertIds(documents, path) {
  const ids = documents.map(doc => doc._id);
  if (ids.some(id => typeof id !== "string" || !id) || new Set(ids).size !== ids.length)
    throw new Error(`Invalid or duplicate IDs: ${path}`);
  for (const doc of documents) {
    for (const key of ["actors", "items", "journal", "pages", "scenes", "tables", "results",
      "macros", "folders", "effects", "tokens", "notes", "playlists", "cards", "regions", "behaviors"]) {
      if (Array.isArray(doc[key])) assertIds(doc[key], `${path}.${doc._id}.${key}`);
    }
  }
}

export function assertOriginal(value, path = "document") {
  if (!value || typeof value !== "object") return;
  if (value.flags?.babele || value.translated || value.hasTranslation || value.originalName) {
    throw new Error(`Babele translation marker at ${path}. Disable Babele and reload before exporting.`);
  }
  for (const [key, child] of Object.entries(value)) {
    if (child && typeof child === "object") assertOriginal(child, `${path}.${key}`);
  }
}

export function summarizeDocuments(documents) {
  const counts = {documents: documents.length, pages: 0, activities: 0, effects: 0, advancement: 0, items: 0, results: 0,
    actors: 0, journal: 0, scenes: 0, tables: 0, macros: 0, playlists: 0, cards: 0, embeddedFolders: 0};
  function visit(document) {
    for (const key of ["pages", "effects", "items", "results"]) counts[key] += Object.keys(document[key] ?? {}).length;
    counts.activities += Object.keys(document.system?.activities ?? {}).length;
    counts.advancement += Object.keys(document.system?.advancement ?? {}).length;
    // Count actual embedded documents, not references in activity.effects.
    for (const item of document.items ?? []) visit(item);
    for (const key of ["actors", "journal", "scenes", "tables", "macros", "playlists", "cards", "folders"]) {
      const children = Array.isArray(document[key]) ? document[key] : [];
      counts[key === "folders" ? "embeddedFolders" : key] += children.length;
      for (const child of children) visit(child);
    }
  }
  documents.forEach(visit);
  return counts;
}

export async function exportCompendiums() {
  if (!game.user?.isGM) throw new Error("A GM must run the exporter.");
  if (game.version !== "14.368" || game.system.id !== "dnd5e" || game.system.version !== "6.0.3")
    throw new Error("This review requires Foundry 14.368 and dnd5e 6.0.3.");
  if (game.modules.get(TARGET)?.active)
    throw new Error("Disable the Phandelver translation and reload before exporting original sources.");
  if (!game.modules.get(SOURCE)?.active) throw new Error("Activate the official Phandelver & Below first.");
  const picker = foundry.applications.apps.FilePicker;
  if (typeof picker.upload !== "function") throw new Error("FilePicker.upload is unavailable.");
  const files = [];
  const inventory = {
    schemaVersion: 2, exportedAt: new Date().toISOString(),
    foundry: game.version, system: {id: game.system.id, version: game.system.version},
    source: {id: SOURCE, version: game.modules.get(SOURCE).version},
    language: game.settings.get("core", "language"), babeleActive: !!game.modules.get("babele")?.active,
    translationActive: false,
    originalCheck: "No Babele markers or translated pack mappings permitted", packs: []
  };
  for (const name of PACKS) {
    const collection = `${SOURCE}.${name}`;
    const pack = game.packs.get(collection);
    if (!pack) throw new Error(`Missing pack: ${collection}`);
    if (game.babele?.mappedCompendiumFor?.(collection)?.translated) throw new Error(`Translated pack: ${collection}. Disable Babele and reload.`);
    const documents = (await pack.getDocuments()).map(doc => doc.toObject());
    const folders = Array.from(pack.folders ?? [], folder => folder.toObject());
    documents.forEach(doc => assertOriginal(doc, `${collection}.${doc._id}`));
    folders.forEach(folder => assertOriginal(folder, `${collection}.folders.${folder._id}`));
    assertIds(documents, collection);
    assertIds(folders, `${collection}.folders`);
    const payload = {schemaVersion: 1, collection, documentType: pack.documentName, sourceVersion: inventory.source.version, folders, documents};
    const text = JSON.stringify(payload, null, 2) + "\n";
    const digest = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(text));
    const sha256 = Array.from(new Uint8Array(digest), byte => byte.toString(16).padStart(2, "0")).join("");
    const filename = `${collection}.en.json`;
    files.push({filename, text});
    inventory.packs.push({collection, documentType: pack.documentName, filename, sha256, folders: folders.length, ...summarizeDocuments(documents)});
  }
  // Validate every pack before writing any file. Write the inventory last as completion marker.
  const destination = `${DESTINATION}/${inventory.exportedAt.replace(/[:.]/g, "-")}`;
  await picker.createDirectory("data", destination, {}, {notify: false});
  inventory.destination = destination;
  files.push({filename: "inventory.json", text: JSON.stringify(inventory, null, 2) + "\n"});
  for (const {filename, text} of files) {
    const result = await picker.upload("data", destination, new File([text], filename, {type: "application/json"}), {}, {notify: false});
    if (!result?.path) throw new Error(`Upload failed: ${filename}`);
  }
  ui.notifications.info(`Phandelver: exported ${inventory.packs.length} original packs to ${destination}`);
  return inventory;
}
