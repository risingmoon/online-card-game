from card import Card
import random


class Deck(object):

    def __init__(self):
        self.cards = self.populate()
        self.shuffle()

    def populate(self):
        cards = []
        for card in Deck.cards:
            cards.append(Card(*card))
        return cards

    def shuffle(self):
        random.shuffle(self.cards)

    def get_card(self):
        return self.cards.pop()

    def __str__(self):
        s = ''
        for card in self.cards:
            s += str(card) + '\r\n'
        return s

    cards = (
        [
            # Clubs
            (2, 1, "Two of Clubs"),
            (3, 1, "Three of Clubs"),
            (4, 1, "Four of Clubs"),
            (5, 1, "Five of Clubs"),
            (6, 1, "Six of Clubs"),
            (7, 1, "Seven of Clubs"),
            (8, 1, "Eight of Clubs"),
            (9, 1, "Nine of Clubs"),
            (10, 1, "Ten of Clubs"),
            (11, 1, "Jack of Clubs"),
            (12, 1, "Queen of Clubs"),
            (13, 1, "King of Clubs"),
            (14, 1, "Ace of Clubs"),
            # Diamonds
            (2, 2, "Two of Diamonds"),
            (3, 2, "Three of Diamonds"),
            (4, 2, "Four of Diamonds"),
            (5, 2, "Five of Diamonds"),
            (6, 2, "Six of Diamonds"),
            (7, 2, "Seven of Diamonds"),
            (8, 2, "Eight of Diamonds"),
            (9, 2, "Nine of Diamonds"),
            (10, 2, "Ten of Diamonds"),
            (11, 2, "Jack of Diamonds"),
            (12, 2, "Queen of Diamonds"),
            (13, 2, "King of Diamonds"),
            (14, 2, "Ace of Diamonds"),
            # Hearts
            (2, 3, "Two of Hearts"),
            (3, 3, "Three of Hearts"),
            (4, 3, "Four of Hearts"),
            (5, 3, "Five of Hearts"),
            (6, 3, "Six of Hearts"),
            (7, 3, "Seven of Hearts"),
            (8, 3, "Eight of Hearts"),
            (9, 3, "Nine of Hearts"),
            (10, 3, "Ten of Hearts"),
            (11, 3, "Jack of Hearts"),
            (12, 3, "Queen of Hearts"),
            (13, 3, "King of Hearts"),
            (14, 3, "Ace of Hearts"),
            # Spades
            (2, 4, "Two of Spades"),
            (3, 4, "Three of Spades"),
            (4, 4, "Four of Spades"),
            (5, 4, "Five of Spades"),
            (6, 4, "Six of Spades"),
            (7, 4, "Seven of Spades"),
            (8, 4, "Eight of Spades"),
            (9, 4, "Nine of Spades"),
            (10, 4, "Ten of Spades"),
            (11, 4, "Jack of Spades"),
            (12, 4, "Queen of Spades"),
            (13, 4, "King of Spades"),
            (14, 4, "Ace of Spades"),
            ])
