/** ID-based text overlays. Unknown fields, scripts and game data are never merged. */
const itemFields = {
  name:'name', requirements:'system.requirements', description:'system.description.value',
  descriptionChat:'system.description.chat', unidentifiedName:'system.unidentified.name',
  unidentifiedDescription:'system.unidentified.description'
};
const actorFields = {
  name:'name', tokenName:'prototypeToken.name', biography:'system.details.biography.value',
  biographyPublic:'system.details.biography.public', alignment:'system.details.alignment',
  habitat:'system.details.habitat.custom', creatureType:'system.details.type.custom',
  creatureSubtype:'system.details.type.subtype', languages:'system.traits.languages.custom',
  senses:'system.attributes.senses.special'
};
const activityFields = ['name','activation.condition','description.chatFlavor','description.value',
  'range.special','roll.name','target.affects.special'];
function read(object, path) { return path.split('.').reduce((value,key) => value?.[key],object); }
function write(object, path, value) {
  const keys=path.split('.');
  const leaf=keys.pop();
  for (const key of keys) object=object[key] ??= {};
  object[leaf]=value;
}
function overlay(source, patch, mapping) {
  if (!source || typeof source !== 'object' || !patch || typeof patch !== 'object') return source;
  const result=structuredClone(source);
  for (const [alias,path] of Object.entries(mapping)) {
    const value=read(patch,alias);
    if (typeof value==='string' && typeof read(source,path)==='string') write(result,path,value);
  }
  return result;
}
function byId(source, patch, apply) {
  if (!source || !patch || typeof source !== 'object' || typeof patch !== 'object') return source;
  const convert=(value,key) => apply(value,patch[value?._id ?? key]);
  return Array.isArray(source) ? source.map(value=>convert(value))
    : Object.fromEntries(Object.entries(source).map(([key,value])=>[key,convert(value,key)]));
}
export const phandelverEffects = (source,patch) => byId(source,patch,
  (value,text)=>overlay(value,text,{name:'name',description:'description'}));
export const phandelverActivities = (source,patch) => byId(source,patch,
  (value,text)=>overlay(value,text,Object.fromEntries(activityFields.map(path=>[path,path]))));
export function translateItem(source,patch) {
  const result=overlay(source,patch,itemFields);
  if (result===source) return source;
  if (source.effects) result.effects=phandelverEffects(source.effects,patch.effects);
  if (source.system?.activities) result.system.activities=phandelverActivities(source.system.activities,patch.activities);
  if (source.system?.advancement) result.system.advancement=byId(source.system.advancement,patch.advancement,
    (value,text)=>overlay(value,text,{name:Object.hasOwn(value,'name')?'name':'title',hint:'hint'}));
  return result;
}
export const phandelverItems = (source,patch) => byId(source,patch,translateItem);
export function translateActor(source,patch) {
  const result=overlay(source,patch,actorFields);
  if (result===source) return source;
  if (source.items) result.items=phandelverItems(source.items,patch.items);
  if (source.effects) result.effects=phandelverEffects(source.effects,patch.effects);
  return result;
}
export const phandelverActors = (source,patch) => byId(source,patch,translateActor);
export function translateScene(source,patch) {
  const result=overlay(source,patch,{name:'name',navigation:'navName'});
  if (result===source) return source;
  for (const [group,field] of Object.entries({notes:'text',drawings:'text',levels:'name'})) {
    if (source[group]) result[group]=byId(source[group],patch[group],(value,text)=>overlay(value,text,{[field]:field}));
  }
  if (source.tokens) result.tokens=byId(source.tokens,patch.tokens,(value,text)=>{
    const token=overlay(value,text,{name:'name'});
    if (token!==value && value.delta) token.delta=translateActor(value.delta,text.delta);
    return token;
  });
  if (source.regions) result.regions=byId(source.regions,patch.regions,(value,text)=>{
    const region=overlay(value,text,{name:'name'});
    if (region!==value && value.behaviors) region.behaviors=byId(value.behaviors,text.behaviors,(behavior,labels)=>{
      const mapping={name:'name'};
      if (behavior.type==='displayScrollingText') mapping.text='system.text';
      if (behavior.type==='teleportToken') Object.assign(mapping,{revealedDialog:'system.dialog.revealed',unrevealedDialog:'system.dialog.unrevealed'});
      return overlay(behavior,labels,mapping);
    });
    return region;
  });
  return result;
}
export const phandelverScenes = (source,patch) => byId(source,patch,translateScene);
export const phandelverMacros = (source,patch) => byId(source,patch,(value,text)=>overlay(value,text,{name:'name'}));
export const phandelverTables = (source,patch) => byId(source,patch,(value,text)=>{
  const table=overlay(value,text,{name:'name',description:'description'});
  if (table!==value && value.results) table.results=byId(value.results,text.results,
    (result,labels)=>overlay(result,labels,{name:'name',description:'description'}));
  return table;
});
