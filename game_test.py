import unittest
from game import Game

NAMES = ['Jordan', 'Matt', 'Justin', 'Cris']


class GameTest(unittest.TestCase):

    def setUp(self):
        self.game = Game()

    def setUp_players(self):
        for name in NAMES:
            self.game.add_player(name)

    def test_player_size(self):
        self.assertEquals(len(self.game.players_list), self.game.players_size)

    def test_add_player(self):
        self.test_player_size()
        #Checks for size
        for name in NAMES:
            self.game.add_player(name)
            self.test_player_size()
        for index in range(len(NAMES)):
            self.assertEquals(NAMES[index],
                              self.game.players_list[index].name)

    def test_mod(self):
        self.setUp_players()
        for i in range(len(NAMES)):
            for j in range(1, 4):
                players = i
                self.assertEquals(
                    self.game.mod(players, j),
                    (i + j) % self.game.players_size)

    def test_run_round(self):
        self.setUp_players()
        self.game.last_raise = 1
        self.game.players_list[3].active = False
        self.game.run_round()


if __name__ == '__main__':
    unittest.main()
