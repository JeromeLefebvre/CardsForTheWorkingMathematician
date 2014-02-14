from deck import Deck
from player import NormalPlayer,Dealer
from hand import Hand
from card import Card as C

# TODO:
'''
Players are paid according to their bets
A table is a collection of players, a dealer and rules and runMatch
Bet calculations called when gameOver : Need to read rules
'''
class Match(object):

    def __init__(self,players,dealer,table=None,deck=None):

        if isinstance(deck,Deck):
            self.deck=deck
        else:
            self.deck = Deck(8)
            self.deck.shuffle()
        assert(isinstance(players,list) and all(isinstance(player,NormalPlayer) for player in players))
        self.players = players
        self.table = table
        assert(isinstance(dealer,Dealer))
        self.dealer = dealer
        self.currenthand = 0
        self.hands = []
        self.startRound()

    def startRound(self):
        for player in self._players:
            cardstopass = [self.deck.pop(), self.deck.pop()]
            self.hands.append(Hand(cardstopass,player)) # Assuming resplittable true
        self.dealerhand = Hand([self.deck.pop(), self.deck.pop()], self.dealer)
				# If blackjack, pay right away, maybe

    def __str__(self):
        return str(self.hands)+"\n"+str(self.dealerhand)
        #return "Players. %sDealer. %s" % (''.join([str(player) for player in self._players])+"\n", self._dealer) #To be tried with multiple players

    def hit(self):
        assert(self.deck.cardsLeft() > 0)
        self.hands[self.currenthand].hit(self.deck.pop())
        if self.hands[self.currenthand].isBusted():
            self.moveToNextHand()

    def stay(self):
    	 self.moveToNextHand()

    def split(self):
        assert(self.hands[self.currenthand].isSplittable())
        self.hands.insert(self.currenthand+1, self.hands[self.currenthand].split())

    def double(self):
        assert(self.hands[self.currenthand].isDoublable())
        self.hands[self.currenthand].double()
        self.moveToNextHand()

    def moveToNextHand(self):
        self.currenthand = self.currenthand + 1
        if self.table != None: # Update the interface
            #self._table.update()
            pass
        if self.currenthand == len(self.hands):
        	  # dealer's turn
        	  self.dealerTurn()

    def dealerTurn(self):
        # It is the dealer's turn, hit until stand
		# Then call game over, i.e. giving out bets
		# Transfer over the rules for should Hit
		# TODO
        while self.dealerShouldHit():
        	self.dealerhand.hit(self.deck.pop())
        self.gameOver()

    def dealerShouldHit(self):
        ''' shoudHit() -> bool -- returns if the dealer wants to hit or not base on the choice of a 17 rule'''
        if self.table.standOn17:
            return self.dealerhand.bestValue() < 17
        else: # soft17
            if self.dealerhand.bestValue() == 17 and len(self.dealerhand.value()) == 2:
                return True
            elif self.dealerhand.bestValue() >= 17:  # Hard 17 or soft >= 18
                return False
            else:
                return True

    def gameOver(self):
        # compare all hands to the dealer and assign to the players their winnings/loss
        for hand in self.hands:
        	 if hand > self.dealerhand:
        	 	  pass

import unittest
class TestMatch(unittest.TestCase):
    def setup(self):
        pass

    def test_match1(self):
        deck = Deck(listOfCards=[C('K','H'), C('Q','H'),C('5','D'), C('5','S'),C('3','H'),C('3','S')])
        player = NormalPlayer(money=10)
        dealer = Dealer(standOn17=True,soft17=False)
        match = Match(players=[player],dealer=dealer,deck=deck)
        self.assertEqual(player.hand(), Hand([C('3','S'),C('3','H')]))
        self.assertEqual(dealer.hand(), Hand([C('5','S'),C('J','D')]))
        match.hit()
        self.assertEqual(player.hand(), Hand([C('3','S'),C('3','H'),C('J','D')]))
        match.stand()
        self.assertEqual(dealer.hand(), Hand([C('5','S'),C('J','D'),C('Q','H')]))
        # the dealer busted, the game is over, asign money
        self.assertEqual(player.money, 15)
if __name__ == "__main__":
    unittest.main()