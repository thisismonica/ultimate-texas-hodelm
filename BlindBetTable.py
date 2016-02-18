__author__ = 'monica_wang'
'''
Royal flush	500 to 1
Straight flush	50 to 1
Four of a kind	10 to 1
Full house	3 to 1
Flush	3 to 2
Straight	1 to 1
'''

from hand import HandType

class BlindBet:
    Table = {
            HandType.UNDEFINED: 0.0,
            HandType.HIGH_CARD: 0.0,
            HandType.PAIR: 0.0,
            HandType.TWO_PAIR: 0.0,
            HandType.THREE_OF_A_KIND: 4.0,
            HandType.STRAIGHT: 1.0,
            HandType.FLUSH: 1.5,
            HandType.FULL_HOUSE: 3.0,
            HandType.FOUR_OF_A_KIND: 10.0,
            HandType.STRAIGHT_FLUSH: 50.0,
            HandType.ROYAL_FLUSH: 500.0
    }


