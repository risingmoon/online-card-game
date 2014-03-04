

class Player:

    def __init__(self, name, points=0):
        #Features that the player knows about itself and tells the game.
        self.name = name
        self.points = points
        self.hand = None
        self.bet = 0
        self.active = True

        #Features that the game assigns to the player.
        self.turn = False
        self.big_blind = False
        self.small_blind = False
        self.dealer = False

    def set_attributes(self,
        turn=False, big_blind=False, small_blind=False, dealer=False):
        """This function allows the game to easily set or unset any
        combination of the attributes it might assign to the player.
        """
        self.turn = turn
        self.big_blind = big_blind
        self.small_blind = small_blind
        self.dealer = dealer

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
