import {phandelverActors,phandelverItems} from './document-text.mjs';

/** Preserve Babele fallback, then reapply explicit IDs, including unchanged names. */
export function reviewedDocumentConverter(delegate) {
  return {
    prepare(context) { return delegate.prepare?.(context); },
    translate(context) {
      const translated=delegate.translate(context);
      const overlay={Actor:phandelverActors,Item:phandelverItems}[context.params.documentType];
      return overlay ? overlay(translated,context.translation) : translated;
    },
    extract(context) { return delegate.extract?.(context); }
  };
}
