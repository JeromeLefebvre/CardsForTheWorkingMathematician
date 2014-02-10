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
        return "Deck(listOfCards=%r)" % self._cards

    def __str__(self):
        # Note due to the card 10, not all lines are of the exact same character lengths
        string = ''
        for i in range(0, len(self._cards)//52):
            string += ''.join( str(card) for card in self._cards[i*52: (i+1)*52] )
            string += '\n'
        string = string[:-1]
        if len(self._cards) % 52 != 0:
            string += '\n'
            string += ''.join( str(card) for card in self._cards[ 52*(len(self._cards)//52):] )
        return string

    def __eq__(self,other):
        assert(isinstance(other,Deck))
        return self._cards == other._cards

import unittest
class TestHand(unittest.TestCase):
    def test_basic(self):
        dealerDeck = Deck(2)
        self.assertEqual(dealerDeck.cardsLeft(), 52*2)
        dealerDeck.pop()
        self.assertEqual(dealerDeck.cardsLeft(), 52*2 - 1)

    def test_fromList(self):
        dealerDeck = Deck(listOfCards=[Card('K','H')])
        self.assertEqual(dealerDeck.pop(), Card('K','H'))   

    def test_errorRaising(self):
        self.assertRaises(ValueError, Deck, 'a few')
        d = Deck(1)
        for i in range(0,52):
            d.pop()
        self.assertRaises(IndexError, d.pop)

    def test_repr(self):
        dealerDeck = Deck(2)
        dealerDeck.shuffle()
        self.assertEqual(eval(repr(dealerDeck)), dealerDeck)
        self.assertRaises(AssertionError, lambda input:dealerDeck == input, Card('K','H'))        

    def test_str(self):
        # A somewhat a rediculous test
        deck = Deck(listOfCards=[Card(rank='Jack',suit='Hearts'), Card(rank='Ace',suit='Diamonds'), Card(rank='5',suit='Spades'), Card(rank='3',suit='Spades'), Card(rank='8',suit='Hearts'), Card(rank='Queen',suit='Hearts'), Card(rank='6',suit='Spades'), Card(rank='2',suit='Spades'), Card(rank='Queen',suit='Spades'), Card(rank='4',suit='Diamonds'), Card(rank='10',suit='Clubs'), Card(rank='King',suit='Diamonds'), Card(rank='6',suit='Spades'), Card(rank='5',suit='Hearts'), Card(rank='9',suit='Diamonds'), Card(rank='King',suit='Clubs'), Card(rank='10',suit='Hearts'), Card(rank='7',suit='Diamonds'), Card(rank='9',suit='Clubs'), Card(rank='King',suit='Diamonds'), Card(rank='10',suit='Diamonds'), Card(rank='Queen',suit='Clubs'), Card(rank='8',suit='Clubs'), Card(rank='King',suit='Spades'), Card(rank='4',suit='Spades'), Card(rank='10',suit='Diamonds'), Card(rank='7',suit='Clubs'), Card(rank='6',suit='Clubs'), Card(rank='Jack',suit='Diamonds'), Card(rank='2',suit='Clubs'), Card(rank='4',suit='Hearts'), Card(rank='3',suit='Diamonds'), Card(rank='9',suit='Hearts'), Card(rank='5',suit='Clubs'), Card(rank='Ace',suit='Spades'), Card(rank='9',suit='Spades'), Card(rank='5',suit='Diamonds'), Card(rank='Jack',suit='Spades'), Card(rank='7',suit='Spades'), Card(rank='7',suit='Spades'), Card(rank='10',suit='Clubs'), Card(rank='Jack',suit='Clubs'), Card(rank='6',suit='Diamonds'), Card(rank='4',suit='Clubs'), Card(rank='3',suit='Diamonds'), Card(rank='6',suit='Hearts'), Card(rank='Queen',suit='Diamonds'), Card(rank='3',suit='Hearts'), Card(rank='7',suit='Hearts'), Card(rank='6',suit='Diamonds'), Card(rank='4',suit='Hearts'), Card(rank='8',suit='Spades'), Card(rank='4',suit='Diamonds'), Card(rank='9',suit='Spades'), Card(rank='Ace',suit='Clubs'), Card(rank='10',suit='Spades'), Card(rank='8',suit='Clubs'), Card(rank='8',suit='Diamonds'), Card(rank='9',suit='Clubs'), Card(rank='Ace',suit='Clubs'), Card(rank='5',suit='Hearts'), Card(rank='Ace',suit='Diamonds'), Card(rank='9',suit='Diamonds'), Card(rank='10',suit='Hearts'), Card(rank='3',suit='Spades'), Card(rank='8',suit='Hearts'), Card(rank='2',suit='Hearts'), Card(rank='7',suit='Diamonds'), Card(rank='Jack',suit='Hearts'), Card(rank='5',suit='Clubs'), Card(rank='8',suit='Spades'), Card(rank='5',suit='Spades'), Card(rank='Ace',suit='Spades'), Card(rank='Jack',suit='Diamonds'), Card(rank='2',suit='Diamonds'), Card(rank='Queen',suit='Clubs'), Card(rank='4',suit='Spades'), Card(rank='2',suit='Diamonds'), Card(rank='2',suit='Spades'), Card(rank='Ace',suit='Hearts'), Card(rank='Jack',suit='Clubs'), Card(rank='King',suit='Hearts'), Card(rank='Ace',suit='Hearts'), Card(rank='10',suit='Spades'), Card(rank='6',suit='Clubs'), Card(rank='8',suit='Diamonds'), Card(rank='7',suit='Clubs'), Card(rank='Queen',suit='Spades'), Card(rank='4',suit='Clubs'), Card(rank='3',suit='Clubs'), Card(rank='2',suit='Hearts'), Card(rank='King',suit='Spades'), Card(rank='5',suit='Diamonds'), Card(rank='Jack',suit='Spades'), Card(rank='2',suit='Clubs'), Card(rank='King',suit='Clubs'), Card(rank='Queen',suit='Hearts'), Card(rank='7',suit='Hearts'), Card(rank='3',suit='Clubs'), Card(rank='3',suit='Hearts'), Card(rank='9',suit='Hearts'), Card(rank='King',suit='Hearts'), Card(rank='6',suit='Hearts')])
        self.assertEqual(str(deck), "J♥A♦5♠3♠8♥Q♥6♠2♠Q♠4♦10♣K♦6♠5♥9♦K♣10♥7♦9♣K♦10♦Q♣8♣K♠4♠10♦7♣6♣J♦2♣4♥3♦9♥5♣A♠9♠5♦J♠7♠7♠10♣J♣6♦4♣3♦6♥Q♦3♥7♥6♦4♥8♠\n4♦9♠A♣10♠8♣8♦9♣A♣5♥A♦9♦10♥3♠8♥2♥7♦J♥5♣8♠5♠A♠J♦2♦Q♣4♠2♦2♠A♥J♣K♥A♥10♠6♣8♦7♣Q♠4♣3♣2♥K♠5♦J♠2♣K♣Q♥7♥3♣3♥9♥K♥6♥")

if __name__ == '__main__':
    unittest.main()
