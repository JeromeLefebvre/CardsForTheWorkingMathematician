from deck import Deck
from player import NormalPlayer,Dealer
from hand import Hand
from card import Card as C

# TODO:
'''
Bet proprety to players
Add bet to hands in split
Players are paid according to their bets
Change splitting rule to hand
A table is a collection of players, a dealer and rules and runMatch
Bet calculations called when gameOver : Need to read rules

'''
class Match(object):

    def __init__(self,players,dealer,table=None,deck=None):

        if isinstance(deck,Deck):
            self._deck=deck
        else:
            self._deck = Deck(8)
            self._deck.shuffle()
        assert(isinstance(players,list) and all(isinstance(player,NormalPlayer) for player in players))
        self._players = players

        self._table = table
        assert(isinstance(dealer,Dealer))
        self._dealer = dealer
        self._currentHand = 0

        self._hands = []
        self.startRound()

    def startRound(self):
        for player in self._players:
            cardsToPass = [self._deck.pop(), self._deck.pop()]
            self._hands.append(Hand(cardsToPass,player))
        self._dealerHand = Hand([self._deck.pop(), self._deck.pop(), self._dealer])
				# If blackjack, pay right away, maybe

    def __str__(self):
    	  return str(self._hands)
        #return "Players. %sDealer. %s" % (''.join([str(player) for player in self._players])+"\n", self._dealer) #To be tried with multiple players

    def hit(self):
        assert(self._deck.cardsLeft() > 0)
        self._hands[self._currentHand].hit(self._deck.pop())
        if self._hands[self._currentHand].isBusted():
            self.killHand()

    def stay(self):
    	 self.killHand()

    def split(self):
        assert(self._hands[self._currentHand].isSplittable()) # Update Hand function to check if player has the funds and is a pair
        self._hands.insert(self._currentHand+1, self._hands[self._currentHand].split()  )

    def double(self):
        assert(self._hands[self._currentHand].isDoublable())
        self._hands[self._currentHand].double()
        self.killHand()

    def killHand(self):
        self._currentHand = self._currentHand + 1
        if self._table: # Update the interface
            #self._table.update()
            pass
        if self._currentHand == len(self._hands):
        	  # dealer's turn
        	  self.dealerTurn()

    def dealerTurn(self):
        # It is the dealer's turn, hit until stand
		# Then call game over, i.e. giving out bets
		# Transfer over the rules for should Hit
		# TODO
        while self.dealerShouldHit():
        	self._dealerHand.hit(self.deck.pop())
        self.gameOver()

    def dealerShouldHit(self):
        ''' shoudHit() -> bool -- returns if the dealer wants to hit or not base on the choice of a 17 rule'''
        if self._table._standOn17:
            return self._dealerHand.bestValue() < 17
        else: # soft17
            if self._dealerHand.bestValue() == 17 and len(self._dealerHand.value()) == 2:
                return True
            elif self._dealerHand.bestValue() >= 17:  # Hard 17 or soft >= 18
                return False
            else:
                return True

    def gameOver(self):
        # compare all hands to the dealer and assign to the players their winnings/loss
        for hand in self._hands:
        	 if hand > self._dealerHand:
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