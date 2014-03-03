

class Player:

    def __init__(self, name, points=0):
        self.name = name
        self.points = points
        self.hand = None
        self.active = False
        self.bet = 0

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
        self.hand = None
        self.bet = 0


if __name__ == '__main__':
    pass
