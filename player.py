

class Player:

    def __init__(self, name, points=0):
        #Features that the player knows about itself and tells the game.
        #Except for bet, these attributes persist across rounds.
        self.name = name
        self.points = points
        self.bet = 0
        self.active = True
        self.hand = None

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
