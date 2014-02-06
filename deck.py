#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      marioga
#
# Created:     05/02/2014
# Copyright:   (c) marioga 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

''' This is the implementation of the deck class. A "deck" consists of _size
decks of 52 cards.
'''
from card import card
from random import shuffle

class deck:
    def __init__(self, size=8):
        try:
            self._size=int(size)
        except ValueError:
            print ("Input for deck is not an integer")
        # We now populate the deck
        self._cards=[]
        for num_decks in range(self._size):
            for rank in range(13):
                for suit in range(4):
                    self._cards.append(card(rank,suit))

    def pop(self):
        return self._cards.pop()

    def cardsLeft(self):
        return len(self._cards)

    def shuffle(self):
        shuffle(self._cards)

def main():
    pass

if __name__ == '__main__':
    d = deck()
    d.shuffle()
    print (d.pop())
    print (d.cardsLeft())
    print (d.pop())
    print (d.cardsLeft())

