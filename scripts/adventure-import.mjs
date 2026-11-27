/** Restore reviewed labels after other modules' post-import synchronization. */
export async function restoreAdventureLabels(adventure, result) {
  let changed = 0;
  for (const scene of [...(result.created?.Scene ?? []), ...(result.updated?.Scene ?? [])]) {
    const original = Array.from(adventure.scenes).find(s => s._id === scene.id);
    if (!original) continue;
    const updates = [];
    for (const token of scene.tokens) {
      const name = original.tokens.find(t => t._id === token.id)?.name;
      // Babele queues token updates from importAdventure without awaiting them.
      // The current name can still match while a generic actor name is in flight.
      // Always queue the reviewed name after those writes, even when equal now.
      if (typeof name === 'string') updates.push({_id:token.id, name});
    }
    if (updates.length) {
      // Do not let Foundry drop equal-name writes before the pending sync lands.
      await scene.updateEmbeddedDocuments('Token', updates, {diff:false});
      changed += updates.length;
    }
  }
  return changed;
}

export function configureAdventureImport(adventure, options) {
  if (adventure.pack !== 'dnd-phandelver-below.pbso-adventures') return;
  if (game.settings.get('core', 'language')?.split('-')[0].toLowerCase() !== 'es') return;
  options.postImport ??= [];
  options.postImport.push(function (result) { return restoreAdventureLabels(this, result); });
}

if (typeof Hooks !== 'undefined') Hooks.on('preImportAdventure', configureAdventureImport);
