from player import Player


class Game:

    def __init__(self):
        self.players_size = 0
        #self.round_size = 0
        self.players_list = []
        #self.round_list = []
        self.pot = 0
        self.min_bet = 0
        self.current_bet = 0
        self.dealer = 0
        self.last_raise = 0
        self.current_player = 0
        self.small_blind_points = 5
        self.big_blind_points = 10
        self.initial_points = 100

    def add_player(self, name):
        self.players_size += 1
        new_player = Player(name)
        self.players_list.append(new_player)
        return new_player

    def remove_player(self, name):
        pass

    def initialize_game(self):
        """When called, we allocate to each player a beginning number of
        points, choose a dealer, and set the big and small blind
        accordingly.
        """

        for player in self.players_list:
            player.points = self.initial_points

        #For now the first player to join the lobby is made the dealer.
        self._set_dealer_and_blinds(dealer=0)

    def _set_dealer_and_blinds(self, dealer=None):
        """Assign one player the role of dealer and the next two players
        the roles of small blind and big blind. If the "dealer" argument
        is passed in, the game forces that player to be the dealer.
        Otherwise, it looks at its internal self.dealer and assigns to the
        NEXT player the role of dealer.
        """
        if dealer:
            self.dealer = dealer
        else:
            self.dealer += 1
            self.dealer %= self.players_size

        small_blind = self.dealer + 1
        small_blind %= self.players_size

        big_blind = self.small_blind + 1
        big_blind %= self.players_size

        self.players_list[self.dealer].set_attributes(dealer=True)
        self.players_list[small_blind].set_attributes(
            small_blind=True, turn=True)
        self.players_list[big_blind].set_attributes(big_blind=True)

        #The small blind is to the left of the dealer, so their turn is first.
        self.current_player = small_blind

    def _next_player_turn(self):
        """Give the next player their turn. Find the next player from
        the current player who is active (hasn't folded) and set their
        "turn" attribute. Unset the "turn" attribute of the player who
        just had their turn.
        """
        self.players_list[self.current_player].turn = False
        self.current_player += 1
        self.current_player %= self.players_size
        self.players_list[self.current_player].turn = True

    def end_round(self):
        for index in self.players_size:
            self.players_list[index].active = True

    def run_round(self):
        player_index = (self.last_raise + 1) % self.players_size
        while player_index is not self.last_raise:
            if self.players_list[player_index].active:
                print self.players_list[player_index].name
            player_index += 1
            player_index = player_index % self.players_size

    def mod(self, player, number):
        return (player + number) % self.players_size

    def blinds(self):
        small_blind = self.players_list[self.mod(self.dealer, 1)]
        big_blind = self.players_list[self.mod(self.dealer, 2)]
        self.last_raised = self.mod(self.dealer, 3)
        small_blind.call(self.small_blind_points)
        big_blind.call(self.big_blind_points)

    def active(self, player):
        return self.player.active

    # def turn(self, player):

    #     if cmd == 'CALL':
    #         player.call(self.current_bet)
    #     elif cmd == 'RAISE':
    #         player.call(self.current_bet)
    #         self.current_bet += player.raise_bet(5)
    #     elif cmd == 'FOLD':
    #         self.pot += player.bet
    #         player.fold()
    #         player.active = False
    #     else:
    #         raise KeyError("WRONG CMD")

    def bet_cycle(self):
        pass

    def run_game(self):
        """
        1.Randomize dealer
        2.Rounds

        """


if __name__ == '__main__':
    game = Game()
    game.run_game()
