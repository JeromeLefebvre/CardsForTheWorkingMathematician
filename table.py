import cmd
from deck import Deck
from hand import Hand
from player import NormalPlayer, Dealer
from match import Match

class BlackJackTable(cmd.Cmd):
    Rules = {"standOn17":True, "softOn17":False, #Only one can be true
             "3to2": True, "6to5":False, #Only one can be true
             "EarlySurrender": True, "LatSurrender": False #At most 1 can be true
             }
    minbet = 3
    maxbet = 10
    intro = "Hello John, I'm your dealer Malkovich. I see you have a few dollars, would you like to play some blackjack? \nThe minimum bet is %s dollars, the maximum bet is %s dollars\nType help or ? to list commands.\n " % (minbet, maxbet)
    prompt = '(input) '
    file = None

    def preloop(self):
        self.inMatch = False
        self.player = NormalPlayer(name="John", money=20)
        self.dealer = Dealer(name="Malkovich",standOn17=BlackJackTable.Rules["standOn17"],soft17=BlackJackTable.Rules["softOn17"])
    # Instructions 
    def do_start(self, arg):
        'Starts a game'
        self.inMatch = True
        self.match = Match(players=[self.player], table=self, dealer=self.dealer)
        self.do_display(None)
        
    def feedback(self, question):
        return input(question)

    def do_hitme(self,arg):
        'Hit me'
        self.match.hit()
        self.do_display(None)

    def do_bet(self,arg):
        'Bet an amount of money'

    def do_stay(self,arg):
        'Current player stays'
        self.match.stay()

    def collectBets(self,name):
        "Collects the amount each player wants to bet"
        while True:
            bet = input(name + " what is your bet? ")
            try:
                bet = int(bet)
                if BlackJackTable.minbet <= bet <= BlackJackTable.maxbet:
                    if not self.player.canBet(bet):
                        print("You can't make that bet, but there is an ATM down the corner")
                    else:
                        return bet
                else:
                    print("A bet needs to be between " + str(BlackJackTable.minbet) + " and " + str(BlackJackTable.maxbet))
            except (TypeError, ValueError):
                print("Please type in a number")

    def do_changeName(self,arg):
        self.player.name = parseString(arg)
        print("I'm sorry, hello there %s " % self.player.name)

    def do_buyIn(self,arg):
        "Buy a certain amount of chips"
        self.match.playerBuysIn(*parse(arg))

    def do_deck(self,arg):
        "Fix the number of decks be used: deck 6"
        self.math.newDecks(*parse(arg))

    def do_changeDefault(self,arg):
        "Change the default amount for a bet: changeDefault 3 10"
        if parse(arg)[0] >= parse(arg)[1]:
            print("Ensure that minimum is lower than the maximum")
        else:
            (BlackJackTable.minbet, BlackJackTable.maxbet) = parse(arg)

    def do_rules(self,arg):
        "Print the current rules"
        print("The minimum bet is " + str(BlackJackTable.minbet) + " and maximum is " + str(BlackJackTable.maxbet))

    def do_display(self,arg):
        'Display your hand'
        print(self.player.name + " has " + str(self.player.money()) + "$")
        if self.inMatch:
            print(self.player.hand())
            print("########################")
            print(self.dealer.hand())

    def do_quit(self,arg):
        'Quit the game'
        print("Thanks for visiting.")
        return True

def parse(arg):
    return tuple(map(int, arg.split()))

def parseString(arg):
    return tuple(map(str, arg.split()))
if __name__ == '__main__':
    BlackJackTable().cmdloop()