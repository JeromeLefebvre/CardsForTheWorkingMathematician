#-------------------------------------------------------------------------------
# Name:        deck.py
# Purpose:     The deck class for a card game
#
# Author:      Mario, Jerome
#
# Created:     05/02/2014
# Copyright:   (c) marioga 2014
#-------------------------------------------------------------------------------

from random import shuffle

from card import Card

class Deck(object):
    def __init__(self, size=8,listOfCards=None):
        if listOfCards != None:
            self._cards = listOfCards
        else:
            try:
                self._size = int(size)
            except ValueError:
                raise ValueError("Input for deck is not an integer")
            # We now populate the deck
            self._cards = []
            for num in range(self._size):
                for rank in range(13):
                    for suit in range(4):
                        self._cards.append(Card(rank,suit))

    def pop(self):
        ''' pop() -> Card -- returns the card on top of the deck '''
        try:
            return self._cards.pop()
        except IndexError:
            raise IndexError("Get yourself new cards")

    def cardsLeft(self):
        ''' cardsLeft() -> int -- returns the number of cards left '''
        return len(self._cards)

    def shuffle(self):
        ''' shuffle() -> None -- shuffles the deck in place '''
        shuffle(self._cards)

    def __repr__(self):
        return "Deck(%r)" % self._size

    def __str__(self):
        # Note due to the card 10, not all lines are of the exact same lengths
        string = ''
        for i in range(0, len(self._cards)//52):
            string += ''.join( str(card) for card in self._cards[i*52: (i+1)*52] )
            string += '\n'
        string = string[:-1]
        if len(self._cards) % 52 != 0:
            string += '\n'
            string += ''.join( str(card) for card in self._cards[ 52*(len(self._cards)//52):] )
        return string

import unittest
class TestHand(unittest.TestCase):
    def setup(self):
        pass

    def test_basic(self):
        dealerDeck = Deck(2)
        self.assertEqual(dealerDeck.cardsLeft(), 52*2)
        dealerDeck.pop()
        self.assertEqual(dealerDeck.cardsLeft(), 52*2 - 1)

    def test_errorRaising(self):
        self.assertRaises(ValueError, Deck, 'a few')
        d = Deck(1)
        for i in range(0,52):
            d.pop()
        self.assertRaises(IndexError, d.pop)

if __name__ == '__main__':
    unittest.main()
