import unittest
from text_schema import numbers,adapt

class NumberTests(unittest.TestCase):
    def test_localized_roll_comment_without_spaces_preserves_formula(self):
        self.assertIsNotNone(adapt('[[/r 1d6#Salvageable shards]]','[[/r 1d6#Fragmentos aprovechables]]'))
        self.assertIsNone(adapt('[[/r 1d6#Salvageable shards]]','[[/r 1d8#Fragmentos aprovechables]]'))

    def test_same_document_id_in_two_packs_retains_exact_destinations(self):
        source='@UUID[Compendium.one.pack.Actor.same]{One} @UUID[Compendium.two.pack.Actor.same]{Two}'
        translated=source.replace('{One}','{Uno}').replace('{Two}','{Dos}')
        self.assertEqual(adapt(source,translated),translated)
        self.assertIsNone(adapt(source,translated.replace('Compendium.one.pack','Compendium.three.pack')))

    def test_known_broken_reference_can_be_repaired_without_losing_rules(self):
        source='&amp;Reference[total-cover}{total cover}, 21 (6d6), [[/save ability=con dc=21]]'
        translated='&amp;Reference[total-cover]{cobertura total}, 21 (6d6), [[/save ability=con dc=21]]'
        self.assertIsNotNone(adapt(source,translated))
        self.assertIsNone(adapt(source,translated.replace('21 (6d6)','22 (6d6)')))
        self.assertIsNone(adapt(source,translated.replace('total-cover','half-cover')))

    def test_currency_with_no_space(self):
        self.assertEqual(numbers('510pp, 1,250gp'),numbers('510 pp, 1.250 po'))
        self.assertIsNotNone(adapt('1,250gp','1.250 po'))
        self.assertIsNone(adapt('1,250gp','1.350 po'))

    def test_dice_ranges_decimals_and_attributes(self):
        self.assertEqual(numbers('<p id="123">2d6 + 2, 30/120, 2.5</p>'),['120','2','2','2','30','5','6'])
        self.assertEqual(numbers('8,000'),['8000'])
        self.assertEqual(numbers('10,000,000gp'),['10000000'])

if __name__=='__main__':unittest.main()
