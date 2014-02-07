
from deck import Deck
from player import NormalPlayer,Dealer

class Match(object):
	def __init__(self):
		self.deck = Deck(8)
		self.players = [NormalPlayer(),Dealer()]
		for i in range(0,2):
			for player in self.players()
				player.dealCard(self.Deck.pop())
		self.currentPlayer = 0
