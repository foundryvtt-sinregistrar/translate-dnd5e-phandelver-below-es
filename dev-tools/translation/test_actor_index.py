import unittest
from apply_actor_index import compose, biography_key
from text_schema import normalize

class ActorIndexTests(unittest.TestCase):
    def test_preserves_portrait_and_links(self):
        source='<h2>@UUID[Actor.one]</h2><figure><img src="portrait.webp"></figure><section class="bio"><p>A loyal scout.</p></section><h2 class="float-clear">References</h2><p><strong>Castle:</strong> @UUID[JournalEntry.one]</p>'
        memory={normalize('<p>A loyal scout.</p>'):{'<p>Un explorador leal.</p>'}}
        text,reason=compose(source,memory,{'References':'Referencias','Castle':'Castillo'})
        self.assertIsNone(reason)
        self.assertEqual(text,source.replace('A loyal scout.','Un explorador leal.').replace('References','Referencias').replace('Castle:','Castillo:'))

    def test_rejects_similar_biography_and_unknown_reference(self):
        source='<section class="bio"><p>A disloyal scout.</p></section><p>References</p>'
        memory={normalize('<p>A loyal scout.</p>'):{'<p>Un explorador leal.</p>'}}
        self.assertIsNone(compose(source,memory,{'References':'Referencias'})[0])
        source=source.replace('disloyal','loyal').replace('References','Unreviewed warning')
        self.assertIsNone(compose(source,memory,{'References':'Referencias'})[0])

    def test_rejects_ambiguous_translation_and_labelled_uuid(self):
        source='<section class="bio"><p>Scout</p></section><p>@UUID[Actor.one]{Unknown label}</p>'
        memory={normalize('<p>Scout</p>'):{'<p>Explorador</p>'}}
        self.assertIsNone(compose(source,memory,{})[0])
        memory[normalize('<p>Scout</p>')].add('<p>Exploradora</p>')
        self.assertIsNone(compose('<section class="bio"><p>Scout</p></section>',memory,{})[0])

    def test_void_element_spelling_and_reviewed_label(self):
        source='<h2>@UUID[Actor.one]{Scout}</h2><section class="bio"><p>Scout.</p><hr><p>Loyal.</p></section>'
        memory={biography_key('<p>Scout.</p><hr /><p>Loyal.</p>'):{'<p>Explorador.</p><hr /><p>Leal.</p>'}}
        result,reason=compose(source,memory,{'Scout':'Explorador'})
        self.assertIsNone(reason)
        self.assertIn('@UUID[Actor.one]{Explorador}',result)
        self.assertIn('<p>Leal.</p>',result)
        self.assertIsNone(compose(source.replace('<hr>','<hr class="important">'),memory,{'Scout':'Explorador'})[0])

    def test_empty_and_unwrapped_biographies(self):
        source='<section class="bio"></section><h2>References</h2>'
        self.assertEqual(compose(source,{}, {'References':'Referencias'})[0],source.replace('References','Referencias'))
        source='<figure><img src="portrait.webp"></figure><p>Scout.</p>'
        memory={biography_key('<p>Scout.</p>'):{'<p>Explorador.</p>'}}
        self.assertEqual(compose(source,memory,{})[0],source.replace('Scout.','Explorador.'))
        self.assertIsNone(compose(source+'<p>Unreviewed.</p>',memory,{})[0])

if __name__=='__main__':unittest.main()
