import cmd
from deck import Deck
from hand import Hand
from player import Player
from match import Match

'''TODO:
1. Set up a series of different tables

'''
class BlackJackTable(cmd.Cmd):
    minbet = 3
    maxbet = 10
    intro = 'Welcome to the blackjack table. Type help or ? to list commands.\n The minimum bet is %s dollars, the maximum bet is %s dollars\n' % (minbet, maxbet)
    prompt = '(input) '
    file = None

    # Instructions
    def do_start(self, arg):
        'Starts a game'
        self.match = Match(table=self)
        self.do_display(None)

    def feedback(self, question):
        return input(question)
        
    def do_hitme(self,arg):
        'Hit me'
        self.match.hit()
        self.do_display(None)

    def do_bet(self,arg):
        'Bet an amount of money'
        print("You've bet", *parse(arg))

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
        print(self.match)

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