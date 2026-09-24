import {phandelverFoldersById, phandelverJournalsById} from './adventure-text.mjs';
import {phandelverAdvancementNames} from './item-text.mjs';
import * as documentText from './document-text.mjs';

Hooks.once('babele.init', babele => {
  const converters=Object.fromEntries(Object.entries(documentText).filter(([name])=>name.startsWith('phandelver')));
  babele.registerConverters({phandelverFoldersById, phandelverJournalsById, phandelverAdvancementNames, ...converters});
});
