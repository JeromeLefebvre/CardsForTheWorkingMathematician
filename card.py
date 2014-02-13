
class Card(object):
    ''' The card object is an object that holds a rank and a suit
    the suitd is sorted as:
    clubs = 0, diamonds = 1, hearts = 2, spades = 3
    the ranks are:
    ace = 0, 2 = 1, ... , 10 = 9, Jack = 10, Queen = 11, King = 12
    '''
    # Here are class variables
    SUITS = {3:'Clubs', 2:'Diamonds', 1:'Hearts', 0:'Spades'}
    SUITS_ICON = {3:'♣', 2:'♦',1:'♥',0:'♠'}
    # Since values are unique, it is nice to look them the other way around
    SUITS_REVERSE = {'Spades': 0, 'Clubs': 3, 'Diamonds': 2, 'Hearts': 1, 'S':0, 'C': 3, 'D':2, 'H':1}
    RANKS = {0: 'Ace', 1: '2', 2: '3', 3: '4', 4: '5',5: '6',6: '7', 7: '8', 8: '9', 9:'10', 10:'Jack', 11:'Queen', 12:'King'}
    RANKS_SHORT = {0: 'A', 1: '2', 2: '3', 3: '4', 4: '5',5: '6',6: '7', 7: '8', 8: '9', 9:'10', 10:'J', 11:'Q', 12:'K'}
    RANKS_REVERSE = {'Ace': 0, '10': 9, 'Jack': 10, 'King': 12, '6': 5, '7': 6, '4': 3, '5': 4, '2': 1, '3': 2, 'Queen': 11, '8': 7, '9': 8, 'A':0, 'Q':11, 'J': 10, 'K': 12}

    # The value of each suits
    BLACKJACK_VALUE = {'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'Jack':10,'Queen':10,'King':10,'Ace':1, 'A':1, 'Q':10, 'J': 10, 'K': 10}
    def __init__(self,rank=None,suit=None):
        # if you don't specify a rank, pick one at random
        if rank == None:
            from random import randint
            self.rank = randint(0,12)
        else:
            if isinstance(rank, int):
                # raises an AssertionError if not within the accepted range
                assert( 0 <= rank <= 12)
                self.rank = rank
            elif isinstance(rank, str):
                assert( rank in [ key for key in Card.RANKS_REVERSE ] )
                self.rank = Card.RANKS_REVERSE[rank]
            else:
                # Gave a weird input
                raise ValueError
        if suit == None:
            from random import randint
            self.suit = randint(0,3)
        else:
            if isinstance(suit, int):
                assert( 0 <= suit <= 3) # Not within the valid range
                self.suit = suit
            elif isinstance(suit, str):
                assert( suit in [ key for key in Card.SUITS_REVERSE ] )
                self.suit = Card.SUITS_REVERSE[suit]
            else:
                # Gave a weird input
                raise ValueError

    @classmethod
    def cardCompare(cls, aCard, withsuits = False):
        if withsuits:
            return aCard.rank, aCard.suit
        else:
            return aCard.rank

    def compare(self, other, method, withsuits= False):
        try:
            return method(self.rank, other.rank)
        except AttributeError:
            raise AttributeError("Need to compare against an other card")

    def __eq__(self, other):
        assert(isinstance(other,Card)) # Must compare against a card
        return self.compare(other, lambda x,y: x == y, withsuits=False)

    def __ne__(self, other):
        if not isinstance(other,Card):
            return True
        return self.rank != other.rank or self.suit != other.suit

    def __gt__(self,other):
        if isinstance(other, Card):
            return self.compare(other, lambda x,y: x > y)
        elif isinstance(other, int):
            return self > Card(other)
        else:
            raise TypeError("Need to compare against a int or Card")

    def __ge__(self,other):
        return not (self < other)

    def __lt__(self,other):
        if isinstance(other, Card):
            return self.compare(other, lambda x,y: x < y)
        elif isinstance(other, int):
            return self < Card(other)
        else:
            raise TypeError("Need to compare against a int or Card")

    def __le__(self,other):
        return not (self > other )

    def __str__(self):
        return str(self.RANKS_SHORT[self.rank]) + str(self.SUITS_ICON[self.suit])

    def __repr__(self):
        return "Card(rank=%r,suit=%r)" % (Card.RANKS[self.rank], Card.SUITS[self.suit])

    @classmethod
    def suitsName(cls,suit):
        return Card.SUITS[suit]

    @classmethod
    def ranksName(cls,rank):
        return Card.RANKS[rank]

    def value(self):
        return Card.BLACKJACK_VALUE[Card.ranksName(self.rank)]

    def isAce(self):
        return self.rank== 0

import unittest
class TestHand(unittest.TestCase):
    def test_sort(self):
        Q = Card('Q')
        J = Card('J')
        t = Card('10')
        self.assertEqual( sorted([Q, J, t]) , [t, J, Q])
        one = Card('3', 'H')
        two = Card('4', 'S')
        self.assertEqual( sorted([two,one]), [one,two])
        one = Card(1, 'H')
        two = Card(2, 'S')
        self.assertEqual( sorted([two,one]), [one,two])

        oneH = Card('2', 'H')
        oneS = Card('2', 'S')
        oneC = Card('2', 'C')
        oneD = Card('2', 'D')
        self.assertEqual( sorted( [oneH, oneS], key= lambda x: (x.rank, x.suit) ), [oneS, oneH] )
        self.assertEqual( sorted( [oneH, oneS, oneC, oneD], key= lambda x: Card.cardCompare(x,withsuits=True)), [oneS, oneH, oneD, oneC] )

        K = Card('K')
        A = Card('A')
        self.assertEqual( sorted( [K, A], key= lambda x: Card.cardCompare(x,withsuits=True)), [A,K] )
        def aceWorthElven(x):
            if x.rank == 0:
                return 11
            else:
                return x.rank
        two = Card('2')
        # One compare with Ace = 0, one with Ace = 11
        self.assertEqual( sorted( [A,two], key= lambda x: Card.cardCompare(x,withsuits=True)), [A,two] )
        self.assertEqual( sorted( [A,two], key= lambda x: Card.cardCompare(x,withsuits=False)), [A,two] )
        self.assertEqual( sorted( [A,two], key= aceWorthElven), [two,A] )

    def test_compare(self):
        self.assertTrue( Card('K') > Card('Q'))
        self.assertTrue( Card('K') > Card('J'))
        self.assertTrue( Card('5') < 6)
        self.assertTrue( Card('5') <= 6)
        self.assertFalse( Card('5') >= 6)
        self.assertRaises(TypeError, lambda x: Card('5') < x, 'aa')
        self.assertRaises(TypeError, lambda x: Card('5') > x, 'aa')
        self.assertRaises( TypeError,  lambda x,y: x<= y, (Card('5'),'not a card') )
        self.assertRaises(AttributeError, lambda input: Card('K')._compare(lambda x,y: x < y, input), [])


    def test_equality(self):
        self.assertEqual( Card('K','H') , Card('K','H'))
        self.assertTrue( Card() != 5 )
        self.assertRaises(AssertionError, lambda input: Card() == input, 5)
        self.assertTrue( Card('K','H') != Card('K','S'))

    def test_creation(self):
        # Verify that I can't create a Card made of Junk
        self.assertRaises( ValueError, Card, [])
        self.assertRaises( AssertionError, lambda s: Card(rank='K',suit=s), 'Pink')
        self.assertRaises( AssertionError, lambda s: Card(rank='K',suit=s), 5)
        self.assertEqual( Card(rank='K',suit=3), Card(rank='K',suit='C'))
        self.assertRaises( ValueError, lambda s: Card(rank='K',suit=s), [])

    def test_choice(self):
        # verify random creation
        c = Card()
        self.assertTrue(c.suit in [0,1,2,3])

    def test_classMethod(self):
        self.assertEqual(Card.suitsName(2),'Diamonds')
        self.assertEqual(Card.ranksName(0),'Ace')

    def test_isAce(self):
        self.assertTrue(Card('A').isAce())

    def test_repr(self):
        K = Card('K', 'H')
        self.assertEqual( eval(repr(K)), K)

    def test_print(self):
        K = Card('K', 'H')
        self.assertEqual( str(K), 'K♥')

if __name__ == "__main__":
    unittest.main()
