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

    #The game's API consists entirely of these 4 (possibly 5) methods:
    #add_player, MAYBE remove_player, initialize_game, update_game, and
    #poll_game.
    #add_player is called to put players into the game before starting it.
    #remove_player allows a player to be dropped from the game.
    #initialize_game is called after all players have been added and takes
    #care of everything related to starting the game.
    #update_game is called every time a player ends their turn to update
    #the internal state of the game to reflect that player's actions.
    #poll_game is called by the server's HTML templater for the game room
    #in order to get out the information it needs to deliver each player
    #a version of the room tailored to them.

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
            if self.players_list[self.current_player].bet < self.players_list[
                    self._get_previous_player(self.current_player)].bet:
                raise ValueError(
                    "Your bet must at least equal the last player's.")

            self.pot += bet

            if self.players_list[self.current_player].bet > self.players_list[
                    self._get_previous_player(self.current_player)].bet:
                self.last_raise = self.current_player

        self._next_player_turn()

        #If we have made it around the table to the last player who raised,
        #and no additional raises have been made, end this betting cycle.
        if self.last_raise == self.current_player:
            self._end_cycle()

    def poll_game(self, player=None):
        """Return a dictionary containing useful information about the
        state of the game. If a player index is passed in, the dictionary
        includes information about that specific player, which makes this
        function a one-stop shop for users to get information specific to
        the game from their perspective.
        """
        info = {
            'dealer': self.dealer,
            'small_blind': self._get_next_player(self.dealer),
            'big_blind': self._get_next_player(self.dealer, 2),
            'pot': self.pot,
        }

        players = []

        if player is not None:
            #Loop beginning with the player on this player's left up
            #through the player on their right. Gather information about
            #the other players that this player needs to be able to see
            #on their game screen.
            for other_player in self.players_list[player + 1:] + \
                    self.players_list[:player]:
                players.append({
                    'name': other_player.name,
                    'bet': other_player.bet,
                    'points': other_player.points,
                    'active': other_player.active,
                })

            info.update({
                'turn': True if player == self.current_player else False,
                'dealer': True if player == info['dealer'] else False,
                'small_blind': True if player == info['small_blind'] else False,
                'big_blind': True if player == info['big_blind'] else False,
                'hand': self.players_list[player].hand,
                'points': self.players_list[player].points,
                'bet': self.players_list[player].bet,
                'active': self.players_list[player].active,
                'name': self.players_list[player].name,
                'players': players,
            })
        else:
            #If a spectator is making this request, return a minimal amount
            #of information on all players.
            for other_player in self.players_list:
                players.append({
                    'name': other_player.name,
                    'bet': other_player.bet,
                    'points': other_player.points,
                    'active': other_player.active,
                })

            info.update({'players': players})

    def _initialize_round(self, dealer=None):
        """Assign one player the role of dealer and the next two players
        the roles of small blind and big blind. If the "dealer" argument
        is passed in, the game forces that player to be the dealer.
        Otherwise, it looks at its internal self.dealer and assigns to the
        NEXT player the role of dealer. The small blind and big blind are
        made to place their bets.
        """
        #Determine who the dealer, small blind, big blind, and first turn
        #will be for the next round.
        if dealer is not None:
            self.dealer = dealer
        else:
            self.dealer = self._get_next_player(self.dealer)

        small_blind = self._get_next_player(self.dealer)

        big_blind = self._get_next_player(small_blind)
        self.last_raise = big_blind

        self.current_player = self._get_next_player(big_blind)

        #Deal two cards to each player and reset their bets and active
        #status from the last round.
        for player in self.players_list:
            player.bet = 0
            player.active = True
            player.hand = None
            #Deal two cards here instead; to do

        #Reset the pot and force the small blind and big blind to place
        #their bets.
        self.pot = 0
        self.pot += self.players_list[small_blind].call(
            self.small_blind_points)
        self.pot += self.players_list[big_blind].call(
            self.big_blind_points)
        #Will eventually need to check that these players have enough
        #points to place the bet.

        self.current_cycle = 0

    def _next_player_turn(self):
        """Give the next player their turn. Find the next player from
        the current player who is active (hasn't folded) and assign their
        index to self.current_player.
        """
        self.current_player = self._get_next_player(self.current_player)
        while(not self.players_list[self.current_player].active):
            self.current_player = \
                self._get_next_player(self.current_player)

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

    def _get_next_active_player(self, index):
        """Get the next active player clockwise around the table from
        the player at the index passed in. The index passed in must be a
        valid index.
        """
        count = 0
        index = self._get_next_player(index)
        while not self.players_list[index].active:
            index = self._get_next_player(index)
            count += 1
            if count > self.players_size:
                raise BaseException(
                    "_get_next_active_player is looping infinitely.")

    def _get_next_player(self, index, step=1):
        """Get the player step positions to the left of the player at
        the index passed in. The index passed in must be a valid index.
        """
        if index not in range(self.players_size):
            raise IndexError(
                "Index %s passed to _get_next_player is out of range." %
                index)

        return (index + step) % self.players_size

    def _get_previous_active_player(self, index):
        """Get the next active player counterclockwise around the table
        from the player at the index passed in. The index passed in must
        be a valid index.
        """
        count = 0
        index = self._get_previous_player(index)
        while not self.players_list[index].active:
            index = self._get_previous_player(index)
            count += 1
            if count > self.players_size:
                raise BaseException(
                    "_get_previous_active_player is looping infinitely.")

    def _get_previous_player(self, index, step=1):
        """Get the player step positions to the right of the player at
        the index passed in. The index passed in must be a valid index.
        """
        if index not in range(self.players_size):
            raise IndexError(
                "Index %s passed to _get_previous_player is out of range."
                % index)

        index -= step
        while index < 0:
            index += self.players_size
        return index


if __name__ == '__main__':
    game = Game()
    game.run_game()
