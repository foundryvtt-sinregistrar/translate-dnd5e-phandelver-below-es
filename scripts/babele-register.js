/** Register this Spanish translation after Babele and core settings exist. */
import './converters.js';

Hooks.once("babele.init", (babele) => {
  Hooks.once("setup", () => {
    const language = game.settings.get("core", "language");
    if (typeof language !== "string" || language.split("-")[0].toLowerCase() !== "es") return;
    for (const lang of new Set([language, "es"])) {
      babele.register({module: "translate-dnd5e-phandelver-below-es", lang, dir: "compendium"});
    }
  });
});
