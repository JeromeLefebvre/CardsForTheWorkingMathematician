from card import Card

class Hand():
    def __init__(self,cards=[]):
        if isinstance(cards,Card):
            self._cards = [cards]
        elif isinstance(cards,list):
            self._cards = cards

    def receive(self,newCard):
        ''' receive(Card) -> None -- add a single card to the current hand '''
        assert(isinstance(newCard,Card))
        self._cards.append(newCard)

    def isBusted(self):
        ''' isBusted() -> bool -- returns if the hand is under 21 points for a choice value of aces '''
        return min(self.value()) <= 21

    def isBlackJack(self):
        '''isBlackJack() -> bool -- returns whether the hand is a BlackJack '''
        return (len(self._cards) == 2 and max(self.value())==21)

    def value(self):
        ''' value() -> list -- returns a list of one or two possible score for the hand '''
        total = 0
        for card in self._cards:
            total += card.blackjackValue()
        # if there is one at least one ace, we get two possible values for the score if it won't go over 21
        if any(card.isAce() for card in self._cards) and total <= 11:
            total = [total, total+10]
        else:
            total = [total]
        return total

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
        self.playerhand = Hand([Card('K')])
        self.assertEqual(self.playerhand.value(),[10])
        self.playerhand.receive(Card('Q'))
        self.assertEqual(self.playerhand.value(),[20])
        self.playerhand.receive(Card('A'))
        self.assertEqual(self.playerhand.value(),[21])
        self.playerhand = Hand([Card('A'),Card('A')])
        self.assertEqual(self.playerhand.value(),[2,12])
        self.playerhand = Hand([Card('K')])
        self.playerhand.receive(Card('A'))
        self.assertEqual(self.playerhand.value(),[11,21])
    def test_compare(self):
        self.playerhand = Hand([Card('K')])
        self.dealerhand = Hand([Card('K')])
        self.assertTrue(self.playerhand ==  self.dealerhand)
        self.playerhand.receive(Card('A'))
        self.dealerhand = Hand(Card('9'))
        self.assertTrue(self.playerhand >  self.dealerhand)
        self.dealerhand = Hand(Card('2'))
        # winning base on the blackjack rule
        self.assertTrue(self.playerhand >  self.dealerhand)

        self.playerhand = Hand([Card('K')])
        self.dealerhand = Hand([Card('Q')])
        self.assertTrue(self.playerhand ==  self.dealerhand)
        self.playerhand = Hand(Card('K'))
        self.dealerhand = Hand(Card('K'))
        self.assertTrue(self.playerhand ==  self.dealerhand)

if __name__ == "__main__":
    unittest.main()
