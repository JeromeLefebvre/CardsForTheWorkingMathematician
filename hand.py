from card import Card

class Hand(object):
    def __init__(self,cards=[]):
        if isinstance(cards,Card):
            self._cards = [cards]
        elif isinstance(cards,list):
            self._cards = cards

    def receive(self,newCard):
        ''' receive(Card) -> None -- add a single card to the current hand '''
        assert(isinstance(newCard,Card))
        self._cards.append(newCard)

    def displayCards(self):
        ''' Prints the content of the hand '''
        for card in self._cards:
            print(card)

    def isBusted(self):
        ''' isBusted() -> bool -- returns if the hand has a busted hand value '''
        return sum(self.value()) == -1

    def isBlackJack(self):
        ''' isBlackJack() -> bool -- returns whether the hand is a BlackJack '''
        return len(self._cards) == 2 and max(self.value())==21

    def isPair(self):
        ''' isPair() -> bool -- returns whether the hand contains of exactly one pair '''
        return len(self._cards) == 2 and len(set(card.rank() for card in self._cards)) == 1

    def value(self):
        ''' value() -> list -- returns a list of one or two possible score for the hand '''
        total = 0
        for card in self._cards:
            total += card.blackjackValue()
        # if there is one at least one ace, we get two possible values for the score if it won't go over 21
        if any(card.isAce() for card in self._cards) and total <= 11:
            total = [total, total+10]
        elif total<=21:
            total = [total]
        else: #assign total of -1 to busted hands. this will be useful for comparison since busted hands never win
            total=[-1]
        return total

    def bestValue(self):
        ''' bestValue() -> bool -- returns the best value for the hand '''
        return max(self.value())

    def split(self):
        ''' split() -> hand -- returns a new hand containing half of the pair that is currently in the hand '''
        assert(self.isPair())
        newHand = Hand(self._cards.pop())
        return newHand

    @classmethod
    def compare(cls,playerHand,dealerHand):
        ''' compare(hand,hand) -> int -- class method that compares two hands, 
        returns 0 if the hands are a tie, -1 if dealer has a stronger hand, 1 if player has a stronger hand'''
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
        return "Hand(cards=%r)" % self._cards

    def __str__(self):
        return "%s" % [str(card) for card in self._cards]

    def _compare(self, other, method):
        ''' _compare(Hand, function) -> bool -- compares two hands of blackjack'''
        try:
            maxself = max(self.value())
            maxother = max(other.value())
            # if we have a blackjack: ace + king/queen/jack/10 is counted as 22
            if len(self._cards) == 2 and maxself == 21:
                maxself = 22
            if len(other._cards) == 2 and maxother == 21:
                maxother = 22
            return method(maxself, maxother)
        except AttributeError:
            pass

    def __eq__(self, other):
        # Must compare against a Hand
        if not isinstance(other,Hand):
            return False
        # We use withsuits since we want actual equality
        return self._compare(other, lambda x,y: x == y)

    def __ne__(self,other):
        if not isinstance(other,Hand):
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
        playerHand = Hand([Card('K')])
        self.assertEqual(playerHand.value(),[10])
        playerHand.receive(Card('Q'))
        self.assertEqual(playerHand.value(),[20])
        playerHand.receive(Card('A'))
        self.assertEqual(playerHand.value(),[21])

        playerHand = Hand([Card('A'),Card('A')])
        self.assertEqual(playerHand.value(),[2,12])
        
        playerHand = Hand([Card('K')])
        playerHand.receive(Card('A'))
        self.assertEqual(playerHand.value(),[11,21])

    def test_compare(self):
        playerHand = Hand([Card('K')])
        dealerHand = Hand([Card('K')])
        self.assertTrue(playerHand ==  dealerHand)
        playerHand.receive(Card('A'))
        dealerHand = Hand(Card('9'))
        self.assertTrue(playerHand >  dealerHand)
        dealerHand = Hand(Card('2'))
        # winning base on the blackjack rule
        self.assertTrue(playerHand.isBlackJack())
        self.assertTrue(playerHand >  dealerHand)

        playerHand = Hand([Card('K')])
        dealerHand = Hand([Card('Q')])
        self.assertTrue(playerHand ==  dealerHand)

    def test_handStates(self):
        hand = Hand([Card('K'),Card('K')])
        self.assertTrue(hand.isPair())
        hand.receive(Card('K'))
        self.assertFalse(hand.isPair())
        self.assertTrue(hand.isBusted())

    def test_slit(self):
        hand = Hand([Card('K','H'),Card('K','D')])
        newHand = hand.split()
        self.assertEqual(newHand._cards, [Card('K','D')])
        self.assertEqual(hand._cards, [Card('K','H')])

        hand = Hand([Card('Q','H'),Card('K','D')])
        self.assertRaises(AssertionError, hand.split)

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

    def test_repr(self):
        playerHand = Hand([Card('Q'),Card('A')])
        self.assertEqual( eval(repr(playerHand)), playerHand)

if __name__ == "__main__":
    unittest.main()