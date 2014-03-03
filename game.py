from player import Player


class Game:

    def __init__(self):
        self.players_size = 0
        #self.round_size = 0
        self.players_list = []
        #self.round_list = []
        self.pot = 0
        self.minimal_bet = 0
        self.current_bet = 0
        self.current_player = 0

    def add_player(self, name):
        self.players_size += 1
        self.players_list.append(Player(name))

    def remove_player(self, name):
        pass

    def start_round(self):
        for index in self.players_size:
            self.players_list[index].active = True

    def run_round(self):
        pass
        # small_blind = self.current_player + 1
        # big_blind = self.current_player + 2
        # last_raise = big_blind

    def turn(self, player, cmd, points):
        if cmd == 'CALL':
            player.call(self.current_bet)
        elif cmd == 'RAISE':
            player.call()
            self.current_bet += player.raise_bet(points)
        elif cmd == 'FOLD':
            player.fold()
        else:
            raise KeyError("WRONG CMD")

    def bet_cycle(self):
        pass


if __name__ == '__main__':
    game = Game()
    game.run_game()
