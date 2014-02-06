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
    def __init__(self, hand=None, money=0, name = "Stranger"):
        if isinstance(hand,Hand):
            self._hand=hand
        try:
            self._money=int(money)
        except ValueError:
            print ("Money is not an integer")
        try:
            self._name=str(name)
        except:
            print ("Name is not valid")

    def hand(self):
        '''Getter for _hand'''
        return self._hand

    def money(self):
        '''Getter for _money'''
        return self._money

    def name(self):
        '''Getter for _name'''
        return self._name

    def displayHand(self):
        ''' Displays player's hand'''
        self._hand.displayCards()

class NormalPlayer(Player):
    def __init__(self, hand=None, money=0, name = "Stranger"):
        Player.__init__(self, hand, money, name)

    def updateAfterBet(self,n):
        '''Updates player's money after betting and makes sure player has enough'''
        try:
            if self._money<int(n):
                print("Not enough money")
            else:
                self._money-=n
        except ValueError:
            print ("Bet is not an integer")

    def hit(self):
        pass

class Dealer(Player):
    def __init__(self, hand=None):
        Player.__init__(self, hand, 0, "Dealer")

if __name__ == '__main__':
    myplayer=NormalPlayer(Hand([Card('K'),Card('3')]))
    myplayer.displayHand()

