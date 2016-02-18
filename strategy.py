__author__ = 'monica_wang'

from card import Card
from hand import Hand
from hand import HandType

def round1Bet(hand):
    if len(hand) != 2:
        raise Exception("wrong number of hand")
    hcard, lcard = sorted(hand, key=lambda c: Card.VALUES[c.getRank()], reverse=True)

    if hcard.getRank() == 'A':
        return 4.0
    if hcard.getRank() == 'K' and (Card.VALUES[lcard.getRank()] > 4 or hcard.getSuit() == lcard.getSuit()):
        return 4.0
    if hcard.getRank() == 'Q' and (Card.VALUES[lcard.getRank()] > 7 or (hcard.getSuit() == lcard.getSuit()) and Card.VALUES[lcard.getRank()] > 5):
        return 4.0
    if hcard.getRank() == 'J' and (Card.VALUES[lcard.getRank()] > 9 or (hcard.getSuit() == lcard.getSuit()) and Card.VALUES[lcard.getRank()] > 7):
        return 4.0

    return 0.0


def round2Bet(hand, community):
    if len(hand) != 2 or len(community) != 3:
        raise Exception("wrong number of hand")

    #Two pair or better.
    current = Hand(hand + community)
    if current.type >= HandType.TWO_PAIR:
        return 2.0

    #Hidden pair*, except pocket deuces.
    if current.type == HandType.PAIR:
        numInCommunity = 0
        for c in community:
            if c.getRank() in current.specialCardsRank:
                numInCommunity += 1
        if numInCommunity == 1:
            return 2.0

    #Four to a flush, including a hidden 10 or better to that flush
    for s in current.suits:
        if len(current.suits[s]) == 4:
            if hand[0] == s and Card.VALUES[hand[0].getRank()] >= 10 or  hand[1] == s and Card.VALUES[hand[1].getRank()] >= 10:
                return 2.0
    return 0.0

def round3Bet(playhand, community):
    if len(playhand) != 2 or len(community) != 5:
        raise Exception("wrong number of hand")

    # Hidden pair or better.
    current = Hand(playhand + community)
    if current.type == HandType.PAIR:
        numInCommunity = 0
        for c in community:
            if c.getRank() in current.specialCardsRank:
                numInCommunity += 1
        if numInCommunity == 1:
            return 1.0
        else:
            return 0.0
    if current.type > HandType.PAIR:
        return 1.0

    #Less than 21 cards dealer outs beat you
    minCardRankValueinHand = min([Card.VALUES[c.getRank()]for c in current.hand])
    numOfCardsPairDealer = 15   # num of cards that can pair dealer to beat you (since you don't have hidden pair)
    if current.type == HandType.PAIR:
        numOfCardsPairDealer = 12

    numOfCardsLarger = 0
    hcard, lcard = sorted(playhand, key=lambda c: Card.VALUES[c.getRank()])
    trial = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
    for t in trial:
        if Card.VALUES[t] > Card.VALUES[hcard.getRank()] and Card.VALUES[t] > minCardRankValueinHand:
            numOfCardsLarger += 1
    numOfCardsLarger *= 4

    if numOfCardsLarger + numOfCardsPairDealer < 21:
        return 1.0
    else:
        return 0.0
