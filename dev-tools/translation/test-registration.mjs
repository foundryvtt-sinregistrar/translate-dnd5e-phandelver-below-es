import {test} from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import fs from 'node:fs';

const script = fs.readFileSync(new URL('../../scripts/babele-register.js', import.meta.url), 'utf8');
for (const [language, expected] of [['en', []], ['fr', []], ['es', ['es']], ['es-ES', ['es-ES', 'es']]]) {
  test(`registration lifecycle: ${language}`, () => {
    const hooks = new Map();
    const registrations = [];
    let settingsReady = false;
    vm.runInNewContext(script, {
      Hooks: {once: (event, callback) => hooks.set(event, callback)},
      game: {settings: {get: () => {assert.ok(settingsReady); return language;}}}
    });
    hooks.get('babele.init')({register: source => registrations.push(source)});
    assert.equal(registrations.length, 0);
    settingsReady = true;
    hooks.get('setup')();
    assert.deepEqual(registrations.map(r => r.lang), expected);
    assert.ok(registrations.every(r => r.dir === 'compendium'));
  });
}
