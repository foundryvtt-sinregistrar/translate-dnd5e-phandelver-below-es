/** Run validateRuntime() as GM. Reads originals; never modifies official packs. */
const MODULE = 'translate-dnd5e-phandelver-below-es';
const ROOT = `/modules/${MODULE}`;
const SOURCE = 'dev-tools/export/_data/source-current/2026-09-24T19-12-21-788Z';
const PACKS = ['pbso-player-tables','pbso-player-options','pbso-items','pbso-bestiary','pbso-adventures'];
async function json(path) {
  const response = await fetch(`${ROOT}/${path}`, {cache:'no-store'});
  if (!response.ok) throw new Error(`${response.status}: ${path}`);
  return response.json();
}
function require(value, message) { if (!value) throw new Error(message); }
// Foundry's HTML field removes the XHTML slash from bare horizontal rules.
function normalizeHtml(value) { return value.replace(/<hr\s*\/>/g, '<hr>'); }
function verifyItem(item, patch, address) {
  if (!patch) return;
  const mapping={name:'name',requirements:'system.requirements',description:'system.description.value',
    descriptionChat:'system.description.chat',unidentifiedName:'system.unidentified.name',unidentifiedDescription:'system.unidentified.description'};
  for (const [alias,path] of Object.entries(mapping)) {
    if (patch[alias] !== undefined) require(path.split('.').reduce((v,k)=>v?.[k],item)===patch[alias],`${address}.${alias}`);
  }
  function nested(actual, expected, at) {
    for (const [key,value] of Object.entries(expected ?? {})) {
      if (typeof value==='string') require(actual?.[key]===value,`${at}.${key}`);
      else nested(actual?.[key],value,`${at}.${key}`);
    }
  }
  for (const [id,patchActivity] of Object.entries(patch.activities ?? {})) nested(item.system.activities[id],patchActivity,`${address}.activities.${id}`);
  for (const [id,patchEffect] of Object.entries(patch.effects ?? {})) nested(item.effects.find(e=>e._id===id),patchEffect,`${address}.effects.${id}`);
}
function verifyActor(actor,patch,address) {
  if (!patch) return;
  for (const [alias,path] of Object.entries({name:'name',tokenName:'prototypeToken.name',biography:'system.details.biography.value',
    biographyPublic:'system.details.biography.public',alignment:'system.details.alignment',habitat:'system.details.habitat.custom',
    creatureType:'system.details.type.custom',creatureSubtype:'system.details.type.subtype',languages:'system.traits.languages.custom',
    senses:'system.attributes.senses.special'})) {
    if (patch[alias]!==undefined) require(path.split('.').reduce((v,k)=>v?.[k],actor)===patch[alias],`${address}.${alias}`);
  }
  for (const [id,item] of Object.entries(patch.items ?? {})) verifyItem(actor.items.find(i=>i._id===id),item,`${address}.items.${id}`);
  for (const [id,effect] of Object.entries(patch.effects ?? {})) {
    const actual=actor.effects.find(e=>e._id===id);
    for (const [key,value] of Object.entries(effect)) require(actual?.[key]===value,`${address}.effects.${id}.${key}`);
  }
}

export async function validateRuntime({pilot = false} = {}) {
  require(game.user.isGM && game.babele && game.modules.get(MODULE)?.active, 'GM, Babele and translation required');
  const report = {date:new Date().toISOString(), foundry:game.version, system:game.system.version,
    babele:game.modules.get('babele').version, source:SOURCE,
    activeModules:[...game.modules.values()].filter(m => m.active).map(m => ({id:m.id,version:m.version})),
    checks:[], errors:[], pilot:[], status:'running'};
  await write('runtime-validation.json', report);
  let journalPilot;
  let itemPilot;
  for (const name of PACKS) {
    const collection = `dnd-phandelver-below.${name}`;
    const source = await json(`${SOURCE}/${collection}.en.json`);
    const payload = await json(`compendium/${collection}.json`);
    const translatedDocuments = [];
    for (const original of source.documents) {
      try {
        const result = game.babele.translate(collection, foundry.utils.deepClone(original));
        const patch = payload.entries[original._id];
        if (source.documentType==='Item') verifyItem(result,patch,original._id);
        if (source.documentType==='Actor') verifyActor(result,patch,original._id);
        if (patch?.name !== undefined) require(result.name === patch.name, `Root name: ${original._id}`);
        if (source.documentType === 'Item' && patch?.description !== undefined) {
          require(result.system.description.value === patch.description, `Item description: ${original._id}`);
        }
        for (const [id, advancement] of Object.entries(patch?.advancement ?? {})) {
          require(result.system.advancement[id]?.name === advancement.name, `Advancement name: ${original._id}.${id}`);
        }
        if (collection.endsWith('.pbso-player-options') && original._id === 'pbsoCharlatan000') itemPilot = result;
        if (source.documentType === 'Adventure') {
          for (const [id,item] of Object.entries(patch.items ?? {})) verifyItem(result.items.find(i=>i._id===id),item,`Adventure.items.${id}`);
          for (const [id,actor] of Object.entries(patch.actors ?? {})) verifyActor(result.actors.find(a=>a._id===id),actor,`Adventure.actors.${id}`);
          for (const field of ['description','caption']) {
            if (patch[field] !== undefined) require(result[field] === patch[field], `Adventure ${field}`);
          }
          for (const folder of result.folders) {
            if (patch.folders?.[folder._id] !== undefined) require(folder.name === patch.folders[folder._id], `Folder: ${folder._id}`);
          }
          for (const journal of result.journal) {
            const jp = patch.journals?.[journal._id];
            if (!jp) continue;
            if (jp.name !== undefined) require(journal.name === jp.name, `Journal: ${journal._id}`);
            for (const page of journal.pages) {
              const pp = jp.pages?.[page._id];
              if (!pp) continue;
              if (pp.name !== undefined) require(page.name === pp.name, `Page name: ${journal._id}.${page._id}`);
              if (pp.text !== undefined) require(page.text.content === pp.text, `Page text: ${journal._id}.${page._id}`);
              if (pp.caption !== undefined) require(page.image.caption === pp.caption, `Page caption: ${journal._id}.${page._id}`);
            }
            if (journal._id === 'pbsoWelcomeToPha') journalPilot = journal;
          }
        }
        if (source.documentType === 'RollTable' && patch?.results) {
          for (const row of result.results) {
            const tr = patch.results[row._id] ?? patch.results[row.range.join('-')];
            if (tr?.description !== undefined) require(row.description === tr.description, `Table result: ${row._id}`);
          }
        }
        // Constructors migrate/normalize their input. Preserve the actual Babele output.
        const document = new (getDocumentClass(source.documentType))(foundry.utils.deepClone(result), {pack:collection});
        document.validate({strict:true});
        translatedDocuments.push(result);
        report.checks.push({collection,id:original._id});
      } catch(error) {report.errors.push({collection,id:original._id,error:error.message});}
    }
    await write(`${name}.runtime.json`, {documents:translatedDocuments});
  }
  if (pilot && !report.errors.length) {
    try {
    require(journalPilot, 'Missing journal pilot');
    let folder = game.folders.find(f => f.type === 'JournalEntry' && f.name === 'Phandelver - Revision');
    if (!folder) folder = await Folder.create({name:'Phandelver - Revision',type:'JournalEntry'});
    let document = game.journal.find(j => j.getFlag(MODULE,'reviewPilot') === journalPilot._id);
    if (!document) {
      const copy = foundry.utils.deepClone(journalPilot);
      const sourceId = copy._id;
      delete copy._id;
      copy.folder = folder.id;
      copy.flags ??= {};
      copy.flags[MODULE] = {reviewPilot:sourceId};
      document = await JournalEntry.create(copy, {renderSheet:false});
    }
    require(document.name === journalPilot.name, 'Imported pilot name mismatch');
    const first = journalPilot.pages.find(p => p._id === 'UOqr9enScoY6VESg');
    require(document.pages.get(first._id)?.text.content === first.text.content, 'Imported pilot text mismatch');
    report.pilot.push({id:document.id,name:document.name});
    document.sheet.render(true);
    require(itemPilot, 'Missing background pilot');
    let itemFolder = game.folders.find(f => f.type === 'Item' && f.name === 'Phandelver - Revision');
    if (!itemFolder) itemFolder = await Folder.create({name:'Phandelver - Revision',type:'Item'});
    let item = game.items.find(i => i.getFlag(MODULE,'reviewPilot') === itemPilot._id);
    if (!item) {
      const copy = foundry.utils.deepClone(itemPilot);
      const sourceId = copy._id;
      delete copy._id;
      copy.folder = itemFolder.id;
      copy.flags ??= {};
      copy.flags[MODULE] = {reviewPilot:sourceId};
      item = await Item.create(copy, {renderSheet:false});
    }
    const imported = item.toObject();
    await write('background-pilot.runtime.json', {expected:itemPilot,imported});
    require(imported.name === itemPilot.name, 'Imported background name mismatch');
    require(normalizeHtml(imported.system.description.value) === normalizeHtml(itemPilot.system.description.value), 'Imported background description mismatch');
    for (const [id, advancement] of Object.entries(itemPilot.system.advancement)) {
      require(imported.system.advancement[id]?.name === advancement.name, `Imported advancement mismatch: ${id}`);
    }
    report.pilot.push({id:item.id,name:item.name,type:'Item'});
    item.sheet.render(true);
    } catch (error) {
      report.errors.push({pilot:true,error:error.message});
    }
  }
  report.status = report.errors.length ? 'failed' : 'passed';
  await write('runtime-validation.json', report);
  ui.notifications.info(`Phandelver: ${report.checks.length} documentos validados; ${report.errors.length} errores.`,{permanent:true});
  return report;
}
async function write(filename, data) {
  const result = await foundry.applications.apps.FilePicker.upload('data', `modules/${MODULE}/dev-tools/export/_data`,
    new File([JSON.stringify(data,null,2)+'\n'],filename,{type:'application/json'}),{}, {notify:false});
  require(result?.path, `Cannot save ${filename}`);
}
