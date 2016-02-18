class Card:
    RANKS = ('2','3','4','5','6','7','8','9','10','J','Q','K','A')
    SUITS = ('Spade','Diamond','Hearts', 'Clubs')
    VALUES = {'A':12, '2':0, '3':1, '4':2, '5':3, '6':4, '7':5, '8':6, '9':7, '10':8, 'J':9, 'Q':10, 'K':11}

    def __init__(self, rank, suit):
        if rank not in self.RANKS or suit not in self.SUITS:
            raise Exception("Illegal input of cards.")
        self._rank = rank
        self._suit = suit

    def getRank(self):
        return self._rank

    def getSuit(self):
        return self._suit

    def __str__(self):
        return self._rank + " of " + self._suit

'''
    def get21Value(self):
        if self._rank in self.NUMBERS:
            return int(self._rank)
        elif self._rank in self.FACES:
            return 10
        else:
            return 11
'''

