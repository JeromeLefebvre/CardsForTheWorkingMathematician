#-------------------------------------------------------------------------------
# Name:        deck.py
# Purpose:
#
# Author:      marioga
#
# Created:     05/02/2014
# Copyright:   (c) marioga 2014
#-------------------------------------------------------------------------------

''' This is the implementation of the deck class. A "deck" consists of _size
decks of 52 cards.
'''
from random import shuffle
import unittest

from card import Card


class Deck(object):
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
        ''' pop() -> Card -- returns the card on top of the deck '''
        return self._cards.pop()

    def cardsLeft(self):
        ''' cardsLeft() -> int -- returns the number of cards left '''
        return len(self._cards)

    def shuffle(self):
        ''' shuffle() -> None -- shuffles the deck in place '''
        shuffle(self._cards)

    def __repr__(self):
        return "Deck(%r)" % self._size

    def __str__(self):
        # Note due to the card 10, not all lines are of the same lengths
        string = ''
        for i in range(0, len(self._cards)//52):
            string += ''.join( str(card) for card in self._cards[i*52: (i+1)*52] )
            string += '\n'
        string = string[:-1]
        if len(self._cards) % 52 != 0:
            string += '\n'
            string += ''.join( str(card) for card in self._cards[ 52*(len(self._cards)//52):] )
        return string

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
