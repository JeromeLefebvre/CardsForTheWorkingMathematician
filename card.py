
class card(object):
	''' The card object is an object that holds a rank and a suit
	the suitd is sorted as:
	clubs = 0, diamonds = 1, hearts = 2, spades = 3
	the ranks are:
	ace = 0, 2 = 1, ... , 10 = 9, Jack = 10, Queen = 11, King = 12
	'''
	# Here are class variables
	_suits = {3:'Clubs', 2:'Diamonds', 1:'Hearts', 0:'Spades'}
	# Since values are unique, it is nice to look them the other way around
	_suitsReverse = {'Spades': 0, 'Clubs': 3, 'Diamonds': 2, 'Hearts': 1, 'S':0, 'C': 3, 'D':2, 'H':1}
	_ranks = {0: 'Ace', 1: '2', 2: '3', 3: '4', 4: '5',5: '6',6: '7', 7: '8', 8: '9', 9:'10', 10:'Jack', 11:'Queen', 12:'King'}
	_ranksReverse = {'Ace': 0, '10': 9, 'Jack': 10, 'King': 12, '6': 5, '7': 6, '4': 3, '5': 4, '2': 1, '3': 2, 'Queen': 11, '8': 7, '9': 8, 'A':0, 'Q':11, 'J': 10, 'K': 12}
	# The value of each suits
	_blackjackValue = {'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'Jacks':10,'Queen':10,'King':10,'Ace':1}
	def __init__(self,rank=None,suit=None):
		# if you don't specify a rank, pick one at random
		if rank == None:
			from random import randint
			self._rank = randint(0,12)
		else:
			if isinstance(rank, int):
				# raises an AssertionError if not within the accepted range
				assert( 0 <= rank <= 12)
				self._rank = rank
			elif isinstance(rank, str):
				assert( rank in [ key for key in card._ranksReverse ] )
				self._rank = card._ranksReverse[rank]
			else:
				# Gave a weird input
				raise ValueError
		if suit == None:
			from random import randint
			self._suit = randint(0,3)
		else:
			if isinstance(suit, int):
				# raises an AssertionError if not within the accepted range
				assert( 0 <= suit <= 3)
				self._suit = suit
			elif isinstance(suit, str):
				assert( suit in [ key for key in card._suitsReverse ] )
				self._suit = card._suitsReverse[suit]
			else:
				# Gave a weird input
				raise ValueError

	def rank(self):
		'''A getter for the rank of the card '''
		return self._rank

	def suit(self):
		'''A getter for the suit of the card '''
		return self._suit

	@classmethod
	def cardCompare(cls, aCard, withsuits = False):
		if withsuits:
			return aCard.rank(), aCard.suit()
		else:
			return aCard.rank()

	def _compare(self, other, method, withsuits= False):
		try:
			if withsuits:
				return method(self.rank(), other.rank()) and method(self.suit(), other.suit())
			else:
				return method(self.rank(), other.rank())
		except AttributeError:
			pass
		# We can't compare those two objects
		# Can't figure out how to output the same thing as python:
		# >>> 5 < []
		# Traceback (most recent call last):
  		#	File "<stdin>", line 1, in <module>
		# TypeError: unorderable types: int() < list()
		# So I have this custom message
		raise TypeError("unorderable types:" + str(type(other)) + " " + str(type(self)))
			
	def __eq__(self, other):
		# Must compare against a card
		if not isinstance(other,card):
			return False
		# We use withsuits since we want actual equality
		return self._compare(other, lambda x,y: x == y, withsuits=True)

	def __ne__(self,other):
		if not isinstance(other,card):
			return True
		# != is more complicated, since we want to return True if either the rank or the suit differs
		withsuits=True
		method = lambda x,y: x != y
		if withsuits:
			return method(self.rank(), other.rank()) or method(self.suit(), other.suit())
		else:
			return method(self.rank(), other.rank())		
		return method(self.rank(), other.rank())

	def __gt__(self,other):
		if isinstance(other, card):
			return self._compare(other, lambda x,y: x > y)
		elif isinstance(other, int):
			return self > card(other)

	def __ge__(self,other):
		if isinstance(other, card):
			return self._compare(other, lambda x,y: x >= y)
		elif isinstance(other, int):
			return self >= card(other)

	def __lt__(self,other):
		if isinstance(other, card):
			return self._compare(other, lambda x,y: x < y)
		elif isinstance(other, int):
			return self < card(other)

	def __le__(self,other):
		if isinstance(other, card):
			return self._compare(other, lambda x,y: x <= y)
		elif isinstance(other, int):
			return self <= card(other)

	def __str__(self):
		''' Used with the print function
		>>> print(card('Q'))
Queen of Hearts
		'''
		return str(self._ranks[self._rank]) + " of " + str(self._suits[self._suit])

	def __repr__(self):
		'''>>> card('Q')
Queen of Spades
		'''
		return str(self._ranks[self._rank]) + " of " + str(self._suits[self._suit])

	@classmethod
	def suits_name(cls,suit):
		return card._suits[suit]

	@classmethod
	def ranks_name(cls,rank):
		return card._ranks[rank]

	def blackjackValue(self,aceWorthElven=False):
		if aceWorthElven and self.rank() == card._ranksReverse[("Ace")]:
			return 11
		return card._blackjackValue[ card._ranks[self.rank()]]

	def isAce(self):
		return self._rank == 0

import unittest
class TestHand(unittest.TestCase):
	def setup(self):
		pass

	def test_sort(self):
		Q = card('Q')
		J = card('J')
		t = card('10')
		self.assertEqual( sorted([Q, J, t]) , [t, J, Q])
		one = card('3', 'H')
		two = card('4', 'S')
		self.assertEqual( sorted([two,one]), [one,two])
		one = card(1, 'H')
		two = card(2, 'S')
		self.assertEqual( sorted([two,one]), [one,two])		
		
		oneH = card('2', 'H')
		oneS = card('2', 'S')
		oneC = card('2', 'C')
		oneD = card('2', 'D')
		self.assertEqual( sorted( [oneH, oneS], key= lambda x: (x.rank(), x.suit()) ), [oneS, oneH] )
		self.assertEqual( sorted( [oneH, oneS, oneC, oneD], key= lambda x: card.cardCompare(x,withsuits=True)), [oneS, oneH, oneD, oneC] )

		K = card('K')
		A = card('A')
		self.assertEqual( sorted( [K, A], key= lambda x: card.cardCompare(x,withsuits=True)), [A,K] )
		def aceWorthElven(x):
			if x.rank() == 0:
				return 11
			else:
				return x.rank()
		two = card('2')
		# One compare with Ace = 0, one with Ace = 11
		self.assertEqual( sorted( [A,two], key= lambda x: card.cardCompare(x,withsuits=True)), [A,two] )
		self.assertEqual( sorted( [A,two], key= aceWorthElven), [two,A] )

	def test_compare(self):
		self.assertTrue( card('K') > card('Q'))
		self.assertTrue( card('K') > card('J'))
		self.assertTrue( card('5') < 6)
		self.assertTrue( card('5') <= 6)
		self.assertFalse( card('5') >= 6)

	def test_equality(self):
		self.assertEqual( card('K','H') , card('K','H'))
		self.assertTrue( card() != 5 )
		self.assertTrue( card('K','H') != card('K','S'))

	def test_creation(self):
		# Verify that I can't create a card made of Junk
		self.assertRaises( ValueError, card, [])

	def test_choice(self):
		# verify random creation
		c = card()
		self.assertTrue(c.suit() in [0,1,2,3])

	def test_classMethod(self):
		self.assertEqual(card.suits_name(2),'Diamonds')

	def test_blackjack(self):
		self.assertEqual( card('Q').blackjackValue(), 10)
		self.assertEqual( card('A').blackjackValue(), 1)
		self.assertEqual( card('A').blackjackValue(True), 11)

if __name__ == "__main__":
	unittest.main()
