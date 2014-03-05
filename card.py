class Card(object):

    def __init__(self, value, suit, prime, string):
        self.value = value  # 2,3,4,5,6,7,8,9,10,11,12,13,14 for 2-Ace
        self.suit = suit  # 1,2,3,4 -> Clubs, Diamonds, Hearts, Spades
        self.prime = prime  # 2,3,5,7,11,13,17,19,23,29,31,37,41 for 2-Ace
        self.string = string  # 'Eight of Hearts', 'Queen of Spades', etc.

    def __str__(self):
        return self.string
