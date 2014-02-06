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
            print (card)

    def isBusted(self):
        ''' isBusted() -> bool -- returns if the hand has a busted hand value '''
        return sum(self.value()) == -1

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
        elif total<=21:
            total = [total]
        else: #assign total of -1 to busted hands. this will be useful for comparison since busted hands never win
            total=[-1]
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
        playerhand = Hand([Card('K')])
        self.assertEqual(playerhand.value(),[10])
        playerhand.receive(Card('Q'))
        self.assertEqual(playerhand.value(),[20])
        playerhand.receive(Card('A'))
        self.assertEqual(playerhand.value(),[21])

        playerhand = Hand([Card('A'),Card('A')])
        self.assertEqual(playerhand.value(),[2,12])
        
        playerhand = Hand([Card('K')])
        playerhand.receive(Card('A'))
        self.assertEqual(playerhand.value(),[11,21])

    def test_compare(self):
        playerhand = Hand([Card('K')])
        dealerhand = Hand([Card('K')])
        self.assertTrue(playerhand ==  dealerhand)
        playerhand.receive(Card('A'))
        dealerhand = Hand(Card('9'))
        self.assertTrue(playerhand >  dealerhand)
        dealerhand = Hand(Card('2'))
        # winning base on the blackjack rule
        self.assertTrue(playerhand.isBlackJack())
        self.assertTrue(playerhand >  dealerhand)

        playerhand = Hand([Card('K')])
        dealerhand = Hand([Card('Q')])
        self.assertTrue(playerhand ==  dealerhand)

    def test_handStates(self):
        hand = Hand([Card('K'),Card('K'),Card('K')])
        self.assertTrue(hand.isBusted())

if __name__ == "__main__":
    unittest.main()
