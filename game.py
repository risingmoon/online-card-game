from player import Player
from deck import Deck
from evaluator import Evaluator


class Game:
    """A game of Texas Hold'em."""
    def __init__(self):
        self.players_size = 0
        self.players_list = []
        self.dealer = 0
        self.last_raise = 0
        self.current_player = 0

        self.pot = 0
        self.round_done = False
        self.best_hand_string = ''
        self.pot_won = 0
        self.winner = ''

        self.current_cycle = 0
        self.end_of_first = 0  # To prevent skipping big blind player

        self.min_bet = 0
        self.small_blind_points = 5
        self.big_blind_points = 10
        self.initial_points = 200

        self.deck = None
        self.common_cards = []
        self.evaluator = Evaluator()

    #The game's API consists entirely of the next 4 (possibly 5) methods:
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
        """Create a new Player object and add it to the game. Return the
        index in self.players_list of the player just created.
        """
        self.players_size += 1
        self.players_list.append(Player(name))
        return self.players_size - 1

    def remove_player(self, index):
        self.players_size -= 1

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

        #If only one active player remains.
        if self._poll_active_players() + self._poll_allin_players() == 1:
            self._end_round(
                self._get_next_active_player(self.current_player))

        if self.end_of_first:
            self.end_of_first = False
            if bet == 0:
                self._end_cycle()
                return

        #Otherwise, the player just checked or placed a bet.
        #Need to check for when the player is able to check (as opposed
        #to when they're required to place a bet).
        if not fold:
            if (self.players_list[self.current_player].bet <
                    self.players_list[self._get_previous_active_player(
                    self.current_player)].bet
                    and (not self.players_list[self.current_player].all_in)):
                raise ValueError(
                    "Your bet must at least equal the previous player's.")

            self.pot += bet

            if self.players_list[self.current_player].bet > self.players_list[
                    self._get_previous_active_player(self.current_player)].bet:
                self.last_raise = self.current_player
                self.min_bet = self.players_list[self.current_player].bet

        self.current_player = \
            self._get_next_active_player(self.current_player)

        #If we have made it around the table to the last player who
        #raised, and no additional raises have been made, end this
        #betting cycle. An exception is made for the first round of
        #betting, in which case the player who bet the big blind gets
        #an opportunity to raise or check.
        if self.last_raise == self.current_player:
            if (
                self.current_player == self._get_next_player(self.dealer, 2)
                    and self.current_cycle == 0):
                self.end_of_first = True
            else:
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
            'best_hand_string': self.best_hand_string,
            'pot_won': self.pot_won,
            'winner': self.winner,
        }

        community = []

        for card in self.common_cards:
            community.append([card.value, card.suit, card.string])

        info.update({'community': community})

        players = []

        if player is not None:
            #Loop beginning with the player on this player's left up
            #through the player on their right. Gather information about
            #the other players that this player needs to be able to see
            #on their game screen.
            for other_player in range(len(self.players_list))[player + 1:] + \
                    range(len(self.players_list[:player])):
                players.append([
                    self.players_list[other_player].name,
                    self.players_list[other_player].bet,
                    self.players_list[other_player].points,
                    self.players_list[other_player].active,
                    True if self.players_list[other_player] ==
                        self.current_player else False,
                    True if self.players_list[other_player] ==
                        info['dealer'] else False,
                    True if self.players_list[other_player] ==
                        info['small_blind'] else False,
                    True if self.players_list[other_player] ==
                        info['big_blind'] else False,
                ])

            info.update({
                'turn': True if player == self.current_player else False,
                'dealer': True if player == info['dealer'] else False,
                'small_blind': True if player == info['small_blind'] else False,
                'big_blind': True if player == info['big_blind'] else False,
                'points': self.players_list[player].points,
                'bet': self.players_list[player].bet,
                'active': self.players_list[player].active,
                'name': self.players_list[player].name,
                'players': players,
            })

            hand = []
            for card in self.players_list[player].hand:
                hand.append([card.value, card.suit, card.string])

            info.update({'hand': hand})

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

        return info

    def _initialize_round(self, dealer=None):
        """Assign one player the role of dealer and the next two players
        the roles of small blind and big blind. If the "dealer" argument
        is passed in, the game forces that player to be the dealer.
        Otherwise, it looks at its internal self.dealer and assigns to the
        NEXT player the role of dealer. The small blind and big blind are
        made to place their bets.
        """

        # Initialize a new deck object for each round
        self.deck = Deck()
        self.round_done = False
        self.best_hand_string = ''
        self.pot_won = 0
        self.winner = ''

        #  Remove players without enough $ to play
        for index, player in enumerate(self.players_list):
            if player.points < self.big_blind_points:
                self.remove_player(index)

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
            player.hand = [self.deck.get_card(), self.deck.get_card()]

        #Reset the pot and force the small blind and big blind to place
        #their bets.
        self.pot = 0
        self.pot += self.players_list[small_blind].call(
            self.small_blind_points)
        self.pot += self.players_list[big_blind].call(
            self.big_blind_points)

        self.min_bet = self.big_blind_points
        #Will eventually need to check that these players have enough
        #points to place the bet.

        self.current_cycle = 0
        self.common_cards = []

    def _end_cycle(self):
        """Called when the current betting cycle has concluded. This
        happens when the player whose turn it would currently be was the
        last player to raise. Initializes the next betting cycle or ends
        the round.
        """
        if self.current_cycle >= 3:
            #If this was the last betting cycle.
            self._end_round()

        else:
            if self.current_cycle == 0:
                self.common_cards = [
                    self.deck.get_card(),
                    self.deck.get_card(),
                    self.deck.get_card()
                    ]
            else:
                self.common_cards.append(self.deck.get_card())

            self.current_cycle += 1

            # Sets current player to first active player left of the big blind.
            self.current_player = \
                self._get_next_active_player(
                    self._get_next_player(self.dealer, 2))
            self.last_raise = self.current_player

    def _end_round(self, winner=None):
        """Called when the current round ends - either when all players
        but one fold, or when the last betting cycle is completed. When
        an argument is passed, the round is assumed to have ended because
        all players but the one with the index passed have folded.
        Determines a winner in the showdown (if applicable) and gives the
        pot to the winner.
        """
        # Find and save best hand for active each player, while keeping
        # track of the overall best hand

        best_rank = 7463  # Worst possible actual rank is 7462
        best_string = ''  # i.e. 'Full House' or 'Pair of Eights', etc.
        # best_cards = []  # Cards comprising the winning hand.
        Tie = False

        if winner is None:
            for index, player in enumerate(self.players_list):
                if player.active or player.all_in:
                    seven_cards = []
                    seven_cards.extend(self.common_cards)
                    seven_cards.extend(player.hand)
                    rank, string, cards = self.evaluator.get_best(seven_cards)
                    if rank < best_rank:
                        if Tie:
                            Tie = False
                        winner = index
                        winners_tie = [winner]
                        best_rank = rank
                        best_string = string
                        # best_cards = cards
                    elif rank == best_rank:
                        Tie = True
                        winners_tie.append(index)

        if Tie:
            split_pot = self.pot // len(winners_tie)
            for player_index in winners_tie:
                self.players_list[player_index].points += split_pot

        # If the winner was all in, they cannot win more than the pot amount
        # at the time of going all in.
        elif self.players_list[winner].all_in:
            subpot = self._get_subpot(self.players_list[winner].bet)
            self.players_list[winner].points += subpot
            self.pot -= subpot
            self.players_list[winner].all_in = False
            if self.pot > 0:
                self._end_round()  # Find winner of remaining pot

        else:
            self.players_list[winner].points += self.pot

        self.round_done = True
        self.best_hand_string = best_string
        self.pot_won = self.pot
        self.winner = self.players_list[winner].name

        self._initialize_round()

    def _poll_active_players(self):
        """Find out how many players are active (haven't folded)."""
        active_players = 0
        for player in self.players_list:
            if player.active:
                active_players += 1

        return active_players

    def _poll_allin_players(self):
        """Find out how many players are all in, but not active."""
        allin_players = 0
        for player in self.players_list:
            if player.all_in:
                allin_players += 1

        return allin_players

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

        return index

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

        return index

    def _get_next_player(self, index, step=1):
        """Get the player step positions to the left of the player at
        the index passed in. The index passed in must be a valid index.
        """
        if index not in range(self.players_size):
            raise IndexError(
                "Index %s passed to _get_next_player is out of range." %
                index)

        return (index + step) % self.players_size

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

    def _get_subpot(self, bet):
        subpot = 0
        for player in self.players_list:
            if bet >= player.bet:
                subpot += player.bet
            else:
                subpot += bet
        return subpot


if __name__ == '__main__':
    game = Game()
    game.run_game()
