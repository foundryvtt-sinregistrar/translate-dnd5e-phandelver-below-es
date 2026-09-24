import {test} from 'node:test';
import assert from 'node:assert/strict';
import {translateItem,translateActor,translateScene,phandelverTables,phandelverMacros} from '../../scripts/document-text.mjs';
import {reviewedDocumentConverter} from '../../scripts/document-fallback.mjs';

test('reviewed proper names override fallback even when unchanged from English',()=>{
  const fallback=[{_id:'droop',name:'Goblin',prototypeToken:{name:'Goblin'},items:[{_id:'sword',name:'Espada',system:{description:{value:'Descripción auxiliar'}}}]}];
  const converter=reviewedDocumentConverter({translate:()=>structuredClone(fallback)});
  const result=converter.translate({params:{documentType:'Actor'},translation:{droop:{name:'Droop',tokenName:'Droop'}}});
  assert.equal(result[0].name,'Droop');assert.equal(result[0].prototypeToken.name,'Droop');
  assert.deepEqual(result[0].items,fallback[0].items);
});

test('item text overlay preserves combat data, identities, order and source',()=>{
  const source={_id:'weapon',name:'Sword',type:'weapon',system:{description:{value:'Original',chat:''},
    unidentified:{name:'Unknown',description:'Iron'},activities:{attack:{_id:'attack',name:'Strike',
      activation:{condition:'On a hit',type:'action'},damage:{parts:[{number:2,denomination:6}]}}},
    advancement:{a:{_id:'a',name:'Equipment',configuration:{items:['Item.x']}}}},
    effects:[{_id:'effect',name:'Bonus',changes:[{key:'system.attributes.ac.bonus',value:'1'}]}]};
  const before=structuredClone(source);
  const result=translateItem(source,{name:'Espada',_id:'wrong',type:'spell',system:{damage:999},
    unidentifiedName:'Desconocida',activities:{attack:{name:'Golpe',activation:{condition:'Al impactar',type:'bonus'},damage:{parts:[]}},extra:{name:'Extra'}},
    advancement:{a:{name:'Equipo',configuration:{items:[]}}},effects:{effect:{name:'Bonificación',changes:[]}}});
  const expected=structuredClone(source);
  expected.name='Espada';expected.system.unidentified.name='Desconocida';
  expected.system.activities.attack.name='Golpe';expected.system.activities.attack.activation.condition='Al impactar';
  expected.system.advancement.a.name='Equipo';expected.effects[0].name='Bonificación';
  assert.deepEqual(result,expected);assert.deepEqual(source,before);
});

test('actor and scene overlays handle nested items, token deltas and typed behaviors only',()=>{
  const actor={_id:'a',name:'Guard',system:{details:{alignment:'Neutral'},attributes:{hp:{value:12}}},items:[{_id:'i',name:'Spear',system:{description:{value:'Sharp'},quantity:1}}]};
  const scene={_id:'s',name:'Cave',navName:'Cave',width:2000,notes:[{_id:'n',text:'Entrance',x:50}],tokens:[{_id:'t',name:'Guard',actorId:'a',delta:actor}],
    regions:[{_id:'r',name:'Exit',behaviors:[{_id:'b',name:'Travel',type:'teleportToken',system:{destination:'Region.x',dialog:{revealed:'Go?',unrevealed:'Enter?'}}},
      {_id:'script',name:'Script',type:'executeScript',system:{source:'console.log(1)'}}]}]};
  const before=structuredClone(scene);
  const result=translateScene(scene,{name:'Cueva',width:1,notes:{n:{text:'Entrada',x:999}},tokens:{t:{name:'Guardia',actorId:'bad',delta:{alignment:'Neutral',items:{i:{name:'Lanza',description:'Afilada',quantity:99}}}}},
    regions:{r:{name:'Salida',behaviors:{b:{name:'Viaje',revealedDialog:'¿Ir?',system:{destination:'bad'}},script:{name:'Guion',text:'bad',system:{source:'bad'}}}}}});
  const expected=structuredClone(scene);expected.name='Cueva';expected.notes[0].text='Entrada';expected.tokens[0].name='Guardia';
  expected.tokens[0].delta.items[0].name='Lanza';expected.tokens[0].delta.items[0].system.description.value='Afilada';
  expected.regions[0].name='Salida';expected.regions[0].behaviors[0].name='Viaje';expected.regions[0].behaviors[0].system.dialog.revealed='¿Ir?';expected.regions[0].behaviors[1].name='Guion';
  assert.deepEqual(result,expected);assert.deepEqual(scene,before);
  assert.equal(translateActor(actor,null),actor);
});

test('table weights and macro commands remain protected',()=>{
  const tables=[{_id:'t',name:'Encounter',formula:'1d6',results:[{_id:'r',name:'Wolf',description:'A wolf',range:[1,6],weight:6,documentUuid:'Actor.x'}]}];
  const translated=phandelverTables(tables,{t:{name:'Encuentro',formula:'1d100',results:{r:{name:'Lobo',description:'Un lobo',range:[0,0],weight:0,documentUuid:'bad'}}}});
  assert.deepEqual(translated,[{...tables[0],name:'Encuentro',results:[{...tables[0].results[0],name:'Lobo',description:'Un lobo'}]}]);
  assert.deepEqual(phandelverMacros([{_id:'m',name:'Open',command:'original()'}],{m:{name:'Abrir',command:'changed()'}}),[{_id:'m',name:'Abrir',command:'original()'}]);
});
