from player import Player


class Game:

    def __init__(self):
        self.players_size = 0
        self.players_list = []
        self.dealer = 0
        self.last_raise = 0
        self.current_player = 0

        self.pot = 0

        self.current_cycle = 0

        self.min_bet = 0
        self.small_blind_points = 5
        self.big_blind_points = 10
        self.initial_points = 100

        #self.round_size = 0
        #self.round_list = []
        #self.current_bet = 0

    #The game's API consists entirely of these 3 (possibly 4) methods:
    #add_player, MAYBE remove_player, initialize_game, and update_game.
    #add_player is called to put players into the game before starting it.
    #remove_player allows a player to be dropped from the game.
    #initialize_game is called after all players have been added and takes
    #care of everything related to starting the game.
    #update_game is called every time a player ends their turn to update
    #the internal state of the game to reflect that player's actions.

    def add_player(self, name):
        """Create a new Player object and add it to the game. Return a
        reference to the Player object just created.
        """
        self.players_size += 1
        new_player = Player(name)
        self.players_list.append(new_player)
        return new_player

    def remove_player(self, name):
        pass

    def initialize_game(self):
        """When called, we allocate to each player a beginning number of
        points and initialize the first round. The first betting cycle
        then begins implicitly.
        """
        for player in self.players_list:
            player.points = self.initial_points

        #For now the first player to join the lobby is made the dealer.
        self._initialize_round(dealer=0)

    def update_game(self, bet=0, fold=False):
        """Function that updates the internal state of the game whenever
        a player concludes their turn. Takes as an argument the amount of
        the bet (if any) placed by that player and whether or not that
        player folded.
        """

        #EVENTUALLY this function will need to validate the actions just
        #made by the player & prompt them to redo if their actions were
        #invalid.

        if fold:
            #If all players but one have folded.
            if self._poll_active_players() == 1:
                for player in range(self.players_size):
                    if self.players_list[player].active:
                        self._end_round(player=player)
                        return
        else:
            self.pot += bet
            if self.players_list[self.current_player].bet > \
                    self.players_list[self.current_player - 1].bet:
                self.last_raise = self.current_player
            # elif self.players_list[self.current_player].bet > \
            #         self.players_list[self.current_player - 1].bet:
            #     raise Exception("Your bet must at least equal the last player's.")

        self._next_player_turn()

        #If we have made it around the table to the last player who raised,
        #and no additional raises have been made, end this betting cycle.
        if self.last_raise == self.current_player:
            self._end_cycle()

    def _initialize_round(self, dealer=None):
        """Assign one player the role of dealer and the next two players
        the roles of small blind and big blind. If the "dealer" argument
        is passed in, the game forces that player to be the dealer.
        Otherwise, it looks at its internal self.dealer and assigns to the
        NEXT player the role of dealer. The small blind and big blind are
        made to place their bets.
        """
        #Determine who the dealer, small blind, and big blind will be for
        #the next round.
        if dealer:
            self.dealer = dealer
        else:
            self.dealer += 1
            self.dealer %= self.players_size

        small_blind = self.dealer + 1
        small_blind %= self.players_size

        big_blind = self.small_blind + 1
        big_blind %= self.players_size

        first_turn = self.big_blind + 1
        first_turn %= self.players_size

        #Clear all the attributes on players left over from the last round.
        for player in self.players_list:
            player.clear_round_attributes()

        #Assign the proper attributes for the coming round to the players
        #that we determined earlier.
        self.players_list[self.dealer].dealer = True

        self.players_list[small_blind].small_blind = True

        self.players_list[big_blind].big_blind = True
        self.last_raise = big_blind

        #The player to the left of the big blind gets the first turn.
        self.current_player = first_turn
        self.players_list[first_turn].turn = True

        #Force the small blind and big blind to place their bets.
        self.pot = 0
        self.pot += self.players_list[small_blind].call(
            self.small_blind_points)
        self.pot += self.players_list[big_blind].call(
            self.big_blind_points)

        #Deal two cards to each player.
        #TBD

    #These functions have been wrapped into _initialize_round.
    # def blinds(self):
    #     small_blind = self.players_list[self.mod(self.dealer, 1)]
    #     big_blind = self.players_list[self.mod(self.dealer, 2)]
    #     self.last_raised = self.mod(self.dealer, 3)
    #     small_blind.call(self.small_blind_points)
    #     big_blind.call(self.big_blind_points)

    # def end_round(self):
    #     for index in self.players_size:
    #         self.players_list[index].active = True

    def _next_player_turn(self):
        """Give the next player their turn. Find the next player from
        the current player who is active (hasn't folded) and set their
        "turn" attribute. Unset the "turn" attribute of the player who
        just had their turn.
        """
        self.players_list[self.current_player].turn = False
        self.current_player += 1
        self.current_player %= self.players_size
        while(not self.players_list[self.current_player].active):
            self.current_player += 1
            self.current_player %= self.players_size

        self.players_list[self.current_player].turn = True

    def _poll_active_players(self):
        """Find out how many players are active (haven't folded)."""
        active_players = 0
        for player in self.players_list:
            if player.active:
                active_players += 1

        return active_players

    def _end_cycle(self):
        """Called when the current betting cycle has concluded. This
        happens when the player whose turn it would currently be was the
        last player to raise."""
        if self.current_cycle == 0:
            #Deal out three cards (the flop)
            self.current_cycle += 1
        elif self.current_cycle == 1:
            #Deal out one card (the turn)
            self.current_cycle += 1
        elif self.current_cycle == 2:
            #Deal out one card (the river)
            self.current_cycle += 1
        else:
            #This was the last betting cycle
            self._end_round()

    def _end_round(self, player=None):
        """Called when the current round ends - either when all players
        but one fold, or when the last betting cycle is completed. When
        an argument is passed, the round is assumed to have ended because
        all players but the one with the index passed have folded.
        """
        if player is not None:
            self.players_list[player].points += self.pot
            self._initialize_round()
        else:
            #The showdown happens here; hands are compared & a winner is
            #determined.
            self._initialize_round()

    # def run_round(self):
    #     player_index = (self.last_raise + 1) % self.players_size
    #     while player_index is not self.last_raise:
    #         if self.players_list[player_index].active:
    #             print self.players_list[player_index].name
    #         player_index += 1
    #         player_index = player_index % self.players_size

    # def mod(self, player, number):
    #     return (player + number) % self.players_size

    # def active(self, player):
    #     return self.player.active

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
