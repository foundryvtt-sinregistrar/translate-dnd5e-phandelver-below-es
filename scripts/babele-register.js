/** Registra en Babele los compendios de Phandelver & Below. */
Hooks.on("init", () => {
  const babele = game?.babele;
  if (!babele) return;

  const current = game.i18n?.lang ?? "es";
  const langs = Array.from(new Set([current, current.split("-")[0]]));
  const compendium = {
    "dnd-phandelver-below.pbso-adventures": {
      label: "Phandelver y Más Abajo - La aventura",
      path: "dnd-phandelver-below.pbso-adventures.json"
    },
    "dnd-phandelver-below.pbso-bestiary": {
      label: "Phandelver y Más Abajo - Bestiario",
      path: "dnd-phandelver-below.pbso-bestiary.json"
    },
    "dnd-phandelver-below.pbso-items": {
      label: "Phandelver y Más Abajo - Objetos",
      path: "dnd-phandelver-below.pbso-items.json"
    },
    "dnd-phandelver-below.pbso-player-options": {
      label: "Phandelver y Más Abajo - Opciones de personaje",
      path: "dnd-phandelver-below.pbso-player-options.json"
    },
    "dnd-phandelver-below.pbso-player-tables": {
      label: "Phandelver y Más Abajo - Tablas de trasfondo",
      path: "dnd-phandelver-below.pbso-player-tables.json"
    }
  };

  for (const lang of langs) {
    babele.register({
      module: "translate-dnd5e-phandelver-below-es",
      lang,
      dir: "compendium",
      compendium
    });
  }
});
