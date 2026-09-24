import {phandelverFoldersById, phandelverJournalsById} from './adventure-text.mjs';
import {phandelverAdvancementNames} from './item-text.mjs';

Hooks.once('babele.init', babele => {
  babele.registerConverters({phandelverFoldersById, phandelverJournalsById, phandelverAdvancementNames});
});
