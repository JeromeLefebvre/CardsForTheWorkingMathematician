
from card import card

class hand():
	def __init__(self,cards=[]):
		if isinstance(cards,card):
			self._cards = [cards]
		elif isinstance(cards,list):
			self._cards = cards

	def receive(self,newcard):
		assert(isinstance(newcard,card))
		self._cards.append(newcard)

	def value(self):
		total = 0
		for card in self._cards:
			total += card.blackjackValue()
		# if there is one atleast one ace, we get two possible values for the score if it won't go over 21
		if any(card.isAce() for card in self._cards) and total <= 11:
			total = [total, total+10]
		else:
			total = [total]
		return total

	def _compare(self,other,method):
		pass

	def _compare(self, other, method, withsuits= False):
		try:
			maxself = max(self.value())
			maxother = max(other.value())
			# if we have a blackjack: ace + king/queen/jack/10 is counted as 22
			if len(self._cards) == 2 and maxself == 21:
				maxself = 22
			if len(other._cards) == 2 and maxother == 21:
				maxself = 22				
			return method(maxself, maxother)
		except AttributeError:
			pass

	def __eq__(self, other):
		# Must compare against a card
		if not isinstance(other,hand):
			return False
		# We use withsuits since we want actual equality
		return self._compare(other, lambda x,y: x == y)

	def __ne__(self,other):
		if not isinstance(other,hand):
			return True
		return self._compare(other, lambda x,y: x != y)

	def __gt__(self,other):
		return self._compare(other, lambda x,y: x > y)

	def __ge__(self,other):
		return self._compare(other, lambda x,y: x >= y)

	def __lt__(self,other):
		return self._compare(other, lambda x,y: x < y)

	def __le__(self,other):
		return self._compare(other, lambda x,y: x <= y)

import unittest
class TestHand(unittest.TestCase):
	def setup(self):
		pass

	def test_handValue(self):
		self.playerhand = hand([card('K')])
		self.assertEqual(self.playerhand.value(),[10])
		self.playerhand.receive(card('Q'))
		self.assertEqual(self.playerhand.value(),[20])
		self.playerhand.receive(card('A'))
		self.assertEqual(self.playerhand.value(),[21])
		self.playerhand = hand([card('A'),card('A')])
		self.assertEqual(self.playerhand.value(),[2,12])
		self.playerhand = hand([card('K')])
		self.playerhand.receive(card('A'))
		self.assertEqual(self.playerhand.value(),[11,21])
	def test_compare(self):
		self.playerhand = hand([card('K')])
		self.dealerhand = hand([card('K')])
		self.assertTrue(self.playerhand ==  self.dealerhand)
		self.playerhand.receive(card('A'))
		self.dealerhand = hand(card('9'))
		self.assertTrue(self.playerhand >  self.dealerhand)
		self.dealerhand = hand(card('2'))
		# winning base on the blackjack rule
		self.assertTrue(self.playerhand >  self.dealerhand)
		
		self.playerhand = hand([card('K')])
		self.dealerhand = hand([card('Q')])
		self.assertTrue(self.playerhand ==  self.dealerhand)
		self.playerhand = hand(card('K'))
		self.dealerhand = hand(card('K'))
		self.assertTrue(self.playerhand ==  self.dealerhand)		

if __name__ == "__main__":
	unittest.main()