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

# from hand import hand

class Player:
    def __init__(self,hand=None,money=0):
        self._hand=hand
        try:
            self._money=int(money)
        except ValueError:
            print ("Money is not an integer")

    def displayHand(self):
        # Print the contents in hand
        pass

    def bet(self,n):
        try:
            if self._money<int(n):
                print("Not enough money")
            else:
                self._money-=n
        except ValueError:
            print ("Bet is not an integer")









def main():
    pass

if __name__ == '__main__':
    main()
