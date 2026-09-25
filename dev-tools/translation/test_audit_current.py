import unittest
from audit_current import numbers, protected_html, tokens


class AuditTests(unittest.TestCase):
    def test_thousands_and_decimals(self):
        self.assertEqual(numbers('8,000 gp and 2.5 feet', 'en'), numbers('8.000 po y 2,5 pies', 'es'))
        self.assertNotEqual(numbers('8,000 gp', 'en'), numbers('8.100 po', 'es'))
        self.assertEqual(numbers('0.125', 'en'), numbers('0,125', 'es'))

    def test_only_allowlisted_visible_attributes_can_change(self):
        en='<span data-tooltip="Gold" data-id="123">gold</span>'
        self.assertEqual(protected_html(en), protected_html(en.replace('Gold', 'Oro')))
        self.assertNotEqual(protected_html(en), protected_html(en.replace('123', '456')))

    def test_roll_comment_can_change_but_formula_cannot(self):
        self.assertEqual(tokens('[[/r 1d6#Days]]'), tokens('[[/r 1d6#Días]]'))
        self.assertNotEqual(tokens('[[/r 1d6#Days]]'), tokens('[[/r 1d8#Días]]'))


if __name__ == '__main__': unittest.main()
