from card import Card

class HandType:
    UNDEFINED = 0
    HIGH_CARD = 1
    PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9
    ROYAL_FLUSH = 10

'''
Return   1 if rank1 > rank2
         -1 if rank1 < rank2
        0 if rank1 == rank2
'''
def compareRanks(rank1, rank2):
    rank1.sort(key=lambda x: Card.VALUES[x], reverse=True)
    rank2.sort(key=lambda x: Card.VALUES[x], reverse=True)

    for i in range(len(rank1)):
        if Card.VALUES[rank1[i]] > Card.VALUES[rank2[i]]:
            return 1
        elif Card.VALUES[rank1[i]] < Card.VALUES[rank2[i]]:
            return -1
    return 0

'''
Return   1 if hand1 > hand2
         -1 if hand1 < hand2
        0 if hand1 == hand2
'''
def compareHands(hand1, hand2):
    if hand1.type > hand2.type:
        return 1
    if hand1.type < hand2.type:
        return -1
    else:
        if hand1.type == HandType.HIGH_CARD or hand1.type == HandType.STRAIGHT or hand1.type == HandType.FLUSH or hand1.type == HandType.STRAIGHT_FLUSH:
            return compareRanks([h.getRank()for h in hand1.hand], [h.getRank() for h in hand2.hand] )

        elif hand1.type == HandType.PAIR or hand1.type == HandType.TWO_PAIR or hand1.type == HandType.THREE_OF_A_KIND or hand1.type == HandType.FOUR_OF_A_KIND:
            for i in range(len(hand1.specialCardsRank)):
                if Card.VALUES[hand1.specialCardsRank[i]] > Card.VALUES[hand2.specialCardsRank[i]]:
                    return 1
                elif Card.VALUES[hand1.specialCardsRank[i]] < Card.VALUES[hand2.specialCardsRank[i]]:
                    return -1
            return compareRanks([h.getRank() for h in hand1.hand if h.getRank() not in hand1.specialCardsRank],
                                    [h.getRank() for h in hand2.hand if h.getRank() not in hand2.specialCardsRank])

        elif hand1.type == HandType.FULL_HOUSE:
            for i in range(len(hand1.specialCardsRank)):
                if Card.VALUES[hand1.specialCardsRank[i]] > Card.VALUES[hand2.specialCardsRank[i]]:
                    return 1
                elif Card.VALUES[hand1.specialCardsRank[i]] < Card.VALUES[hand2.specialCardsRank[i]]:
                    return -1
            return 0

        elif hand1.type == HandType.ROYAL_FLUSH:
            return 0

class Hand:
    def __init__(self, cards):
        self.cards = cards # 7 cards. 5 cards in hand
        self.type = HandType.UNDEFINED
        self.hand = []
        self.specialCardsRank = [] # special part of this hand, pair(s), three of a kind...
        self.checkHandRank() # hand has only 5 cards

    def checkHandRank(self):
        suits, ranks = {}, {}

        for c in self.cards:
            ranks[c.getRank()] = [c] if c.getRank() not in ranks else ranks[c.getRank()] + [c]
            suits[c.getSuit()] = [c] if c.getSuit() not in suits else suits[c.getSuit()] + [c]

        self.suits = suits

        self.checkStraight(ranks)
        if self.type != HandType.STRAIGHT_FLUSH:
            self.checkFlush(suits)

        if self.type != HandType.UNDEFINED:
            return

        self.checkDuplicates(ranks)

    def checkStraight(self, ranks):
        sorted_ranks = sorted(ranks.keys(), key=lambda card: Card.VALUES[card])
        if sorted_ranks[0] == 'A':
            sorted_ranks.append('A')

        starts = []
        for i, r in enumerate(sorted_ranks[:-4]):
            prev = r
            isStraight = True
            for a in sorted_ranks[i+1:i+5]:
                if Card.VALUES[a] != (Card.VALUES[prev] + 1)%13:
                    isStraight = False
                    break
                prev = a
            if isStraight:
                starts.append(i)

        if starts != []:
            self.type = HandType.STRAIGHT
            hand = []
            for start in starts: # check each start points
                hand = [ranks[r][0] for r in sorted_ranks[start:start+5]]
                i = 1
                while i != len(hand) and hand[i].getSuit() == hand[0].getSuit():
                    i += 1
                if i == len(hand):
                    self.type = HandType.STRAIGHT_FLUSH
                    self.hand = hand
                    if self.hand[0].getRank() == '10':
                        self.type = HandType.ROYAL_FLUSH
                        return
            self.hand = hand if self.type == HandType.STRAIGHT else self.hand

    def checkFlush(self, suits):
        for s in suits:
            if len(suits[s]) >= 5:
                self.type = HandType.FLUSH if self.type < HandType.FLUSH else self.type
                self.hand = sorted(suits[s], key=lambda c: Card.VALUES[c.getRank()])[-5:]
                break

    def checkDuplicates(self, ranks):
        # Check Four of a kind
        for r in ranks.keys():
            if len(ranks[r]) == 4:
                self.type = HandType.FOUR_OF_A_KIND
                self.specialCardsRank = [r]
                self.hand = ranks[r]
        if (self.type == HandType.FOUR_OF_A_KIND):
            self.hand += [sorted([c for c in self.cards if c.getRank() not in self.specialCardsRank], key=lambda card: Card.VALUES[card.getRank()])[-1]]
        else:
            # Check Three of a Kind
            for r in ranks.keys():
                if len(ranks[r]) == 3:
                    self.type = HandType.THREE_OF_A_KIND
                    self.specialCardsRank.append(r)
            if self.type == HandType.THREE_OF_A_KIND:
                if len(self.specialCardsRank) > 1:
                    self.specialCardsRank = [self.specialCardsRank[0]] \
                        if Card.VALUES[self.specialCardsRank[0]] > Card.VALUES[self.specialCardsRank[1]] else [self.specialCardsRank[1]]

                # Check Full house
                specialCardsRankForPair = []
                for r in ranks.keys():
                    if len(ranks[r]) == 2:
                        self.type = HandType.FULL_HOUSE
                    specialCardsRankForPair.append(r)

                if self.type == HandType.FULL_HOUSE:
                    if len(specialCardsRankForPair) > 1:
                        specialCardsRankForPair = [specialCardsRankForPair[0]] \
                            if Card.VALUES[specialCardsRankForPair[0]] > Card.VALUES[specialCardsRankForPair[1]] else [specialCardsRankForPair[1]]
                    self.hand = ranks[self.specialCardsRank[0]] + ranks[specialCardsRankForPair[0]]
                    self.specialCardsRank += specialCardsRankForPair
                else:
                    self.hand = ranks[self.specialCardsRank[0]] + sorted([c for c in self.cards if c.getRank() not in self.specialCardsRank], key=lambda card: Card.VALUES[card.getRank()])[-2:]
            else:
                # Check Two Pair
                for r in ranks.keys():
                    if len(ranks[r]) == 2:
                        if self.type == HandType.PAIR or self.type == HandType.TWO_PAIR:
                            self.type = HandType.TWO_PAIR
                            if len(self.specialCardsRank) < 2:
                                self.specialCardsRank.append(r)
                            else:
                                if Card.VALUES[r] > Card.VALUES[min(self.specialCardsRank, key=lambda x:Card.VALUES[x])]:
                                    self.specialCardsRank.remove(min(self.specialCardsRank, key=lambda x:Card.VALUES[x]))
                                    self.specialCardsRank.append(r)
                        else:
                            self.type = HandType.PAIR
                            self.specialCardsRank.append(r)
                if self.type == HandType.TWO_PAIR:
                    self.hand = ranks[self.specialCardsRank[0]] + ranks[self.specialCardsRank[1]] + \
                                [sorted([c for c in self.cards if c.getRank() not in self.specialCardsRank], key=lambda card: Card.VALUES[card.getRank()])[-1]]
                elif self.type == HandType.PAIR:
                    self.hand = ranks[self.specialCardsRank[0]] + \
                                sorted([c for c in self.cards if c.getRank() not in self.specialCardsRank], key=lambda card: Card.VALUES[card.getRank()])[-3:]
                else:
                    self.type = HandType.HIGH_CARD
                    self.hand = sorted(self.cards, key=lambda card: Card.VALUES[card.getRank()])[-5:]

    def __str__(self):
        TypeStr = { HandType.UNDEFINED: 'UNDEFINED',
                    HandType.HIGH_CARD: 'HIGH CARD',
                    HandType.PAIR: 'PAIR',
                    HandType.TWO_PAIR: 'TWO PAIR',
                    HandType.THREE_OF_A_KIND: 'THREE OF A KIND',
                    HandType.STRAIGHT: 'STRAIGHT',
                    HandType.FLUSH: 'FLUSH',
                    HandType.FULL_HOUSE: 'FULL HOUSE',
                    HandType.FOUR_OF_A_KIND: 'FOUR OF A KIND',
                    HandType.STRAIGHT_FLUSH: 'STRAIGHT FLUSH',
                    HandType.ROYAL_FLUSH: 'ROYAL FLUSH'}
        res = "[" + ", ".join([str(c) for c in self.hand]) + "] "
        res += "(Type: " + TypeStr[self.type] + ")"
        return res

