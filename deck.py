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
from card import card
<<<<<<< HEAD
from random import randrange, shuffle
=======
from random import shuffle
>>>>>>> bcc4e68503b61c16220bd43377e5d8a942a6f97f

class deck:
    def __init__(self, size=8):
        try:
            self._size=int(size)
        except ValueError:
            print ("Input for deck is not an integer")
        # We now populate the deck
        self._cards=[]
        for num_decks in range(self._size):
            for rank in range(13):
                for suit in range(4):
                    self._cards.append(card(rank,suit))

    def pop(self):
        return self._cards.pop()

    def cardsLeft(self):
        return len(self._cards)

    def shuffle(self):
        shuffle(self._cards)

import unittest
class TestHand(unittest.TestCase):
    def setup(self):
        pass

    def test_basic(self):
        self.dealerdeck = deck(2)
        self.assertEqual(self.dealerdeck.cardsLeft(), 52*2)
        self.dealerdeck.pop()
        self.assertEqual(self.dealerdeck.cardsLeft(), 52*2 - 1)

if __name__ == '__main__':
    unittest.main()
    d = deck()
    d.shuffle()
    print (d.pop())
    print (d.cardsLeft())
    print (d.pop())
    print (d.cardsLeft())

