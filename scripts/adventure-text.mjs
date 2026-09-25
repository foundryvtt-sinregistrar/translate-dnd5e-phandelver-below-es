/** Apply only reviewed text fields to exact IDs. Never merge technical fields. */
export function phandelverFoldersById(source, translation) {
  if (!Array.isArray(source) || !translation) return source;
  return source.map(folder => typeof translation[folder._id] === 'string'
    ? {...folder, name: translation[folder._id]} : folder);
}

export function phandelverJournalsById(source, translation) {
  if (!Array.isArray(source) || !translation) return source;
  return source.map(journal => {
    const patch = translation[journal._id];
    if (!patch || typeof patch !== 'object') return journal;
    const result = {...journal};
    if (typeof patch.name === 'string') result.name = patch.name;
    if (Array.isArray(journal.pages) && patch.pages) {
      result.pages = journal.pages.map(page => {
        const text = patch.pages[page._id];
        if (!text || typeof text !== 'object') return page;
        const translated = {...page};
        if (typeof text.name === 'string') translated.name = text.name;
        if (typeof text.text === 'string') translated.text = {...page.text, content: text.text};
        if (typeof text.caption === 'string') translated.image = {...page.image, caption: text.caption};
        return translated;
      });
    }
    return result;
  });
}
