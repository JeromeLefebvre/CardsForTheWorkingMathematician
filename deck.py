#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      marioga
#
# Created:     05/02/2014
# Copyright:   (c) marioga 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

''' This is the implementation of the deck class. A "deck" consists of _size
decks of 52 cards.
'''
from random import shuffle
import unittest

from card import Card


class Deck:
    def __init__(self, size=8):
        try:
            self._size = int(size)
        except ValueError:
            print ("Input for deck is not an integer")
        # We now populate the deck
        self._cards = []
        for num_decks in range(self._size):
            for rank in range(13):
                for suit in range(4):
                    self._cards.append(Card(rank,suit))

    def pop(self):
        ''' pop() -> Card -- returns the top of the card '''
        return self._cards.pop()

    def cardsLeft(self):
        ''' cardsLeft() -> int -- returns the number of cards left '''
        return len(self._cards)

    def shuffle(self):
        ''' shuffle() -> None -- shuffles the deck in place '''
        shuffle(self._cards)

class TestHand(unittest.TestCase):
    def setup(self):
        pass

    def test_basic(self):
        self.dealerDeck = Deck(2)
        self.assertEqual(self.dealerDeck.cardsLeft(), 52*2)
        self.dealerDeck.pop()
        self.assertEqual(self.dealerDeck.cardsLeft(), 52*2 - 1)

if __name__ == '__main__':
    unittest.main()
