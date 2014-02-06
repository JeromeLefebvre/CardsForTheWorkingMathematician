
from card import card

class hand():
	def __init__(self,cards=[]):
		self._cards = cards

	def receive(self,card):
		self._cards.append(card)

	def value(self):
		total = 0
		for card in self._cards:
			total += card.blackjackValue()
		# if there is one atleast one ace, we get two possible values for the score if it won't go over 21
		if any(card.isAce() for card in self._cards) and total <= 11:
			total = [total, total+10]
		return total


import unittest
class TestHand(unittest.TestCase):
	def setup(self):
		pass

	def test_handValue(self):
		self.playerhand = hand([card('K')])
		self.assertEqual(self.playerhand.value(),10)
		self.playerhand.receive(card('Q'))
		self.assertEqual(self.playerhand.value(),20)
		self.playerhand.receive(card('A'))
		self.assertEqual(self.playerhand.value(),21)
		self.playerhand = hand([card('A'),card('A')])
		self.assertEqual(self.playerhand.value(),[2,12])

if __name__ == "__main__":
	unittest.main()