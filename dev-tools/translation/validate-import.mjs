/** Read-only world inspection after importing Adventure through its normal UI. */
const MODULE = 'translate-dnd5e-phandelver-below-es';
const DIRECTORY = `modules/${MODULE}/dev-tools/export/_data`;

async function write(name, value) {
  return foundry.applications.apps.FilePicker.upload('data', DIRECTORY,
    new File([JSON.stringify(value, null, 2) + '\n'], name, {type:'application/json'}), {}, {notify:false});
}

export async function validateImport() {
  if (!game.user.isGM) throw new Error('GM required');
  const expected = (await (await fetch(`/${DIRECTORY}/pbso-adventures.runtime.json`, {cache:'no-store'})).json()).documents[0];
  const report = {date:new Date().toISOString(), foundry:game.version, system:game.system.version,
    world:game.world.id, counts:{}, missing:[], referenceCount:0, unresolved:[], status:'running'};
  await write('import-validation.json', report);
  const actual = {_id:expected._id, name:expected.name, description:expected.description, caption:expected.caption};
  const requests = new Map();
  function references(value, relative) {
    if (typeof value === 'string') {
      for (const match of value.matchAll(/@(?:UUID|Embed)\[([^\]]+)\]/g)) {
        const uuid = match[1].split(/\s/)[0].split('#')[0];
        const key = uuid.startsWith('.') ? `${relative.uuid}|${uuid}` : uuid;
        if (!requests.has(key)) requests.set(key, {uuid, context:relative.uuid, relative});
      }
    } else if (Array.isArray(value)) value.forEach(v => references(v, relative));
    else if (value && typeof value === 'object') Object.values(value).forEach(v => references(v, relative));
  }
  for (const key of ['actors','items','journal','scenes','tables','macros','folders']) {
    actual[key] = [];
    for (const original of expected[key]) {
      const doc = game[key].get(original._id);
      if (!doc) {report.missing.push(`${key}.${original._id}`); continue;}
      actual[key].push(doc.toObject());
      if (key === 'journal') for (const page of doc.pages) references(page.toObject(), page);
      else if (key === 'actors') {
        references(doc.system.details?.biography, doc);
        for (const item of doc.items) references(item.toObject(), item);
      } else if (key === 'items') references(doc.toObject(), doc);
      else if (key === 'tables') references(doc.toObject(), doc);
    }
    report.counts[key] = {expected:expected[key].length, imported:actual[key].length};
  }
  await write('adventure-imported.runtime.json', {documents:[actual]});
  const queue = [...requests.values()];
  report.referenceCount = queue.length;
  let next = 0;
  await Promise.all(Array.from({length:8}, async () => {
    while (next < queue.length) {
      const row = queue[next++];
      try {
        const doc = await fromUuid(row.uuid, {relative:row.relative});
        if (!doc) report.unresolved.push({uuid:row.uuid, context:row.context});
      } catch (error) {
        report.unresolved.push({uuid:row.uuid, context:row.context, error:error.message});
      }
    }
  }));
  report.unresolved.sort((a,b) => a.uuid.localeCompare(b.uuid));
  report.status = report.missing.length ? 'failed' : 'imported';
  await write('import-validation.json', report);
  ui.notifications.info(`Phandelver: importación comprobada; ${report.missing.length} documentos ausentes; ${report.unresolved.length} referencias pendientes.`, {permanent:true});
  return report;
}
