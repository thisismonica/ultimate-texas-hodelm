__author__ = 'monica_wang'

from card import Card
from hand import Hand

files = ["royalflush.txt", "straightflush.txt", "fourofakind", "fullhouse.txt", "flush.txt", "straight.txt", "threeofakind.txt", "twopair", "pair.txt", "highcard.txt"]
expects = ["[10 of Diamond, J of Diamond, Q of Diamond, K of Diamond, A of Diamond] (Type: ROYAL FLUSH)",
           "[3 of Diamond, 4 of Diamond, 5 of Diamond, 6 of Diamond, 7 of Diamond] (Type: STRAIGHT FLUSH)",
           "[2 of Spade, 2 of Diamond, 2 of Clubs, 2 of Hearts, J of Diamond] (Type: FOUR OF A KIND)",
           "[2 of Spade, 2 of Clubs, 2 of Hearts, K of Diamond, K of Hearts] (Type: FULL HOUSE)",
           "[3 of Diamond, 9 of Diamond, 10 of Diamond, J of Diamond, Q of Diamond] (Type: FLUSH)",
           "[10 of Diamond, J of Diamond, Q of Diamond, K of Hearts, A of Hearts] (Type: STRAIGHT)",
           "[10 of Hearts, 10 of Diamond, 10 of Clubs, 2 of Hearts, J of Diamond] (Type: THREE OF A KIND)",
           "[K of Diamond, K of Hearts, 6 of Hearts, 6 of Diamond, 10 of Diamond] (Type: TWO PAIR)",
           "[2 of Spade, 2 of Hearts, 10 of Diamond, J of Diamond, K of Hearts] (Type: PAIR)",
           "[6 of Diamond, 10 of Diamond, J of Diamond, K of Hearts, A of Hearts] (Type: HIGH CARD)"
           ]
totalPassed = 0
for i,file in enumerate(files):
    filename = '../testHand/' + file
    cards = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            rank, spade = line.split()
            cards.append(Card(rank, spade))

    hand = Hand(cards)
    if str(hand) == expects[i]:
        totalPassed +=1
        "Test ",i," passed!"
    else:
        "Test ",i," passed!"
        print "Output: ", hand
        print "Was expecting: ", expects[i]
print "================"
print "Run Tests: ",len(files)," Passed: ",totalPassed, ", Failed: ",len(files) - totalPassed