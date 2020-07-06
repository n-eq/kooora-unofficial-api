import unittest
import sys, os

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.dirname(DATA_DIR)))

from kooora import Kooora, League

class TestLeague(unittest.TestCase):
    def test_parsing_from_id(self):
        l = League.from_id(16126)
        self.assertEqual(l.get_title(), 'الدوري الإسباني الدرجة الأولى')
        self.assertEqual(l.get_years(), [2018, 2019])
        self.assertEqual(l.get_sport(), 0)

        l = League.from_id(9406)
        self.assertEqual(l.get_table()[3]['Team']['Name'], 'الكوكب المراكشي')

if __name__ == '__main__':
    unittest.main()

