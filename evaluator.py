from itertools import combinations
from pickle import load


class Evaluator(object):

    def __init__(self):
        '''
        Loads dictionaries from pickle filesThe dictionaries contain a
        unique key for every possible five card hand, mapped to a tuple
        of the corresponding hand's rank and the name of that hand.
        '''
        with open('rank_table.pickle', 'rb') as infile:
            self.rank_table = load(infile)
        infile.close()
        with open('flush_rank_table.pickle', 'rb') as infile:
            self.flush_rank_table = load(infile)
        infile.close()

    def get_best(self, seven_cards):
        '''Iterates through all five card combinations among the seven card
        hand and returns a tuple of the best hand\'s rank, name, and list of
        the five cards comprising that best hand.'''
        if len(seven_cards) != 7:
            raise ValueError('Must pass 7 card hand.')
        possible_hands_iter = combinations(seven_cards, 5)
        best_rank = 7463  # Worst possible actual rank is 7462
        best_string = None
        best_cards = None
        while True:
            try:
                current_hand = possible_hands_iter.next()
                rank, string = self.get_rank_and_string(current_hand)
                if rank < best_rank:
                    best_rank = rank
                    best_string = string
                    best_cards = current_hand
            except StopIteration:
                return best_rank, best_string, best_cards

    def get_rank_and_string(self, five_cards):
        '''Returns a tuple of the rank and name of the hand the five passed
        cards represent.'''
        hashed = 1
        for card in five_cards:
            hashed *= card.prime
        if self.is_flush(five_cards):
            return self.flush_rank_table[hashed]
        return self.rank_table[hashed]

    def is_flush(self, cards):
        suit = cards[0].suit
        if all(card.suit == suit for card in cards):
            return True
        return False
