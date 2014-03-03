from player import Player

class Game:

    def __init__(self):
        self.players_size = 0
        self.round_size = 0
        self.players_list = []
        self.round_list = []

    def add_player(self,name):
        self.players_size += 1
        self.players_list.append(Player(name))
if __name__ == '__main__':
    game = Game()
    game.run_game()
