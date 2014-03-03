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


if __name__ == '__main__':
    unittest.main()
