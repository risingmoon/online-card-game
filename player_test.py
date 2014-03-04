import unittest
from player import Player


class PlayerTest(unittest.TestCase):

    def setUp(self):
        self.player = Player('foo', 100)

    def test_init(self):
        self.assertEqual(self.player.name, 'foo')
        self.assertEqual(self.player.points, 100)

    def test_call(self):
        self.player.call(25)
        self.assertEqual(self.player.bet, 25)
        self.assertEquals(self.player.points, 75)

    def test_raise_bet(self):
        self.test_call()
        self.player.raise_bet(50)
        self.assertEqual(self.player.bet, 75)
        self.assertEquals(self.player.points, 25)

    def test_fold(self):
        self.test_raise_bet()
        self.player.fold()
        self.assertEqual(self.player.bet, 0)
        self.assertEqual(self.player.hand, None)
        self.assertEqual(self.player.points, 25)


if __name__ == '__main__':
    unittest.main()
