from card import Card
import random

class Deck:
    def __init__(self, numofDecks):
        self._cards = []
        self._numofDecks = numofDecks
        for i in range( numofDecks ):
            for suit in Card.SUITS:
                for rank in Card.RANKS:
                    c = Card(rank, suit)
                    self._cards.append(c)

    def shuffle(self):
        random.shuffle(self._cards)
    
    # Removes top cards
    def draw(self, number):
        res = []
        for i in range(number):
            res.append(self._cards.pop())
        return res

    def __len__(self):
        return len(self._cards)

    def __str__(self):
        res = ""
        for c in self._cards:
            res = res+str(c)+'\n'
        return res


