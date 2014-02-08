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
            # Name is not a private variable
            self.name = str(name)
        except:
            raise ValueError("Name is not valid, but I'd like to call you John")

    def hand(self):
        '''Getter for _hand'''
        return self._hand

    def money(self):
        '''Getter for _money'''
        return self._money

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

    def canBet(self,bet):
        '''canBet() -> bool -- Checks whether the player has enough to bet'''
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

'''
"Dealer stands on all 17s": In this case, the dealer must continue to take cards ("hit") 
until his total is 17 or greater. An Ace in the dealer's hand is always counted as 11 if
 possible without the dealer going over 21. For example, (Ace,8) would be 19 and the 
 dealer would stop drawing cards ("stand"). Also, (Ace,6) is 17 and again the dealer will stand. 
 (Ace,5) is only 16, so the dealer would hit. He will continue to draw cards until the hand's value 
 is 17 or more. For example, (Ace,5,7) is only 13 so he hits again. (Ace,5,7,5) makes 18 
 so he would stop ("stand") at that point.

Dealer hits soft 17": Some casinos use this rule variation instead. This rule is identical except 
for what happens when the dealer has a soft total of 17. Hands such as (Ace,6), (Ace,5,Ace), and 
(Ace, 2, 4) are all examples of soft 17. The dealer hits these hands, and stands on soft 18 or higher,
 or hard 17 or higher. When this rule is used, the house advantage against the players is slightly increased.
'''
class Dealer(Player):
    '''This class corresponds to the dealer. We assign no money to it and interpret
    its money as wins or losses for the house'''
    def __init__(self, hand=None,name="Malkovich", standOn17=False, soft17=False):
        Player.__init__(self, hand, 0, "Dealer")
        assert(standOn17 ^ soft17) # Dealer can only follow one rule
        self._standOn17 = standOn17
        self._soft17 = soft17

    def startMatch(self,cards,withholecard=False):
        '''Deals initial cards to the dealer'''
        if withholecard:
            self._hand=Hand(cards[0])
            self._holecard=cards[1]
        else:
            self._hand=Hand(cards)

    def flipHoleCard(self):
        '''Adds the holecard to the hand'''
        self._hand.receive(self._holecard)

    def shouldHit(self):
        ''' shoudHit() -> bool -- returns if the dealer wants to hit or not base on the choice of a 17 rule'''
        if self._standOn17:
            return self._hand.bestValue() < 17
        elif self._soft17:
            # Soft 17
            if self._hand.bestValue() == 17 and len(self._hand.value()) == 2:
                return True
            # Hard 17 or soft >= 18
            elif self._hand.bestValue() >= 17:
                return False
            else:
                return True
        else:
            raise ValueError("Dealer is not setup well")

import unittest
class TestPlayer(unittest.TestCase):
    def setUp(self):
        pass

    def test_basicPlayer(self):
        pass

    def test_dealer(self):
        aDealer = Dealer(standOn17=True)
        aDealer.startMatch([Card('K'), Card('7')]) # hit 17
        self.assertFalse(aDealer.shouldHit())

        aDealer = Dealer(standOn17=True)
        aDealer.startMatch([Card('K'), Card('6')]) # Below 17
        self.assertTrue(aDealer.shouldHit())

        aDealer = Dealer(standOn17=True)
        aDealer.startMatch([Card('A'), Card('6')]) # shoft 17
        self.assertFalse(aDealer.shouldHit())     


        aDealer = Dealer(soft17=True)
        aDealer.startMatch([Card('A'), Card('6')]) # soft 17
        self.assertTrue(aDealer.shouldHit())

        aDealer = Dealer(soft17=True)
        aDealer.startMatch([Card('K'), Card('7')]) # hard 17
        self.assertFalse(aDealer.shouldHit())

        aDealer = Dealer(soft17=True)
        aDealer.startMatch([Card('K'), Card('6'), Card('2')]) # hard 18
        self.assertFalse(aDealer.shouldHit())   

if __name__ == '__main__':
    unittest.main()
    
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


