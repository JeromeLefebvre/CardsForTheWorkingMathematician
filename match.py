from deck import Deck
from player import NormalPlayer, Dealer
from hand import Hand
from card import Card as C
from game import Game
'''
# TODO:
Players are paid according to their bets
A game is a collection of players, a dealer and rules and runMatch
Bet calculations called when gameOver : Need to read rules
'''
class Match(object):
    def __init__(self,players,dealer,game,deck=None):
        if isinstance(deck,Deck):
            self.deck=deck
        else:
            self.deck = Deck(8)
            self.deck.shuffle()
        assert(isinstance(players,list) and all(isinstance(player,NormalPlayer) for player in players))
        self.players = players
        self.game = game
        assert(isinstance(dealer,Dealer))
        self.dealer = dealer
        self.currenthand = 0
        self.hands = []
        self.game = game
        self.surrendered = {}
        self.startRound()
        self.insurance = {player:0 for player in self.players}

    def startRound(self):
        for player in self.players:
            cardstopass = [self.deck.pop(), self.deck.pop()]
            newHand = Hand(cardstopass,player)
            self.hands.append(newHand) # Assuming resplittable true
        self.dealerhand = Hand([self.deck.pop(), self.deck.pop()], self.dealer)
        if self.dealerhand.cards[0].isAce(): # assuming 0 is the hole hand
            for player in self.players:
                self.insurance[player] = player.offerInsurance()
        if self.dealerhand.isBlackJack():
            self.dealerHasBlackJack()
        if self.game.rules["surrender"]:
            for hand in self.hands:
                if hand.player.offerSurrender():
                    # The hand should be deleted and the player get his money back
                    pass

    def dealerHasBlackJack(self):
        self.gameOver()

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
        if self.currenthand == len(self.hands): # dealer's turn
              self.dealerTurn()

    def dealerTurn(self):
        # TODO: There should be an an appeal to the user interface here to turn over the dealer card.
        while self.dealerShouldHit():
            self.dealerhand.hit(self.deck.pop())
        self.gameOver()

    def dealerShouldHit(self):
        ''' shoudHit() -> bool -- returns if the dealer wants to hit or not based on the choice of a 17 rule'''
        if self.game.rules['standonsoft17']:
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
        deck = Deck(listOfCards=[C('K','H'), C('Q','H'),C('J','D'),C('5','D'), C('5','S'),C('3','H'),C('3','S')])
        game = Game()
        player = NormalPlayer(money=10)
        dealer = Dealer()
        match = Match(players=[player],dealer=dealer,deck=deck,game=game)
        self.assertEqual(match.hands, [Hand([C('3','S'),C('3','H')])])
        self.assertEqual(match.dealerhand, Hand([C('5','S'),C('5','D')]))
        match.hit()
        self.assertEqual(match.hands, [Hand([C('3','S'),C('3','H'),C('J','D')])])
        match.stay()
        self.assertEqual(match.dealerhand, Hand([C('5','S'),C('5','D'),C('Q','H')]))
        # the dealer busted, the game is over, asign money
        #self.assertEqual(player.money, 15)
if __name__ == "__main__":
    unittest.main()