import assert from 'node:assert/strict';
import {test} from 'node:test';
import {assertOriginal, assertIds, summarizeDocuments} from './export-compendiums.mjs';

test('reject translated content nested in an adventure actor item', () => {
  assert.throws(() => assertOriginal({actors: [{items: [{flags: {babele: {translated: true}}}]}]}), /marker/);
  assert.doesNotThrow(() => assertOriginal({name: 'Goblin', system: {description: {value: '<p>Original</p>'}}}));
});
test('IDs are unique within their collection, not globally', () => {
  assert.doesNotThrow(() => assertIds([{_id: 'a', items: [{_id: 'same'}]}, {_id: 'b', items: [{_id: 'same'}]}], 'actors'));
  assert.throws(() => assertIds([{_id: 'a', pages: [{_id: 'p'}, {_id: 'p'}]}], 'journal'), /duplicate/);
  assert.throws(() => assertIds([{name: 'missing'}], 'items'), /Invalid/);
});
test('nested counts distinguish actual effects from activity effect references', () => {
  const counts = summarizeDocuments([{actors: [{items: [{effects: [{_id: 'e'}], system: {
    activities: {act: {effects: [{_id: 'e'}]}}, advancement: [{_id: 'adv'}]
  }}]}], journal: [{pages: [{_id: 'p'}]}], folders: [{_id: 'f'}]}]);
  assert.equal(counts.effects, 1);
  assert.equal(counts.activities, 1);
  assert.equal(counts.advancement, 1);
  assert.equal(counts.pages, 1);
  assert.equal(counts.embeddedFolders, 1);
});
test('scene journal references are not embedded journal documents', () => {
  const counts = summarizeDocuments([{journal: [{_id: 'j', pages: [{_id: 'p'}]}],
    scenes: [{journal: 'abcdefghijklmnop'}, {journal: null}]}]);
  assert.equal(counts.journal, 1);
  assert.equal(counts.pages, 1);
});
