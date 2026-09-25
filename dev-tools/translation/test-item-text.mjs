import {test} from 'node:test';
import assert from 'node:assert/strict';
import {phandelverAdvancementNames} from '../../scripts/item-text.mjs';

test('keyed advancements retain grants and configuration despite extra patch fields', () => {
  const source = {a:{_id:'a',name:'Equipment',configuration:{items:[{uuid:'Item.x'}]},value:{chosen:['x']}}};
  const snapshot = structuredClone(source);
  const result = phandelverAdvancementNames(source, {a:{name:'Equipo',_id:'bad',configuration:{},value:{}}});
  assert.deepEqual(result,{a:{...snapshot.a,name:'Equipo'}});
  assert.deepEqual(source,snapshot);
  assert.deepEqual(phandelverAdvancementNames(source,{a:{name:42}}),source);
});

test('legacy advancement arrays keep their shape and title field', () => {
  const source = [{_id:'a',title:'Feature',type:'ItemGrant'}, {_id:'b',title:'Other'}];
  assert.deepEqual(phandelverAdvancementNames(source,{a:{name:'Rasgo'}}),
    [{_id:'a',title:'Rasgo',type:'ItemGrant'},source[1]]);
  assert.equal(source[0].title,'Feature');
});
