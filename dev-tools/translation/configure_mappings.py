"""Keep Babele's embedded-document fallback and constrain custom leaf overlays."""
from text_schema import ROOT, load, save

def configure():
    item={'description':'system.description.value','requirements':'system.requirements',
          'descriptionChat':'system.description.chat','unidentifiedName':'system.unidentified.name',
          'unidentifiedDescription':'system.unidentified.description',
          'activities':{'path':'system.activities','converter':'phandelverActivities'},
          'effects':{'path':'effects','converter':'phandelverEffects'},
          'advancement':{'path':'system.advancement','converter':'phandelverAdvancementNames'}}
    def documents(path,kind,mapping):
        return {'path':path,'converter':'phandelverDocuments','documentType':kind,'cardinality':'many','mapping':mapping}
    actor={'biography':'system.details.biography.value','tokenName':'prototypeToken.name',
           'alignment':'system.details.alignment','habitat':'system.details.habitat.custom',
           'creatureType':'system.details.type.custom','creatureSubtype':'system.details.type.subtype',
           'languages':'system.traits.languages.custom','senses':'system.attributes.senses.special',
           'biographyPublic':'system.details.biography.public',
           'items':documents('items','Item',item),'effects':{'path':'effects','converter':'phandelverEffects'}}
    for name in ['pbso-items','pbso-player-options','pbso-bestiary','pbso-adventures']:
        path=ROOT/f'compendium/dnd-phandelver-below.{name}.json';payload=load(path)
        if name in ['pbso-items','pbso-player-options']:payload['mapping'].update(item)
        elif name=='pbso-bestiary':payload['mapping'].update(actor)
        else:payload['mapping'].update({'items':documents('items','Item',item),'actors':documents('actors','Actor',actor),
            'scenes':{'path':'scenes','converter':'phandelverScenes'},
            'tables':{'path':'tables','converter':'phandelverTables'},
            'macros':{'path':'macros','converter':'phandelverMacros'}})
        save(path,payload)

if __name__=='__main__':configure()
