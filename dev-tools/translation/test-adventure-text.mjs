import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {phandelverFoldersById, phandelverJournalsById} from '../../scripts/adventure-text.mjs';

test('same-named folders keep independent translations and structure', () => {
  const source = [{_id:'a', name:'Chapter 1', folder:'parent'}, {_id:'b', name:'Chapter 1'}];
  const result = phandelverFoldersById(source, {a:'Capítulo 1'});
  assert.deepEqual(result, [{_id:'a', name:'Capítulo 1', folder:'parent'}, source[1]]);
  assert.equal(source[0].name, 'Chapter 1');
});
test('journal text conversion cannot overwrite IDs, links, image resources or mechanics', () => {
  const source = [{_id:'j', name:'Atlas', pages:[{_id:'p', name:'Map', src:'map.webp', text:{content:'EN', format:1}}]}];
  const patch = {j:{_id:'bad', name:'Atlas ES', pages:{p:{_id:'bad', name:'Mapa', src:'bad.webp', text:'ES'}}}};
  const result = phandelverJournalsById(source, patch);
  assert.deepEqual(result, [{_id:'j', name:'Atlas ES', pages:[{_id:'p', name:'Mapa', src:'map.webp', text:{content:'ES', format:1}}]}]);
  assert.equal(source[0].pages[0].text.content, 'EN');
});

const root = new URL('../../', import.meta.url);
const read = path => JSON.parse(fs.readFileSync(new URL(path, root), 'utf8'));
const base = new URL('dev-tools/export/_data/source-current/', root);
const exports = fs.existsSync(base) ? fs.readdirSync(base).sort().filter(name => fs.existsSync(new URL(`${name}/inventory.json`, base))) : [];
test('all existing translations apply to real original IDs without other field changes', {skip: !exports.length}, () => {
  const source = read(`dev-tools/export/_data/source-current/${exports.at(-1)}/dnd-phandelver-below.pbso-adventures.en.json`).documents[0];
  const patch = read('compendium/dnd-phandelver-below.pbso-adventures.json').entries[source._id];
  const snapshot = structuredClone(source);
  const folders = phandelverFoldersById(source.folders, patch.folders);
  const journals = phandelverJournalsById(source.journal, patch.journals);
  let pages = 0;
  for (const folder of folders) {
    assert.equal(folder.name, patch.folders[folder._id]);
    folder.name = source.folders.find(f => f._id === folder._id).name;
  }
  for (const journal of journals) {
    const original = source.journal.find(j => j._id === journal._id);
    assert.equal(journal.name, patch.journals[journal._id].name);
    journal.name = original.name;
    for (const page of journal.pages) {
      const text = patch.journals[journal._id].pages?.[page._id];
      if (!text) continue;
      pages++;
      const originalPage = original.pages.find(p => p._id === page._id);
      if (text.name !== undefined) {assert.equal(page.name,text.name); page.name=originalPage.name;}
      if (text.text !== undefined) {assert.equal(page.text.content,text.text); page.text.content=originalPage.text.content;}
      if (text.caption !== undefined) {assert.equal(page.image.caption,text.caption); page.image=originalPage.image;}
    }
  }
  assert.equal(pages,310);
  assert.equal(folders.length,71);
  assert.equal(journals.length,61);
  assert.deepEqual(folders,source.folders);
  assert.deepEqual(journals,source.journal);
  assert.deepEqual(source,snapshot);
});
