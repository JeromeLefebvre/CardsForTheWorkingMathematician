import cmd
from deck import Deck
from hand import Hand

class BlackJackTable(cmd.Cmd):
    intro = 'Welcome to the blackjack table. Type help or ? to list commands.\n'
    prompt = '(table) '
    file = None

    # Instructions
    def do_start(self, arg):
        'Starts a game'
        self.deck = Deck(1)
        self.hand = Hand()

    def do_hitme(self,arg):
        'Hit me'
        self.hand.receive(self.deck.pop())

    def do_display(self,arg):
        'Display your hand'
        print(self.hand)

    def do_quit(self,arg):
        'Quit the game'
        print("Thanks for visiting.")
        return True

if __name__ == '__main__':
    BlackJackTable().cmdloop()        