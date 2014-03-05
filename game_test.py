import unittest
from game import Game


class GameTest(unittest.TestCase):

    def setUp(self):
        self.game = Game()
        self.names = ['Jordan', 'Matt', 'Justin', 'Cris']

    def setUp_players(self):
        for name in self.names:
            self.game.add_player(name)

    def test_player_size(self):
        self.assertEquals(len(self.game.players_list), self.game.players_size)

    def test_add_player(self):
        self.test_player_size()
        #Checks for size
        for name in self.names:
            self.game.add_player(name)
            self.test_player_size()
        for index in range(len(self.names)):
            self.assertEquals(self.names[index],
                              self.game.players_list[index].name)


class TestPlayerGetFunctions(unittest.TestCase):
    """Test the _get_next_player and _get_previous_player funcions."""
    def setUp(self):
        self.game = Game()
        for name in ['Jordan', 'Matt', 'Justin', 'Cris']:
            self.game.add_player(name)

        self.middle_next = 1
        self.middle_prev = 2
        self.beginning = 0
        self.end = 3

    def test_get_next_from_center(self):
        """Get the next player from the middle of the list of players."""
        self.assertEqual(self.game._get_next_player(self.middle_next),
            self.middle_next + 1)

    def test_get_next_from_center_with_step(self):
        """Get the next player from the middle of the list of players
        using a step size greater than one.
        """
        self.assertEqual(self.game._get_next_player(self.middle_next, 2),
            self.middle_next + 2)

    def test_get_next_from_end(self):
        """Get the next player from the end of the list of players."""
        self.assertEqual(self.game._get_next_player(self.end),
            self.beginning)

    def test_get_next_from_end_with_step(self):
        """Get the next player from the end of the list of players using
        a step size greater than one.
        """
        self.assertEqual(self.game._get_next_player(self.end, 2),
            self.beginning + 1)

    def test_get_previous_from_center(self):
        """Get the previous player from the middle of the list of players."""
        self.assertEqual(self.game._get_previous_player(self.middle_prev),
            self.middle_prev - 1)

    def test_get_previous_from_center_with_step(self):
        """Get the previous player from the middle of the list of players
        using a step size greater than one.
        """
        self.assertEqual(self.game._get_previous_player(self.middle_prev, 2),
            self.middle_prev - 2)

    def test_get_previous_from_beginning(self):
        """Get the previous player from the beginning of the list of players.
        """
        self.assertEqual(self.game._get_previous_player(self.beginning),
            self.end)

    def test_get_previous_from_beginning_with_step(self):
        """Get the previous player from the beginning of the list of players
        using a step size greater than one.
        """
        self.assertEqual(self.game._get_previous_player(self.beginning, 2),
            self.end - 1)


if __name__ == '__main__':
    unittest.main()
