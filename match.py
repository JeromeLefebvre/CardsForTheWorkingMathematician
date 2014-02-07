from deck import Deck
from player import NormalPlayer,Dealer

class Match(object):
    def __init__(self,table,deck=None,players=None,dealer=None):
        if isinstance(deck,Deck):
            self._deck=deck
        else:
            self._deck = Deck(8)
            self._deck.shuffle()
        if isinstance(players,list) and all(isinstance(player,NormalPlayer) for player in players):
            self._players = players
        else:
            self._players = [NormalPlayer()]
        # If more than one player for one sitting ask the name of each player
        if len(self._players) > 1:
            for index, player in enumerate(self._players):
                name = table.feedback("Enter the name of player 1: ")


        if isinstance(dealer,Dealer):
            self._dealer = dealer
        else:
            self._dealer = Dealer()
        self._dealer = Dealer()

        self._currentPlayer = 0

    def setBet(self):
        # Need to think of how match handles bet
        pass

    def startRound(self):
        for player in self._players:
        	player.startMatch([self._deck.pop(), self._deck.pop()])
        self._dealer.startMatch([self._deck.pop(), self._deck.pop()])

    def __str__(self):
        return "Players %s, Dealer %s" % ([str(player) for player in self._players], self._dealer)

    def playerBuysIn(self,dollars):
        ''' playerBuysIn(dollars) -> None -- The current player bought in some extra in chips'''
        self._players[self._currentPlayer].extraChips(dollars)

    def newDeck(self,numberOfDecks):
        '''newDeck(int) -> None -- Throws away the old decks and starts over with new decsk'''
        self._deck = Deck(numberOfDecks)
        self._deck.shuffle()

    def hit(self):
        assert(self._deck.cardsLeft() > 0)
        self._players[self._currentPlayer].updateAfterHit(self._deck.pop())

    def stay(self):
        self._players[self._currentPlayer].updateAfterStay()
        if self._players[self._currentPlayer].isSplit():
            pass #HAVE TO FIGURE OUT WHAT TO DO HERE. ALSO NEED TO VERIFY WHAT HAND PLAYER IS AT, FIRST OR SECOND
        else:
            self._currentPlayer+=1

    def double(self):
        self._players[self._currentPlayer].updateAfterDouble(self._deck.pop())
        if self._players[self._currentPlayer].isSplit():
            pass #HAVE TO FIGURE OUT WHAT TO DO HERE. ALSO NEED TO VERIFY WHAT HAND PLAYER IS AT, FIRST OR SECOND
        else:
            self._currentPlayer+=1

    def split(self):
        self._players[self._currentPlayer].updateAfterSplit()

if __name__ == "__main__":
    match = Match()
    print (match)

