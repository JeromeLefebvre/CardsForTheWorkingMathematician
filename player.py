#-------------------------------------------------------------------------------
# Name:        player.py
# Purpose:
#
# Author:      marioga
#
# Created:     05/02/2014
# Copyright:   (c) marioga 2014
#-------------------------------------------------------------------------------

from card import Card
from hand import Hand

class Player(object):
    def __init__(self, hand=None, money=0, name="Player"):
        if isinstance(hand,Hand):
            self._hand = [hand]
        try:
            self._money = int(money)
        except ValueError:
            raise ValueError("Money needs to be an integer")
        try:
            self._name = str(name)
        except:
            raise ValueError("Name is not valid, but I'd like to call you John")

    def hand(self):
        '''Getter for _hand'''
        return self._hand

    def money(self):
        '''Getter for _money'''
        return self._money

    def name(self):
        '''Getter for _name'''
        return self._name

    def __str__(self):
        '''Nice representation for player'''
        return "Name: %s, Cards: %s" % (self.name(), self.hand())

    def hit(self,card):
        ''' Here we update a player class after a hit'''
        if isinstance(card,Card):
            self._hand.receive(card)

    def updateAfterStay(self):
        ''' Here we update a player class after a stay; so far nothing happens'''
        pass

class NormalPlayer(Player):
    '''This class corresponds to normal players in the table'''
    def __init__(self, hand=None, money=0, name = "Player"):
        Player.__init__(self, hand, money, name)
        self._issplit=False

    def startMatch(self,cards):
        self._hand=Hand(cards)

    def hasEnoughToBet(self,bet=0):
        '''Check whether a player has enough to bet'''
        return self.money()>=bet

    def isSplit(self):
        '''Check whether the player has split.'''
        return self._issplit

    def extraChips(self,dollar):
        ''' extraChips(int) -> None -- Receive dollar worth of money'''
        assert(dollar >= 0)
        self._money += dollar

    def updateAfterDouble(self,card,bet=0):
        '''Updates player's instance after doubling and makes sure player has enough'''
        try:
            if self.hasEnoughToBet(int(bet)):
                self._money-=bet
                self._hand.receive(card)
            else:
                print("Not enough money to double")
        except ValueError:
            print ("Bet is not an integer")

    def updateAfterSplit(self,bet=0):
        '''Updates player after he split his pair. Creates an alternative hand'''
        try:
            if self.hasEnoughToBet(int(bet)):
                self._money-=bet
                self._secondhand = self._hand.split()
                self._issplit=True
            else:
                print("Not enough money to double")
        except ValueError:
            print ("Bet is not an integer")

    def updateAfterSecondHit(self):
        pass

    def updateAfterBet(self,bet=0):
        '''Updates player's money after betting and makes sure player has enough'''
        try:
            if self.hasEnoughToBet(int(bet)):
                self.money-=bet
            else:
                print("Not enough money to bet")
        except ValueError:
            print ("Bet is not an integer")

class Dealer(Player):
    '''This class corresponds to the dealer. We assign no money to it and interpret
    its money as wins or losses for the house'''
    def __init__(self, hand=None):
        Player.__init__(self, hand, 0, "Dealer")

    def startMatch(self,cards,withholecard=True):
        '''Deals initial cards to the dealer'''
        if withholecard:
            self._hand=Hand(cards[0])
            self._holecard=cards[1]
        else:
            self._hand=Hand(cards)

    def flipHoleCard(self):
        '''Adds the holecard to the hand'''
        self._hand.receive(self._holecard)

import unittest

class TestPlayer(unittest.TestCase):
    def setUp(self):
        pass

    def test_basicPlayer(self):
        pass

if __name__ == '__main__':
    #unittest.main()
    
    myplayer = NormalPlayer(Hand([Card(),Card()]),5)
    print(myplayer)
    print(myplayer.hand().value())
    myplayer.updateAfterHit(Card())
    print(myplayer)
    print(myplayer.hand().value())
    myplayer.updateAfterDouble(Card(),5)
    print(myplayer)
    print(myplayer.hand().value())
    myplayer.updateAfterDouble(Card(),5)
    print(myplayer)
    print(myplayer.hand().value())


