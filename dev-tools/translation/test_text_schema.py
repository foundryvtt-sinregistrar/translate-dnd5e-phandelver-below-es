import unittest
from text_schema import numbers,adapt

class NumberTests(unittest.TestCase):
    def test_currency_with_no_space(self):
        self.assertEqual(numbers('510pp, 1,250gp'),numbers('510 pp, 1.250 po'))
        self.assertIsNotNone(adapt('1,250gp','1.250 po'))
        self.assertIsNone(adapt('1,250gp','1.350 po'))

    def test_dice_ranges_decimals_and_attributes(self):
        self.assertEqual(numbers('<p id="123">2d6 + 2, 30/120, 2.5</p>'),['120','2','2','2','30','5','6'])
        self.assertEqual(numbers('8,000'),['8000'])
        self.assertEqual(numbers('10,000,000gp'),['10000000'])

if __name__=='__main__':unittest.main()
