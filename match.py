from deck import Deck
from player import NormalPlayer,Dealer

class Match(object):
    _PLAY_OPTIONS = {'H':"(H)it",'D':"(D)ouble",'S':"(S)tay",'P':"s(P)lit"}

    def __init__(self,deck=None,players=None,dealer=None):
        if isinstance(deck,Deck):
            self._deck=deck
        else:
            self._deck = Deck(8)
            self._deck.shuffle()
        if isinstance(players,list) and all(isinstance(player,NormalPlayer) for player in players):
            self._players = players
        else:
            self._players = [NormalPlayer()]
        if isinstance(dealer,Dealer):
            self._dealer = dealer
        else:
            self._dealer = Dealer()
        self._dealer = Dealer()

        self._currentPlayer = 0
        for player in self._players:
        	player.startMatch([self._deck.pop(), self._deck.pop()])
        self._dealer.startMatch([self._deck.pop(), self._deck.pop()])

        self._PLAY_CALLS = {'H':self.hit,'D':self.double,'S':self.stay,'P':self.split} #Whoa! A dictionary that we'll use to call functions!

    def __str__(self):
        return "Players %s, Dealer %s" % ([str(player) for player in self._players], self._dealer)

    def hit(self):
        assert(self._deck.cardsLeft() > 0)
        self._players[self._currentPlayer].updateAfterHit(self._deck.pop())
        if self._players[self._currentPlayer].hand().isBusted():
            print ("You are busted!")
            self._currentPlayer+=1

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
        # More should be done here. Maybe don't try split for now.

    def play(self):
        '''This is the flow control method inside match. '''
        print("This is the beginning of the match.")
        while self._currentPlayer<len(self._players):
            print(match)
            print()
            print ("Your options are: %s" % " ".join([str(Match._PLAY_OPTIONS[key]) for key in Match._PLAY_OPTIONS.keys()]))
            print()
            try:
                user_input=str(input("What would you like to do?")).upper()
                assert(user_input in Match._PLAY_OPTIONS.keys())
                self._PLAY_CALLS[user_input]() #Neat way to store and call functions!
            except:
                print("Invalid input! Try again")
                print()

        print("Done with players!") #Now we should do the dealer's part
        print()
        print(match)


if __name__ == "__main__":
    match = Match()
    match.play()


