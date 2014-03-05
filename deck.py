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
            (2, 1, 2, "Two of Clubs"),
            (3, 1, 3, "Three of Clubs"),
            (4, 1, 5, "Four of Clubs"),
            (5, 1, 7, "Five of Clubs"),
            (6, 1, 11, "Six of Clubs"),
            (7, 1, 13, "Seven of Clubs"),
            (8, 1, 17, "Eight of Clubs"),
            (9, 1, 19, "Nine of Clubs"),
            (10, 1, 23, "Ten of Clubs"),
            (11, 1, 29, "Jack of Clubs"),
            (12, 1, 31, "Queen of Clubs"),
            (13, 1, 37, "King of Clubs"),
            (14, 1, 41, "Ace of Clubs"),
            # Diamonds
            (2, 2, 2, "Two of Diamonds"),
            (3, 2, 3, "Three of Diamonds"),
            (4, 2, 5, "Four of Diamonds"),
            (5, 2, 7, "Five of Diamonds"),
            (6, 2, 11, "Six of Diamonds"),
            (7, 2, 13, "Seven of Diamonds"),
            (8, 2, 17, "Eight of Diamonds"),
            (9, 2, 19, "Nine of Diamonds"),
            (10, 2, 23, "Ten of Diamonds"),
            (11, 2, 29, "Jack of Diamonds"),
            (12, 2, 31, "Queen of Diamonds"),
            (13, 2, 37, "King of Diamonds"),
            (14, 2, 41, "Ace of Diamonds"),
            # Hearts
            (2, 3, 2, "Two of Hearts"),
            (3, 3, 3, "Three of Hearts"),
            (4, 3, 5, "Four of Hearts"),
            (5, 3, 7, "Five of Hearts"),
            (6, 3, 11, "Six of Hearts"),
            (7, 3, 13, "Seven of Hearts"),
            (8, 3, 17, "Eight of Hearts"),
            (9, 3, 19, "Nine of Hearts"),
            (10, 3, 23, "Ten of Hearts"),
            (11, 3, 29, "Jack of Hearts"),
            (12, 3, 31, "Queen of Hearts"),
            (13, 3, 37, "King of Hearts"),
            (14, 3, 41, "Ace of Hearts"),
            # Spades
            (2, 4, 2, "Two of Spades"),
            (3, 4, 3, "Three of Spades"),
            (4, 4, 5, "Four of Spades"),
            (5, 4, 7, "Five of Spades"),
            (6, 4, 11, "Six of Spades"),
            (7, 4, 13, "Seven of Spades"),
            (8, 4, 17, "Eight of Spades"),
            (9, 4, 19, "Nine of Spades"),
            (10, 4, 23, "Ten of Spades"),
            (11, 4, 29, "Jack of Spades"),
            (12, 4, 31, "Queen of Spades"),
            (13, 4, 37, "King of Spades"),
            (14, 4, 41, "Ace of Spades"),
            ])
