/**
 * Exporta los cinco compendios de Phandelver & Below desde Foundry VTT.
 *
 * Uso:
 * 1. Abre un mundo con dnd-phandelver-below, Babele y este módulo activos.
 * 2. Inicia sesión como GM y abre las herramientas de desarrollo (F12).
 * 3. Pega este archivo completo en la consola y pulsa Enter.
 * 4. Extrae el ZIP descargado en dev-tools/export/_data/source/.
 *
 * Los datos exportados pertenecen al módulo comercial original y no deben
 * añadirse al repositorio ni redistribuirse.
 */
(async () => {
  const packIds = [
    "dnd-phandelver-below.pbso-player-tables",
    "dnd-phandelver-below.pbso-player-options",
    "dnd-phandelver-below.pbso-items",
    "dnd-phandelver-below.pbso-bestiary",
    "dnd-phandelver-below.pbso-adventures"
  ];

  if (!game.user?.isGM) {
    throw new Error("Debes ejecutar la exportación como GM.");
  }
  if (!game.babele?.extract) {
    throw new Error("Babele no está activo o no ofrece extract().");
  }
  if (typeof JSZip !== "function" || typeof saveAs !== "function") {
    throw new Error("JSZip/saveAs no están disponibles en esta sesión de Foundry.");
  }

  const missing = packIds.filter((id) => !game.packs.get(id));
  if (missing.length) {
    throw new Error(`No se encontraron estos packs: ${missing.join(", ")}`);
  }

  const zip = new JSZip();
  const inventory = {
    generatedAt: new Date().toISOString(),
    foundryVersion: game.version,
    system: {
      id: game.system.id,
      version: game.system.version
    },
    sourceModule: {
      id: "dnd-phandelver-below",
      version: game.modules.get("dnd-phandelver-below")?.version ?? null
    },
    packs: []
  };

  for (const packId of packIds) {
    const pack = game.packs.get(packId);
    const index = await pack.getIndex({ fields: ["type", "folder"] });
    const indexEntries = Array.from(index.values());
    const sourceDocuments = await Promise.all(
      indexEntries.map((entry) => pack.getDocument(entry._id))
    );
    const entries = {};

    for (const document of sourceDocuments) {
      const source = document.toObject();
      entries[document.id] = game.babele.extract(packId, source) ?? {
        name: source.name
      };
    }

    const folders = {};
    pack.folders?.forEach((folder) => {
      const originalName = folder.originalName ?? folder.name;
      if (originalName) folders[originalName] = originalName;
    });

    const payload = {
      label: pack.metadata?.label ?? packId,
      ...(Object.keys(folders).length ? { folders } : {}),
      entries
    };
    zip.file(`translations/${packId}.json`, JSON.stringify(payload, null, 2));

    const documents = indexEntries.map((entry) => ({
      id: entry._id,
      name: entry.name,
      type: entry.type ?? pack.documentName,
      folder: entry.folder ?? null,
      status: "pending"
    }));

    inventory.packs.push({
      id: packId,
      label: pack.metadata?.label ?? packId,
      documentName: pack.documentName,
      count: documents.length,
      documents
    });
  }

  zip.file("inventory.json", JSON.stringify(inventory, null, 2));
  zip.file("README.txt", [
    "Private working export for translate-dnd5e-phandelver-below-es.",
    "Do not commit or redistribute these source files.",
    "Translation entries are keyed by Foundry document ID to preserve duplicate names.",
    "Copy translations/*.json into the module compendium directory only after translation and review."
  ].join("\n"));

  const blob = await zip.generateAsync({ type: "blob" });
  saveAs(blob, "phandelver-below-source-export.zip");
  ui.notifications.info("Exportación de Phandelver & Below completada.");
})();
