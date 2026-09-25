import {phandelverFoldersById, phandelverJournalsById} from './adventure-text.mjs';
import {phandelverAdvancementNames} from './item-text.mjs';
import * as documentText from './document-text.mjs';
import {reviewedDocumentConverter} from './document-fallback.mjs';

Hooks.once('babele.init', babele => {
  const converters=Object.fromEntries(Object.entries(documentText).filter(([name])=>name.startsWith('phandelver')));
  const documentConverter=babele.converterRegistry?.named('document');
  if (documentConverter) converters.phandelverDocuments=reviewedDocumentConverter(documentConverter);
  babele.registerConverters({phandelverFoldersById, phandelverJournalsById, phandelverAdvancementNames, ...converters});
});
