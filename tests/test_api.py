import unittest
import sys, os

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.dirname(DATA_DIR)))

print("path: ", sys.path)

from kooora.kooora import Kooora, Team, Player, League

class TestAPISearch(unittest.TestCase):
    def setUp(self):
        self.api = Kooora()
        self.kacm_teams = self.api.search_team('الكوكب المراكشي')

    def test_search_result_instance(self):
        for t in self.kacm_teams:
            self.assertIsInstance(t, Team)

        for p in self.api.search_player('مهري'):
            self.assertIsInstance(p, Player)

        for l in self.api.search_league('الدوري الفرنسي'):
            self.assertIsInstance(l, League)

    def test_team_search_result(self):
        kacm_ids = [t.get_id() for t in self.kacm_teams]
        self.assertIn(1291, kacm_ids)

if __name__ == '__main__':
    unittest.main()

