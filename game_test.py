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


class TestGetActivePlayerFunctions(unittest.TestCase):
    """Test the _get_next_active_player, _get_previous_active_player, and
    _poll_active_players functions.
    """
    def setUp(self):
        self.game = Game()
        for name in ['Jordan', 'Matt', 'Justin', 'Cris']:
            self.game.add_player(name)

    def test_poll_all_players_active(self):
        """Count the active players when all players are active."""
        self.assertEqual(
            self.game._poll_active_players(), self.game.players_size)

    def test_poll_some_players_active(self):
        """Count the active players when some players are active, and not
        necessarily all in a row.
        """
        for player in self.game.players_list[::2]:
            player.active = False

        self.assertEqual(
            self.game._poll_active_players(), self.game.players_size / 2)

    def test_poll_no_players_active(self):
        """Count the active players when no players are active."""
        for player in self.game.players_list:
            player.active = False

        self.assertEqual(
            self.game._poll_active_players(), 0)

    def test_get_previous_no_active_players(self):
        """Attempt to the find the previous active player when no players
        are active.
        """
        for player in self.game.players_list:
            player.active = False

        self.assertRaises(
            BaseException, self.game._get_previous_active_player, 0)

    def test_get_next_no_active_players(self):
        """Attempt to find the next active player when no players are
        active.
        """
        for player in self.game.players_list:
            player.active = False

        self.assertRaises(
            BaseException, self.game._get_previous_active_player, 0)

    def test_get_previous_within_list(self):
        """Attempt to find the previous active player when that player
        comes before the beginning of the list.
        """
        for player in self.game.players_list[::2]:
            player.active = False

        self.assertEqual(
            self.game._get_previous_active_player(2), 0)

    def test_get_next_within_list(self):
        """Attempt to find the next active player when that player comes
        before the end of the list.
        """
        for player in self.game.players_list[::2]:
            player.active = False

        self.assertEqual(
            self.game._get_next_active_player(0), 2)

    def test_get_previous_past_beginning(self):
        """Attempt to find the previous active player when that operation
        will require us to loop back to the end of the list.
        """
        for player in self.game.players_list[::2]:
            player.active = False

        self.assertEqual(
            self.game._get_previous_active_player(0), 2)

    def test_get_next_past_end(self):
        """Attempt to find the next active player when that operation will
        require us to loop back to the top of the list.
        """
        for player in self.game.players_list[::2]:
            player.active = False

        self.assertEqual(
            self.game._get_next_active_player(2), 0)


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
