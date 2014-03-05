class Card(object):

    def __init__(self, value, suit, prime, string):
        self.value = value
        self.suit = suit  # 1,2,3,4 -> Clubs, Diamonds, Hearts, Spades
        self.prime = prime
        self.string = string

    def __str__(self):
        return self.string
