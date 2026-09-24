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

export async function validateRuntime({pilot = false} = {}) {
  require(game.user.isGM && game.babele && game.modules.get(MODULE)?.active, 'GM, Babele and translation required');
  const report = {date:new Date().toISOString(), foundry:game.version, system:game.system.version,
    babele:game.modules.get('babele').version, checks:[], errors:[], pilot:[]};
  let journalPilot;
  for (const name of PACKS) {
    const collection = `dnd-phandelver-below.${name}`;
    const source = await json(`${SOURCE}/${collection}.en.json`);
    const payload = await json(`compendium/${collection}.json`);
    const translatedDocuments = [];
    for (const original of source.documents) {
      try {
        const result = game.babele.translate(collection, foundry.utils.deepClone(original));
        const patch = payload.entries[original._id];
        if (patch?.name !== undefined) require(result.name === patch.name, `Root name: ${original._id}`);
        if (source.documentType === 'Adventure') {
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
        const document = new (getDocumentClass(source.documentType))(result, {pack:collection});
        document.validate({strict:true});
        translatedDocuments.push(result);
        report.checks.push({collection,id:original._id});
      } catch(error) {report.errors.push({collection,id:original._id,error:error.message});}
    }
    await write(`${name}.runtime.json`, {documents:translatedDocuments});
  }
  if (pilot && !report.errors.length) {
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
  }
  await write('runtime-validation.json', report);
  ui.notifications.info(`Phandelver: ${report.checks.length} documentos validados; ${report.errors.length} errores.`,{permanent:true});
  return report;
}
async function write(filename, data) {
  const result = await foundry.applications.apps.FilePicker.upload('data', `modules/${MODULE}/dev-tools/export/_data`,
    new File([JSON.stringify(data,null,2)+'\n'],filename,{type:'application/json'}),{}, {notify:false});
  require(result?.path, `Cannot save ${filename}`);
}
