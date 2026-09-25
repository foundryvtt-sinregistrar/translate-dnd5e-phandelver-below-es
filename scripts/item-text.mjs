/** Translate advancement labels by ID, preserving both legacy and keyed storage. */
export function phandelverAdvancementNames(source, translation) {
  if (!source || typeof source !== 'object' || !translation) return source;
  const translate = (advancement, key) => {
    if (!advancement || typeof advancement !== 'object') return advancement;
    const patch = translation[advancement._id ?? key];
    if (typeof patch?.name !== 'string') return advancement;
    if (Object.hasOwn(advancement, 'name')) return {...advancement, name:patch.name};
    if (Object.hasOwn(advancement, 'title')) return {...advancement, title:patch.name};
    return advancement;
  };
  if (Array.isArray(source)) return source.map(advancement => translate(advancement));
  return Object.fromEntries(Object.entries(source).map(([key,value]) => [key,translate(value,key)]));
}
