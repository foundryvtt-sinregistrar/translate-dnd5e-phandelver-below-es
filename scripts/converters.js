import {phandelverFoldersById, phandelverJournalsById} from './adventure-text.mjs';

Hooks.once('babele.init', babele => {
  babele.registerConverters({phandelverFoldersById, phandelverJournalsById});
});
