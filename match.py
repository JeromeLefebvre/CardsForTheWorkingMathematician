from deck import Deck
from player import NormalPlayer,Dealer
from hand import Hand
from card import Card as C
class Match(object):

    _PLAY_OPTIONS = {'H':"(H)it",'D':"(D)ouble",'S':"(S)tay",'P':"s(P)lit"}
    def __init__(self,table=None,players=None,dealer=None,deck=None):
        if isinstance(deck,Deck):
            self._deck=deck
        else:
            self._deck = Deck(8)
            self._deck.shuffle()
        if isinstance(players,list) and all(isinstance(player,NormalPlayer) for player in players):
            self._players = players
        else:
            self._players = [NormalPlayer()]
        self._table = table

        # If more than one player for one sitting ask the name of each player
        if len(self._players) > 1:
            for index, player in enumerate(self._players):
                name = self._table.feedback("Enter the name of player 1: ")

        if isinstance(dealer,Dealer):
            self._dealer = dealer
        else:
            self._dealer = Dealer()
        self._currentHand = 0
        if self._table:
            self.collectBets()
        self._hands = []
        self.startRound()

    def split(self):
        ''' split() -> None -- Splits the card of the currentPlayer if he has a pair or enough money'''
        currentHand = self.hands[self._currentHand]
        if not currentHand.isPair():
            print("You can only split a pair on your first hand")
            return
        if not currentHand.player.canBet(self.bets[current]):
            print("You need matching funds to split a hand")
            return
        newHand = currentHand.split()
        self._hands.insert(self._currentHand, newHand)
        self.handFinish()

    def handFinish(self):
        self.gameIsOver()
        self._currentHand = (self._currentHand + 1 if self._currentHand + 1 < len(self._hands) else 0)
        if self._table:
            self._table.prompt = "(" + self._hands[self._currentHand].player.name + ")"
        if isinstance(self._hands[self._currentHand].player, Dealer):
            self.hit()

    def collectBets(self):
        self.bets = {}
        for player in self._players:
            self.bets[player] = self._table.collectBets(player.name)

    def setBet(self):
        # Need to think of how match handles bet
        pass

    def dealerBust(self):
        ''' dealerBust() -> None -- if the dealer bust, every remeaning hands wins'''

    def startRound(self):
        for player in self._players:
            cardsToPass = [self._deck.pop(), self._deck.pop()]
            self._hands.append( player.startMatch(cardsToPass) )
        self._hands.append( self._dealer.startMatch([self._deck.pop(), self._deck.pop()]) )
        self._PLAY_CALLS = {'H':self.hit,'D':self.double,'S':self.stay,'P':self.split} #Whoa! A dictionary that we'll use to call functions!

    def __str__(self):
        return "Players. %sDealer. %s" % (''.join([str(player) for player in self._players])+"\n", self._dealer) #To be tried with multiple players

    def playerBuysIn(self,dollars):
        ''' playerBuysIn(dollars) -> None -- The current player bought in some extra in chips'''
        self._players[self._currentPlayer].extraChips(dollars)

    def newDeck(self,numberOfDecks):
        '''newDeck(int) -> None -- Throws away the old decks and starts over with new decsk'''
        self._deck = Deck(numberOfDecks)
        self._deck.shuffle()

    def hit(self):
        assert(self._deck.cardsLeft() > 0)
        if isinstance(self._hands[self._currentHand].player, Dealer):
            if self._dealer.shouldHit():
                self._dealer.hit(self._deck.pop())
        else:
            self._hands[self._currentHand].hit(self._deck.pop())
        if self._hands[self._currentHand].isBusted():
            print (self._hands[self._currentHand].player.name, "You are busted!")
            self.deleteHand()
        self.handFinish()


    def gameIsOver(self):
        if len(self._hands) <= 1 and self._table:
            self._table.killMatch()

    def deleteHand(self):
        del self._hands[self._currentHand]
        self._currentHand = (self._currentHand if self._currentHand < len(self._hands) else 0)

    def stay(self):
        if Hand.compare(self._hands[self._currentHand], self._dealer.hand()) == 1:
            print(self._players[self._currentPlayer].name + " won!")
        elif Hand.compare(self._players[self._currentPlayer].hand(), self._dealer.hand()) == -1:
            print(self._dealer.name + " has won")
        else:
            print("It is a tie")
        return
        #self._players[self._currentPlayer].updateAfterStay()

    def double(self):
        self._players[self._currentPlayer].updateAfterDouble(self._deck.pop())
        if self._players[self._currentPlayer].hand().isBusted():
            print ("You are busted!")
        if self._players[self._currentPlayer].isSplit():
            pass #HAVE TO FIGURE OUT WHAT TO DO HERE. ALSO NEED TO VERIFY WHAT HAND PLAYER IS AT, FIRST OR SECOND
        else:
            self._currentPlayer+=1

    def split(self):
        self._players[self._currentPlayer].updateAfterSplit()
        # More should be done here. In particular, one must check whether splitting is possible.
        # At this point, an exception is thrown and caught by the except in play(). Maybe don't try split for now.

    def play(self):
        '''This is the flow control method inside match. '''
        print("This is the beginning of the match.")
        while self._currentPlayer<len(self._players):
            print(match)
            print()
            # At this point, must check whether player has blackjack!
            try:
                print ("Your options are: %s" % " ".join([str(Match._PLAY_OPTIONS[key]) for key in Match._PLAY_OPTIONS.keys()]))
                print()
                user_input=str(input("What would you like to do?")).upper()
                assert(user_input in Match._PLAY_OPTIONS.keys())
                self._PLAY_CALLS[user_input]() #Neat way to store and call functions!
            except:
                print("Invalid input! Try again")
                print()
        print("Done with players!")
        print()
        print(match)
        #Now we should do the dealer's part and the results. Off to sleep!

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
        self.assertEqual(dealer.hand(), Hand([C('5','S'),C('J','D'),C('Q','H')]))

if __name__ == "__main__":
    unittest.main()


