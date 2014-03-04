

class Player:

    def __init__(self, name, points=0):
        #Features that the player knows about itself and tells the game.
        #Except for bet, these attributes persist across rounds.
        self.name = name
        self.points = points
        self.bet = 0
        self.active = True

        #Features that the game assigns to the player. These (along with)
        #the bet, above) are set at the beginning of each round.
        self.hand = None
        self.turn = False
        self.big_blind = False
        self.small_blind = False
        self.dealer = False

    def clear_round_attributes(self):
        """This function allows the game to easily clear attributes on
        the player that are specific to a certain round, so that the
        player can be made ready for the next round.
        """
        self.bet = 0
        self.hand = None
        self.turn = False
        self.big_blind = False
        self.small_blind = False
        self.dealer = False

    def call(self, points):
        self.points -= points
        self.bet += points
        return points

    def raise_bet(self, points):
        return self.call(points=points)
        # self.points -= points
        # self.bet += points
        # return points

    def fold(self):
        self.active = False
        self.hand = None
        self.bet = 0


if __name__ == '__main__':
    pass
