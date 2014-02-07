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

    def updateAfterHit(self,card):
        ''' Here we update a player class after a hit'''
        if isinstance(card,Card):
            self._hand.receive(card)

    def updateAfterStay(self):
        ''' Here we update a player class after a stay; so far nothing happens'''
        pass


class NormalPlayer(Player):
    '''This class corresponds to normal players in the table'''
    def __init__(self, hand=None, money=0, name = "Stranger"):
        Player.__init__(self, hand, money, name)
        self._issplit=False

    def hasEnoughToBet(self,bet):
        '''Check whether a player has enough to bet'''
        return self.money()>=bet

    def isSplit(self):
        '''Check whether the player has split.'''
        return self._issplit


    def updateAfterDouble(self,card,bet):
        '''Updates player's instance after doubling and makes sure player has enough'''
        try:
            if self.hasEnoughToBet(int(bet)):
                self._money-=bet
                self._hand.receive(card)
            else:
                print("Not enough money to double")
        except ValueError:
            print ("Bet is not an integer")

    def updateAfterSplit(self,bet):
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


    def updateAfterBet(self,bet):
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

if __name__ == '__main__':
    myplayer=NormalPlayer(Hand([Card(),Card()]),5)
    myplayer.displayHand()
    print (myplayer.hand().value())
    myplayer.updateAfterHit(Card())
    myplayer.displayHand()
    print (myplayer.hand().value())
    myplayer.updateAfterDouble(Card(),5)
    myplayer.displayHand()
    print (myplayer.hand().value())
    myplayer.updateAfterDouble(Card(),5)
    myplayer.displayHand()
    print (myplayer.hand().value())


