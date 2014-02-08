from deck import Deck
from player import NormalPlayer,Dealer

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
        self.startRound()

    def setBet(self):
        # Need to think of how match handles bet
        pass

    def startRound(self):
        for player in self._players:
            cardsToPass = [self._deck.pop(), self._deck.pop()]
            #print("**", cardsToPass, "to player ", player.name)
            player.startMatch(cardsToPass)
        self._dealer.startMatch([self._deck.pop(), self._deck.pop()])

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
        self._players[self._currentPlayer].hit(self._deck.pop())
        if self._players[self._currentPlayer].hand().isBusted():
            print ("You are busted!")
            self._currentPlayer = (self._currentPlayer + 1 if self._currentPlayer + 1 < len(self._players) else 0)

    def stay(self):
        self._players[self._currentPlayer].updateAfterStay()
        if self._players[self._currentPlayer].isSplit():
            pass #HAVE TO FIGURE OUT WHAT TO DO HERE. ALSO NEED TO VERIFY WHAT HAND PLAYER IS AT, FIRST OR SECOND
        else:
            self._currentPlayer+=1

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


if __name__ == "__main__":
    match = Match()
    match.play()


