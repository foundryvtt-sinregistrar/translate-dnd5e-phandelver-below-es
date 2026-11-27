import {test} from 'node:test';
import assert from 'node:assert/strict';
import {restoreAdventureLabels, configureAdventureImport} from '../../scripts/adventure-import.mjs';

test('restore custom token labels only in the imported scenes', async () => {
  const writes = [];
  const scene = {id:'s', tokens:[{id:'t',name:'Commoner'},{id:'u',name:'Untouched'}],
    updateEmbeddedDocuments:async (type,data) => writes.push({type,data})};
  const adventure = {scenes:new Set([{_id:'s',tokens:[{_id:'t',name:'Mirna Dendrar'}]}])};
  assert.equal(await restoreAdventureLabels(adventure,{created:{Scene:[scene]}}),1);
  assert.deepEqual(writes,[{type:'Token',data:[{_id:'t',name:'Mirna Dendrar'}]}]);
  assert.equal(await restoreAdventureLabels(adventure,{created:{}}),0);
});

test('post-import correction is restricted to Spanish PBSO imports', () => {
  globalThis.game={settings:{get:()=> 'en'}};
  const options={};
  configureAdventureImport({pack:'dnd-phandelver-below.pbso-adventures'},options);
  assert.equal(options.postImport,undefined);
  game.settings.get=()=> 'es-ES';
  configureAdventureImport({pack:'other'},options);
  assert.equal(options.postImport,undefined);
  configureAdventureImport({pack:'dnd-phandelver-below.pbso-adventures'},options);
  assert.equal(options.postImport.length,1);
  delete globalThis.game;
});

test('reviewed labels survive an in-flight actor-name synchronization', async () => {
  const token = {id:'t',name:'Mirna Dendrar'};
  const synchronization = Promise.resolve().then(() => { token.name = 'Commoner'; });
  const scene = {id:'s',tokens:[token],updateEmbeddedDocuments:async (type, updates, options) => {
    assert.equal(options.diff,false, 'Equal current values must still be written');
    await synchronization;
    assert.equal(type,'Token');
    for (const update of updates) token.name = update.name;
  }};
  const adventure = {scenes:[{_id:'s',tokens:[{_id:'t',name:'Mirna Dendrar'}]}]};
  assert.equal(await restoreAdventureLabels(adventure,{created:{Scene:[scene]}}),1);
  await synchronization;
  assert.equal(token.name,'Mirna Dendrar');
});
