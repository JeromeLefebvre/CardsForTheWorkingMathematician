from card import Card

class Hand(object):
    def __init__(self, cards=[], player=None, resplittable=True, isasplit=False):
        if isinstance(cards,Card):
            self.cards = [cards]
        elif isinstance(cards,list) and all(isinstance(card,Card) for card in cards):
            self.cards = cards
        self.resplittable = resplittable
        self.isasplit = isasplit
        self.player = player
        if player != None:
            self.bet=self.player.bet
        else:
            self.bet=0 # For consistency

    def sort(self):
        '''sort() -> None -- Sorts the cards in the hand in place'''
        self.cards = sorted(self.cards, key = lambda x: Card.cardCompare(x,withsuits=True))

    def sorted(self):
        '''sorted() -> Hand -- Returns the cards sorted by rank and suits'''
        return sorted(self.cards, key = lambda x: Card.cardCompare(x,withsuits=True))

    def hit(self, newCard):
        ''' hit(Card) -> None -- add a single card to the current hand '''
        assert(isinstance(newCard,Card))
        self.cards.append(newCard)

    def double(self, newCard):
        ''' double(Card) -> None -- add a single card to the current hand and collect money from player'''
        assert(isinstance(newCard,Card))
        self.cards.append(newCard)
        self.bet*=2
        if self.player != None:
            self.player.betMoney()


    def split(self):
        ''' split() -> hand -- returns a new hand containing half of the pair that is currently in the hand '''
        assert(self.isSplittable())
        self.isasplit=True
        newHand = Hand(self.cards.pop(),self.player,self.resplittable,True)
        if self.player != None:
            self.player.betMoney()
        return newHand

    def isBusted(self):
        ''' isBusted() -> bool -- returns if the hand has a busted hand value '''
        return self.value() == [-1]

    def isBlackJack(self):
        ''' isBlackJack() -> bool -- returns whether the hand is a BlackJack, which means the first two cards add to soft 21'''
        return len(self.cards) == 2 and self.bestValue() == 21 and not(self.isasplit)

    def isSplittable(self):
        ''' isSplittable() -> bool -- returns whether the hand contains of exactly one pair and is on the first hand'''
        if self.player==None:
            return len(self.cards) == 2 and len(set(card.rank for card in self.cards)) == 1 and self.resplittable
        else:
            return len(self.cards) == 2 and len(set(card.rank for card in self.cards)) == 1 and self.resplittable and self.player.canBet(self.bet)

    def isDoublable(self):
        ''' isDoublable() -> bool -- returns whether the hand contains of exactly one pair and is on the first hand'''
        if self.player!=None:
            return self.player.canBet(self.bet)
        else:
            return True

    def value(self):
        ''' value() -> list -- returns a list of one or two possible score for the hand '''
        total = 0
        for card in self.cards:
            total += card.value()
        # if there is one at least one ace, we get two possible values for the score if it won't go over 21
        if any(card.isAce() for card in self.cards) and total <= 11:
            total = [total, total+10]
        elif total<=21:
            total = [total]
        else: #assign total of -1 to busted hands. this will be useful for comparison since busted hands never win
            total=[-1]
        return total

    def bestValue(self):
        ''' bestValue() -> bool -- returns the best value for the hand '''
        return max(self.value())

    @classmethod
    def compare(cls,playerHand,dealerHand):
        ''' compare(hand,hand) -> int -- class method that compares two hands,
        returns 0 if the hands are a tie, -1 if dealer has a stronger hand, 1 if player has a stronger hand'''
        assert(isinstance(playerHand, Hand) and isinstance(dealerHand, Hand))
        if playerHand.bestValue() > dealerHand.bestValue():
            return 1
        elif playerHand.bestValue() < dealerHand.bestValue():
            return -1
        else:
            if playerHand.bestValue() < 21 or (playerHand.isBlackJack() and dealerHand.isBlackJack()):
                return 0
            elif playerHand.isBlackJack() and not dealerHand.isBlackJack():
                return 1
            elif not playerHand.isBlackJack() and dealerHand.isBlackJack():
                return -1

    def __repr__(self):
        return "Hand(cards=%r)" % self.cards

    def __str__(self):
        return ''.join(str(card) + ' ' for card in self.cards).rstrip(' ') # + "Busted\n" if self.isBusted() else "" + "BlackJack\n" if self.isBlackJack() else "" + "Pair\n" if self.isPair() else ""

    def __eq__(self, other):
        # Equality means that the two hands contain the same cards
        if not isinstance(other,Hand):
            return False
        return self.sorted() == other.sorted()

    def __ne__(self,other):
        if not isinstance(other,Hand):
            return True
        return not self == other

    def __gt__(self,other):
        return Hand.compare(self,other) > 0

    def __ge__(self,other):
        return Hand.compare(self,other) >= 0

    def __lt__(self,other):
        return Hand.compare(self,other) < 0

    def __le__(self,other):
        return Hand.compare(self,other) <= 0

import unittest
class TestHand(unittest.TestCase):
    def test_handValue(self):
        playerHand = Hand([Card('K')])
        self.assertEqual(playerHand.value(),[10])
        playerHand.hit(Card('Q'))
        self.assertEqual(playerHand.value(),[20])
        playerHand.hit(Card('A'))
        self.assertEqual(playerHand.value(),[21])
        playerHand.sort()
        self.assertEqual(playerHand.cards,[Card('A'), Card('Q'), Card('K')])

        playerHand = Hand([Card('A'),Card('A')])
        self.assertEqual(playerHand.value(),[2,12])

        playerHand = Hand([Card('K')])
        playerHand.hit(Card('A'))
        self.assertEqual(playerHand.value(),[11,21])
        self.assertTrue(playerHand != 'cat')
        self.assertFalse(playerHand == 'cat')

    def test_basicCompare(self):
        playerHand = Hand([Card('K','H')])
        dealerHand = Hand([Card('K','H')])
        self.assertTrue(playerHand ==  dealerHand)
        playerHand.hit(Card('A'))
        dealerHand = Hand(Card('9'))
        self.assertTrue(playerHand !=  dealerHand)
        self.assertTrue(playerHand >  dealerHand)
        self.assertTrue(playerHand >=  dealerHand)
        self.assertTrue(dealerHand < playerHand)
        self.assertTrue(dealerHand <= playerHand)
        dealerHand = Hand(Card('2'))
        # winning base on the blackjack rule
        self.assertTrue(playerHand.isBlackJack())
        self.assertTrue(playerHand >  dealerHand)

    def test_handStates(self):
        hand = Hand([Card('K'),Card('K')])
        self.assertTrue(hand.isSplittable())
        hand.hit(Card('K'))
        self.assertFalse(hand.isSplittable())
        self.assertTrue(hand.isBusted())
        hand = Hand([Card('A'),Card('J'),Card('K'), Card('A')])
        self.assertTrue(hand.isBusted())

    def test_slit(self):
        hand = Hand([Card('K','H'),Card('K','D')])
        newHand = hand.split()
        self.assertEqual(newHand.cards, [Card('K','D')])
        self.assertEqual(hand.cards, [Card('K','H')])

        hand = Hand([Card('Q','H'),Card('K','D')])
        self.assertRaises(AssertionError, hand.split)

        hand = Hand([Card('J','H'),Card('J','D')])
        newHand = hand.split()
        newHand.hit(Card('A'))
        self.assertFalse(newHand.isBlackJack())

    def test_compare(self):
        playerHand = Hand([Card('K'),Card('K')])
        dealerHand = Hand([Card('9'),Card('J')])
        self.assertEqual( Hand.compare(playerHand,dealerHand), 1)

        playerHand = Hand([Card('K'),Card('K')])
        dealerHand = Hand([Card('A'),Card('K')])
        self.assertEqual( Hand.compare(playerHand,dealerHand), -1)

        playerHand = Hand([Card('9'),Card('K'), Card('2')])
        dealerHand = Hand([Card('A'),Card('K')])
        self.assertEqual( Hand.compare(playerHand,dealerHand), -1)

        playerHand = Hand([Card('2'),Card('4')])
        dealerHand = Hand([Card('3'),Card('3')])
        self.assertEqual( Hand.compare(playerHand,dealerHand), 0)

        playerHand = Hand([Card('Q'),Card('A')])
        dealerHand = Hand([Card('10'),Card('A')])
        self.assertEqual( Hand.compare(playerHand,dealerHand), 0)

        playerHand = Hand([Card('Q'),Card('A')])
        dealerHand = Hand([Card('8'),Card('A'),Card('2')])
        self.assertEqual( Hand.compare(playerHand,dealerHand), 1)

    def test_repr(self):
        playerHand = Hand([Card('Q'),Card('A')])
        self.assertEqual( eval(repr(playerHand)), playerHand)

    def test_print(self):
        playerHand = Hand([Card('Q','S'),Card('A','S')])
        self.assertEqual(str(playerHand), "Q♠ A♠")

if __name__ == "__main__":
    unittest.main()