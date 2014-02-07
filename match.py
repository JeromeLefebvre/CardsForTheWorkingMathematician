from deck import Deck
from player import NormalPlayer,Dealer

class Match(object):
	def __init__(self):
		self.deck = Deck(8)
		self.deck.shuffle()
		self.dealer = Dealer()
		self.players = [NormalPlayer()]
		self.currentPlayer = 0
		
		self.dealer.startMatch([self.Deck.pop(), self.Deck.pop()])
		for player in self.players()
			player.startMatch([self.Deck.pop(), self.Deck.pop()])

	def __str__(self):
		return "Players %s, Dealer" % [str(player) for player in self.Players], str(self.dealer)

	def hit(self):
		assert(self.deck.cardsLeft() > 0)
		self.players[self.currentPlayer].updateAfterHit(self.Deck.pop())

if __name__ == "__main__":
	match = Match()
		
