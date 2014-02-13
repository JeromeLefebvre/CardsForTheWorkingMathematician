from card import Card
from hand import Hand

class Player(object):
    def __init__(self, money=0, name="Player"):
        assert(isinstance(money,int)) # money needs to be an integer
        self.money = money
        assert(isinstance(name,str)) # name needs to be a string
        self.name = name

    def __str__(self):
        '''Nice representation for player'''
        return "Name: %s, Money: %s" % (self.name(), self.money())

class NormalPlayer(Player):
    '''This class corresponds to normal players in the table'''
    def __init__(self, money=0, name="John", bet=0):
        Player.__init__(self, money, name)
        self.bet=bet

    def canBet(self,bet):
        '''canBet() -> bool -- Checks whether the player has enough to bet'''
        return self.money>=self.bet

    def betMoney(self):
        '''Subtract bet from the player's money'''
        self.money-=self.bet

    def collectMoney(self, amount):
        ''' collectBet(int) -> None -- A win is recorded in the player's money'''
        assert(amount>=0)
        self.money += amount

    def extraChips(self, dollar):
        ''' extraChips(int) -> None -- Receive dollar worth of money'''
        assert(dollar >= 0)
        self._money += dollar


class Dealer(Player):
    '''This class corresponds to the dealer. We assign no money to it and interpret
    its money as wins or losses for the house'''
    def __init__(self,name="Malkovich"):
        Player.__init__(self, 0, name)


    def updateHouseMoney(self,amount):
        self.money+=amount

import unittest
class TestPlayer(unittest.TestCase):
    def test_basicPlayer(self):
        pass

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

''' TO BE DEALT WITH FOR A DIFFERENT TESTING UNIT'''
##    def test_dealer(self):
##        aDealer = Dealer(standOn17=True)
##        aDealer.startMatch([Card('K'), Card('7')]) # hit 17
##        self.assertFalse(aDealer.shouldHit())
##
##        aDealer = Dealer(standOn17=True)
##        aDealer.startMatch([Card('K'), Card('6')]) # Below 17
##        self.assertTrue(aDealer.shouldHit())
##
##        aDealer = Dealer(standOn17=True)
##        aDealer.startMatch([Card('A'), Card('6')]) # shoft 17
##        self.assertFalse(aDealer.shouldHit())
##
##
##        aDealer = Dealer(soft17=True)
##        aDealer.startMatch([Card('A'), Card('6')]) # soft 17
##        self.assertTrue(aDealer.shouldHit())
##
##        aDealer = Dealer(soft17=True)
##        aDealer.startMatch([Card('K'), Card('7')]) # hard 17
##        self.assertFalse(aDealer.shouldHit())
##
##        aDealer = Dealer(soft17=True)
##        aDealer.startMatch([Card('K'), Card('6'), Card('2')]) # hard 18
##        self.assertFalse(aDealer.shouldHit())

if __name__ == '__main__':
    unittest.main()