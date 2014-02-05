class card(object):
	''' The card object (this is crazy) is an object that holds a rank and a suite
	the suited is sorted as:
	clubs = 0, diamonds = 1, hearts = 2, spades = 3
	the ranks are:
	ace = 0, 1 = 1, 2 = 2, ... , 10 = 10, Jack = 11, Queen = 12, King = 13
	'''
	# Here are class variables
	_suites = {0:'Clubs', 1:'Diamonds', 2:'Hearts',3:'Spades'}
	# Since values are unique, it is nice to look them the other way around
	_suites_reverse = {'Spades': 3, 'Clubs': 0, 'Diamonds': 1, 'Hearts': 2, 'S':3, 'C': 0, 'D':1, 'H':2}
	_ranks = {0: 'Ace', 1: '2', 2: '3', 3: '4', 4: '5',5: '6',6: '7', 7: '8', 8: '9', 9:'10', 10:'Jack', 11:'Queen', 12:'King'}
	_ranks_reverse = {'Ace': 0, '10': 9, 'Jack': 10, 'King': 12, '6': 5, '7': 6, '4': 3, '5': 4, '2': 1, '3': 2, 'Queen': 11, '8': 7, '9': 8, 'A':0, 'Q':11, 'J': 10, 'K': 12}

	def __init__(self,rank=None,suite=None):
		# if you don't specify a rank, pick one at random
		if rank == None:
			from random import randint
			self._rank = randint(0,13)
		else:
			if isinstance(rank, int):
				# raises an AssertionError if not within the accepted range
				assert( 0 <= rank <= 13)
				self._rank = rank
			elif isinstance(rank, str):
				assert( rank in [ key for key in card._ranks_reverse ] )
				self._rank = card._ranks_reverse[rank]
			else:
				# Gave a weird input
				raise ValueError
		if suite == None:
			from random import randint
			self._suite = randint(0,3)
		else:
			if isinstance(suite, int):
				# raises an AssertionError if not within the accepted range
				assert( 0 <= suite <= 3)
				self._suite = suite
			elif isinstance(suite, str):
				assert( suite in [ key for key in card._suites_reverse ] )
				self._suite = card._suites_reverse[suite]
			else:
				# Gave a weird input
				raise ValueError

	def rank(self):
		'''A getter for the rank of the card '''
		return self._rank

	def suite(self):
		'''A getter for the suite of the card '''
		return self._suite

	@classmethod
	def cardCompare(cls, aCard, withSuites = False):
		if withSuites:
			return aCard.rank(), aCard.suite()
		else:
			return aCard.rank()

	def _compare(self, other, method, withSuites= False):
		try:
			if withSuites:
				return method(self.rank(), other.rank()) and method(self.suite(), other.suite())
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
		return self._compare(other, lambda x,y: x == y)

	def __ne__(self,other):
		if not isinstance(other,card):
			return True
		return self._compare(other, lambda x,y: x != y)

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
		return str(self._ranks[self._rank]) + " of " + str(self._suites[self._suite])

	def __repr__(self):
		'''>>> card('Q')
Queen of Spades
		'''
		return str(self._ranks[self._rank]) + " of " + str(self._suites[self._suite])

	@classmethod
	def suites_name(cls,suite):
		return card._suites[suite]

	@classmethod
	def ranks_name(cls,rank):
		return card._ranks[rank]

import unittest
class TestHand(unittest.TestCase):
	def setup(self):
		pass

	def test_sort(self):
		self.assertEqual( sorted([card('Q'), card('J'), card('10')]) , [card('10'), card('J'), card('Q')])
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
		self.assertEqual( sorted( [oneH, oneS], key= lambda x: (x.rank(), x.suite()) ), [oneS, oneH] )
		self.assertEqual( sorted( [oneH, oneS, oneC, oneD], key= lambda x: card.cardCompare(x,withSuites=True)), [oneC, oneD, oneH, oneS] )

		K = card('K')
		A = card('A')
		self.assertEqual( sorted( [K, A], key= lambda x: card.cardCompare(x,withSuites=True)), [A,K] )
		def aceWorthElven(x):
			if x.rank() == 0:
				return 11
			else:
				return x.rank()
		two = card('2')
		self.assertEqual( sorted( [A,two], key= aceWorthElven), [two,A] )
	def test_compare(self):
		self.assertTrue( card('K') > card('Q'))
		self.assertTrue( card('K') > card('J'))
		self.assertTrue( card('5') < 6)
		self.assertTrue( card('5') <= 6)
		self.assertFalse( card('5') >= 6)

	def test_equality(self):
		self.assertEqual( card('K') , card('K'))
		self.assertFalse( card('K') == 5 )
		self.assertTrue( card() != 5 )
		self.assertEqual( card('Q'), card('Q'))

	def test_creation(self):
		# Verify that I can't create a card made of Junk
		self.assertRaises( ValueError, card, [])

	def test_choice(self):
		# verify random creation
		c = card()
		self.assertTrue(c.suite() in [0,1,2,3])

	def test_classMethod(self):
		self.assertEqual(card.suites_name(2),'Hearts')
	
if __name__ == "__main__":
	unittest.main()
