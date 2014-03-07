

class Player:

    def __init__(self, name, points=0):
        #Features that the player knows about itself and tells the game.
        #Except for bet, these attributes persist across rounds.
        self.name = name
        self.points = points
        self.bet = 0
        self.active = True
        self.all_in = False
        self.hand = []

    def call(self, points, subpot=None):
        """Place a bet. Might consider renaming this function."""
        points = int(points)
        if points >= self.points:
            points = self.points
            self.all_in = True
            self.active = False
        self.points -= points
        self.bet += points
        return points

    def raise_bet(self, points):
        """Raise or place a bet. Alias of call."""
        return self.call(points=points)
        # self.points -= points
        # self.bet += points
        # return points

    def fold(self):
        """Fold. Returns true (the value expected by the game's update_game
        when a player has just folded).
        """
        self.active = False
        self.hand = None
        self.bet = 0
        return True


if __name__ == '__main__':
    pass
